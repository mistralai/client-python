#!/usr/bin/env python

import asyncio
import os

from mistralai.async_client import MistralAsyncClient
from mistralai.models.jobs import TrainingParameters

POLLING_INTERVAL = 10


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = MistralAsyncClient(api_key=api_key)

    # Create new files
    with open("examples/file.jsonl", "rb") as f:
        training_file = await client.files.create(file=f)
    with open("examples/validation_file.jsonl", "rb") as f:
        validation_file = await client.files.create(file=f)
    # Create a new job
    created_job = await client.jobs.create(
        model="open-mistral-7b",
        training_files=[training_file.id],
        validation_files=[validation_file.id],
        hyperparameters=TrainingParameters(
            training_steps=1,
            learning_rate=0.0001,
        ),
    )
    print(created_job)

    while created_job.status in ["RUNNING", "QUEUED"]:
        created_job = await client.jobs.retrieve(created_job.id)
        print(f"Job is {created_job.status}, waiting {POLLING_INTERVAL} seconds")
        await asyncio.sleep(POLLING_INTERVAL)

    if created_job.status == "FAILED":
        print("Job failed")
        return

    # Chat with model
    response = await client.chat(
        model=created_job.fine_tuned_model,
        messages=[
            {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
            {"role": "user", "content": "What is the capital of France ?"},
        ],
    )

    print(response.choices[0].message.content)

    # Delete files
    await client.files.delete(training_file.id)
    await client.files.delete(validation_file.id)

    # Delete fine-tuned model
    await client.delete_model(created_job.fine_tuned_model)


if __name__ == "__main__":
    asyncio.run(main())
