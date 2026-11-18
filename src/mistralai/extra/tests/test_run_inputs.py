import json

import httpx2 as httpx
import pydantic
import pytest

from mistralai.client import Mistral
from mistralai.client.models import (
    FunctionCallEntry,
    FunctionResultEntry,
    InputEntries,
    MessageInputEntry,
    MessageOutputEntry,
)
from mistralai.extra.run.context import RunContext

RESPONSE = {
    "object": "conversation.response",
    "conversation_id": "conv_1",
    "outputs": [
        {
            "object": "entry",
            "type": "message.output",
            "role": "assistant",
            "content": "ok",
        }
    ],
    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
}


def _client(sent: list[dict]) -> Mistral:
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json=RESPONSE)

    return Mistral(
        api_key="test",
        async_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


@pytest.mark.asyncio
async def test_run_async_forwards_typed_input_entries() -> None:
    sent: list[dict] = []
    client = _client(sent)
    inputs: list[InputEntries] = [
        MessageInputEntry(role="user", content="Hello"),
        MessageOutputEntry(content="Hi"),
        FunctionCallEntry(tool_call_id="call_1", name="f", arguments="{}"),
        FunctionResultEntry(tool_call_id="call_1", result="42"),
    ]
    async with RunContext(model="mistral-medium-latest") as ctx:
        result = await client.beta.conversations.run_async(run_ctx=ctx, inputs=inputs)

    assert [entry["type"] for entry in sent[0]["inputs"]] == [
        "message.input",
        "message.output",
        "function.call",
        "function.result",
    ]
    assert sent[0]["inputs"][0]["content"] == "Hello"
    assert sent[0]["inputs"][1]["content"] == "Hi"
    assert result.input_entries == inputs


@pytest.mark.asyncio
async def test_run_async_rejects_unknown_input() -> None:
    sent: list[dict] = []
    client = _client(sent)
    async with RunContext(model="mistral-medium-latest") as ctx:
        with pytest.raises(pydantic.ValidationError):
            await client.beta.conversations.run_async(
                run_ctx=ctx,
                inputs=[object()],  # type: ignore[arg-type]
            )
    assert sent == []
