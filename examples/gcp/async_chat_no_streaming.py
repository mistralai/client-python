#!/usr/bin/env python

import asyncio
import os
import subprocess

from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.models.usermessage import UserMessage

GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]


def _get_token():
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


async def main():
    client = MistralGCP(
        api_key=_get_token(),
        server_url=_build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
    )

    chat_response = await client.chat.complete_async(
        model=GCP_MODEL,
        messages=[UserMessage(content="What is the best French cheese?")],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
