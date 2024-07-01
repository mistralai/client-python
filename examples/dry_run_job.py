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

    # Create a new job
    dry_run_job = await client.jobs.create(
        model="open-mistral-7b",
        training_files=[training_file.id],
        hyperparameters=TrainingParameters(
            training_steps=1,
            learning_rate=0.0001,
        ),
        dry_run=True,
    )

    print("Dry run job created")
    print(f"Train tokens: {dry_run_job.train_tokens}")
    print(f"Dataset tokens: {dry_run_job.data_tokens}")
    print(f"Epochs number: {dry_run_job.epochs}")
    print(f"Expected duration: {dry_run_job.expected_duration_seconds}")
    print(f"Cost: {dry_run_job.cost} {dry_run_job.cost_currency}")


if __name__ == "__main__":
    asyncio.run(main())
