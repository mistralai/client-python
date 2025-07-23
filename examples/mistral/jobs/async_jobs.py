#!/usr/bin/env python

import asyncio
import os

from mistralai import Mistral
from mistralai.models import File, CompletionTrainingParametersIn


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Create new files
    with open("examples/fixtures/ft_training_file.jsonl", "rb") as f:
        training_file = await client.files.upload_async(
            file=File(file_name="file.jsonl", content=f)
        )
    with open("examples/fixtures/ft_validation_file.jsonl", "rb") as f:
        validation_file = await client.files.upload_async(
            file=File(file_name="validation_file.jsonl", content=f)
        )

    # Create a new job
    created_job = await client.fine_tuning.jobs.create_async(
        model="open-mistral-7b",
        training_files=[{"file_id": training_file.id, "weight": 1}],
        validation_files=[validation_file.id],
        hyperparameters=CompletionTrainingParametersIn(
            training_steps=1,
            learning_rate=0.0001,
        ),
    )
    print(created_job)

    # List jobs
    jobs = await client.fine_tuning.jobs.list_async(page=0, page_size=5)
    print(jobs)

    # Retrieve a job
    retrieved_job = await client.fine_tuning.jobs.get_async(job_id=created_job.id)
    print(retrieved_job)

    # Cancel a job
    canceled_job = await client.fine_tuning.jobs.cancel_async(job_id=created_job.id)
    print(canceled_job)

    # Delete files
    await client.files.delete_async(file_id=training_file.id)
    await client.files.delete_async(file_id=validation_file.id)


if __name__ == "__main__":
    asyncio.run(main())
