from mistralai import Mistral, BatchRequest, UserMessage
import os
import asyncio


async def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    requests = [BatchRequest(
        custom_id=str(i),
        body=dict(
            model="mistral-medium-latest",
            messages=[UserMessage(
                content=f"What's i + {i}"
            )]
        )
    ) for i in range(5)
    ]

    job = await client.batch.jobs.create_async(
        requests=requests,
        model="mistral-small-latest",
        endpoint="/v1/chat/completions",
        metadata={"job_type": "testing"}
    )

    print(f"Created job with ID: {job.id}")

    while job.status not in ["SUCCESS", "FAILED"]:
        await asyncio.sleep(1)
        job = await client.batch.jobs.get_async(job_id=job.id)
        print(f"Job status: {job.status}")

    print(f"Job is done, status {job.status}")
    for res in job.outputs:
        print(res["response"]["body"])

if __name__ == "__main__":
    asyncio.run(main())
