#!/usr/bin/env python

import asyncio
import os

from mistralai import Mistral
from mistralai.models import TrainingParametersIn


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Create new files
    with open("examples/file.jsonl", "rb") as f:
        training_file = await client.files.upload_async(
            file={"file_name": "test-file.jsonl", "content": f}
        )

    # Create a new job
    dry_run_job = await client.fine_tuning.jobs.create_async(
        model="open-mistral-7b",
        training_files=[{"file_id": training_file.id, "weight": 1}],
        hyperparameters=TrainingParametersIn(
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
