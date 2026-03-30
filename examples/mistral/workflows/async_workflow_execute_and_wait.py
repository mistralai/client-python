#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral

WORKFLOW_NAME = "example-hello-world-workflow"


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Example 1: Using API sync mode (server-side waiting)
    result = await client.workflows.execute_workflow_and_wait_async(
        workflow_identifier=WORKFLOW_NAME,
        input={"document_title": "hello world"},
        use_api_sync=True,
        timeout_seconds=60.0,
    )
    print(f"Result (API sync): {result}")

    # Example 2: Using polling mode (client-side waiting)
    result = await client.workflows.execute_workflow_and_wait_async(
        workflow_identifier=WORKFLOW_NAME,
        input={"document_title": "hello world"},
        use_api_sync=False,
        polling_interval=5,
        max_attempts=12,  # 12 attempts * 5 seconds = 60 seconds max
    )
    print(f"Result (polling): {result}")


if __name__ == "__main__":
    asyncio.run(main())
