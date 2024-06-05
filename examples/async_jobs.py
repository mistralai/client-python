#!/usr/bin/env python

import asyncio
import os

from mistralai.async_client import MistralAsyncClient
from mistralai.models.jobs import TrainingParameters


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

    # List jobs
    jobs = await client.jobs.list(page=0, page_size=5)
    print(jobs)

    # Retrieve a job
    retrieved_job = await client.jobs.retrieve(created_job.id)
    print(retrieved_job)

    # Cancel a job
    canceled_job = await client.jobs.cancel(created_job.id)
    print(canceled_job)

    # Delete files
    await client.files.delete(training_file.id)
    await client.files.delete(validation_file.id)


if __name__ == "__main__":
    asyncio.run(main())
