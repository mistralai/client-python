#!/usr/bin/env python

from pprint import pprint
import asyncio
from mistralai import Mistral, TrainingFile, ClassifierTrainingParametersIn

import os


async def upload_files(client: Mistral, file_names: list[str]) -> list[str]:
    # Upload files
    print("Uploading files...")

    file_ids = []
    for file_name in file_names:
        with open(file_name, "rb") as file:
            f = await client.files.upload_async(
                file={
                    "file_name": file_name,
                    "content": file.read(),
                },
                purpose="fine-tune",
            )
        file_ids.append(f.id)
    print("Files uploaded...")
    return file_ids


async def train_classifier(client: Mistral,training_file_ids: list[str]) -> str:
    print("Creating job...")
    job = await client.fine_tuning.jobs.create_async(
        model="ministral-3b-latest",
        job_type="classifier",
        training_files=[
            TrainingFile(file_id=training_file_id)
            for training_file_id in training_file_ids
        ],
        hyperparameters=ClassifierTrainingParametersIn(
            learning_rate=0.0001,
        ),
        auto_start=True,
    )

    print(f"Job created ({job.id})")

    i = 1
    while True:
        await asyncio.sleep(10)
        detailed_job = await client.fine_tuning.jobs.get_async(job_id=job.id)
        if detailed_job.status not in [
            "QUEUED",
            "STARTED",
            "VALIDATING",
            "VALIDATED",
            "RUNNING",
        ]:
            break
        print(f"Still training after {i * 10} seconds")
        i += 1

    if detailed_job.status != "SUCCESS":
        print("Training failed")
        raise Exception(f"Job failed {detailed_job.status}")

    print(f"Training succeed: {detailed_job.fine_tuned_model}")

    return detailed_job.fine_tuned_model


async def main():
    training_files = ["./examples/fixtures/classifier_sentiments.jsonl"]
    client = Mistral(
        api_key=os.environ["MISTRAL_API_KEY"],
    )

    training_file_ids: list[str] = await upload_files(client=client, file_names=training_files)
    model_name: str | None = await train_classifier(client=client,training_file_ids=training_file_ids)

    if model_name:
        print("Calling inference...")
        response = client.classifiers.classify(
            model=model_name,
            inputs=["It's nice", "It's terrible", "Why not"],
        )
        print("Inference succeed !")
        pprint(response)

        print("Calling inference (Chat)...")
        response = client.classifiers.classify_chat(
            model=model_name,
            inputs={"messages": [{"role": "user", "content": "Lame..."}]},
        )
        print("Inference succeed (Chat)!")
        pprint(response)


if __name__ == "__main__":
    asyncio.run(main())
