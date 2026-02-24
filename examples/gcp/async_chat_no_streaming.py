#!/usr/bin/env python
"""
Example: Async chat completion with GCP Vertex AI.

The SDK automatically:
- Detects credentials via google.auth.default()
- Auto-refreshes tokens when they expire
- Builds the Vertex AI URL from project_id and region

Prerequisites:
    gcloud auth application-default login

Usage:
    GCP_PROJECT_ID=your-project GCP_REGION=us-central1 GCP_MODEL=mistral-small-2503 python async_chat_no_streaming.py
"""

import asyncio
import os

from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.models.usermessage import UserMessage

# Configuration from environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")  # Optional: auto-detected from credentials
GCP_REGION = os.environ.get("GCP_REGION", "us-central1")
GCP_MODEL = os.environ.get("GCP_MODEL", "mistral-small-2503")


async def main():
    # The SDK automatically handles:
    # - Credential detection via google.auth.default()
    # - Token refresh when expired
    # - Vertex AI URL construction
    client = MistralGCP(
        project_id=GCP_PROJECT_ID,
        region=GCP_REGION,
    )

    chat_response = await client.chat.complete_async(
        model=GCP_MODEL,
        messages=[UserMessage(content="What is the best French cheese?")],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
