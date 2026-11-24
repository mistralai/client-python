#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral
from mistralai.client.models import File


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Create a new file
    created_file = await client.files.upload_async(
        file=File(
            file_name="batch_file.jsonl",
            # One Batch API request per line: a custom_id and the request body.
            content=b'{"custom_id": "0", "body": {"messages": [{"role": "user", "content": "What is the best French cheese?"}]}}\n',
        ),
        purpose="batch",
    )
    print(created_file)

    # List files
    files = await client.files.list_async()
    print(files)

    # Retrieve a file
    retrieved_file = await client.files.retrieve_async(file_id=created_file.id)
    print(retrieved_file)

    # Delete a file
    deleted_file = await client.files.delete_async(file_id=created_file.id)
    print(deleted_file)


if __name__ == "__main__":
    asyncio.run(main())
