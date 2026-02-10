#!/usr/bin/env python
import os

from mistralai.client import Mistral
from mistralai.client.models import File, CompletionTrainingParametersIn


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Create new files
    with open("examples/fixtures/ft_training_file.jsonl", "rb") as f:
        training_file = client.files.upload(
            file=File(file_name="file.jsonl", content=f)
        )
    with open("examples/fixtures/ft_validation_file.jsonl", "rb") as f:
        validation_file = client.files.upload(
            file=File(file_name="validation_file.jsonl", content=f)
        )

    # Create a new job
    created_job = client.fine_tuning.jobs.create(
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
    jobs = client.fine_tuning.jobs.list(page=0, page_size=5)
    print(jobs)

    # Retrieve a job
    retrieved_job = client.fine_tuning.jobs.get(job_id=created_job.id)
    print(retrieved_job)

    # Cancel a job
    canceled_job = client.fine_tuning.jobs.cancel(job_id=created_job.id)
    print(canceled_job)

    # Delete files
    client.files.delete(file_id=training_file.id)
    client.files.delete(file_id=validation_file.id)


if __name__ == "__main__":
    main()
