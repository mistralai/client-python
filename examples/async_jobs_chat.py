#!/usr/bin/env python
import asyncio
import json
import os
import random
from pathlib import Path

from mistralai import Mistral
from mistralai.models import (
    File,
    CompletionTrainingParametersIn,
)

POLLING_INTERVAL = 10

cwd = Path(__file__).parent

user_contents = [
    "How far is the Moon from Earth?",
    "What's the largest ocean on Earth?",
    "How many continents are there?",
    "What's the powerhouse of the cell?",
    "What's the speed of light?",
    "Can you solve a Rubik's Cube?",
    "What is the tallest mountain in the world?",
    "Who painted the Mona Lisa?",
]

# List of assistant contents
assistant_contents = [
    "Around 384,400 kilometers. Give or take a few, like that really matters.",
    "The Pacific Ocean. You know, the one that covers more than 60 million square miles. No big deal.",
    "There are seven continents. I hope that wasn't too hard to count.",
    "The mitochondria. Remember that from high school biology?",
    "Approximately 299,792 kilometers per second. You know, faster than your internet speed.",
    "I could if I had hands. What's your excuse?",
    "Mount Everest, standing at 29,029 feet. You know, just a little hill.",
    "Leonardo da Vinci. Just another guy who liked to doodle.",
]

system_message = "Marv is a factual chatbot that is also sarcastic"

def create_validation_file() -> bytes:
    return json.dumps({
        "messages": [
            {"role": "user", "content": "How long does it take to travel around the Earth?"},
            {"role": "assistant", "content": "Around 24 hours if you're the Earth itself. For you, depends on your mode of transportation."}
        ],
        "temperature": random.random()
    }).encode()

async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    requests = []
    for um, am in zip(
        random.sample(user_contents, len(user_contents)),
        random.sample(assistant_contents, len(assistant_contents)),
    ):
        requests.append(json.dumps({
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": um},
                {"role": "assistant", "content": am},
            ]
        }))

    # Create new files
    training_file = await client.files.upload_async(
        file=File(
            file_name="file.jsonl", content=("\n".join(requests)).encode()
        ),
        purpose="fine-tune",
    )

    validation_file = await client.files.upload_async(
        file=File(
            file_name="validation_file.jsonl", content=create_validation_file()
        ),
        purpose="fine-tune",
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

    while created_job.status in ["RUNNING", "STARTED", "QUEUED", "VALIDATING", "VALIDATED"]:
        created_job = await client.fine_tuning.jobs.get_async(job_id=created_job.id)
        print(f"Job is {created_job.status}, waiting {POLLING_INTERVAL} seconds")
        await asyncio.sleep(POLLING_INTERVAL)

    if created_job.status == "FAILED":
        print("Job failed")
        raise Exception(f"Job failed with {created_job.status}")

    print(created_job)
    # Chat with model
    response = await client.chat.complete_async(
        model=created_job.fine_tuned_model,
        messages=[
            {
                "role": "system",
                "content": "Marv is a factual chatbot that is also sarcastic.",
            },
            {"role": "user", "content": "What is the capital of France ?"},
        ],
    )

    print(response.choices[0].message.content)

    # Delete files
    await client.files.delete_async(file_id=training_file.id)
    await client.files.delete_async(file_id=validation_file.id)

    # Delete fine-tuned model
    await client.models.delete_async(model_id=created_job.fine_tuned_model)


if __name__ == "__main__":
    asyncio.run(main())
