"""Run an embeddings batch job with the typed BatchClient.

Compare with async_batch_job_chat_completion_inline.py, which hand-builds the
request lines and would hand-parse the output. BatchClient owns the JSONL wire
format and the upload/create/poll/download lifecycle; you pass typed request
bodies keyed by custom_id and read back typed responses.

The two type params bind to the SDK's own per-endpoint models -- here
EmbeddingRequest / EmbeddingResponse. For another endpoint, swap the endpoint
string and response_body_type (e.g. "/v1/chat/completions", ChatCompletionResponse).
"""

import asyncio
import os

from mistralai.client import Mistral
from mistralai.client.models import EmbeddingRequest, EmbeddingResponse
from mistralai.extra.batch import BatchClient, BatchInput


async def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    batch = BatchClient(
        client,
        endpoint="/v1/embeddings",
        response_body_type=EmbeddingResponse,
    )

    texts = {
        "doc-0": "What is the best French cheese?",
        "doc-1": "What is the best French wine?",
    }

    # Pass typed bodies keyed by custom_id straight to run() -- it sends them
    # inline (or uploads if large), then blocks until the job reaches a terminal
    # state (owns the poll loop). The pure BatchInput below is I/O-free; build it
    # anywhere. To run the same input again later, upload it and keep the file id:
    #     payload = BatchInput.from_payload({...})
    #     f = await batch.upload(payload)      # f.file_id -- stash and reuse
    #     result = await batch.run(f)
    result = await batch.run(
        BatchInput.from_payload(
            {
                custom_id: EmbeddingRequest(model="mistral-embed", inputs=text)
                for custom_id, text in texts.items()
            }
        )
    )
    print(
        f"Job {result.job.id}: {result.status} "
        f"({result.succeeded} ok, {result.failed} failed)"
    )

    # run() already downloaded and parsed the output/error files, so these are sync.
    for custom_id, response in result.by_id().items():
        print(f"{custom_id}: {len(response.data[0].embedding)}-dim embedding")

    for err in result.errors():
        print(f"{err.custom_id} failed: {err.status_code} {err.error}")

    # Responses the API returned but that didn't match EmbeddingResponse (a schema
    # mismatch) land here instead of raising, so one bad line never loses the rest.
    for err in result.response_errors():
        print(f"{err.custom_id} unparseable: {err.error}")

    # For a large result, stream_results() instead of run() to read it one line at a
    # time (constant memory). It binds to a job you already own -- create it (or
    # rehydrate one from a prior process via batch.get(job_id)) and pass the handle;
    # it reads only, so cleaning up the job and its files stays yours:
    #     handle = await batch.create(BatchInput.from_payload({...}))
    #     async for custom_id, item in batch.stream_results(handle):
    #         ...  # item is a typed EmbeddingResponse or a BatchRequestError


if __name__ == "__main__":
    asyncio.run(main())
