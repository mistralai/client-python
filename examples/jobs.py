#!/usr/bin/env python
import os

from mistralai.client import MistralClient
from mistralai.models.jobs import TrainingParameters


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    # Create new files
    with open("examples/file.jsonl", "rb") as f:
        training_file = client.files.create(file=f)
    with open("examples/validation_file.jsonl", "rb") as f:
        validation_file = client.files.create(file=f)

    # Create a new job
    created_job = client.jobs.create(
        model="open-mistral-7b",
        training_files=[training_file.id],
        validation_files=[validation_file.id],
        hyperparameters=TrainingParameters(
            training_steps=1,
            learning_rate=0.0001,
        ),
    )
    print(created_job)

    jobs = client.jobs.list(created_after=created_job.created_at - 10)
    for job in jobs.data:
        print(f"Retrieved job: {job.id}")

    # Retrieve a job
    retrieved_job = client.jobs.retrieve(created_job.id)
    print(retrieved_job)

    # Cancel a job
    canceled_job = client.jobs.cancel(created_job.id)
    print(canceled_job)

    # Delete files
    client.files.delete(training_file.id)
    client.files.delete(validation_file.id)


if __name__ == "__main__":
    main()
