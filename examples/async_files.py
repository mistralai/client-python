#!/usr/bin/env python

import asyncio
import os

from mistralai.async_client import MistralAsyncClient


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralAsyncClient(api_key=api_key)

    # Create a new file
    created_file = await client.files.create(file=open("examples/file.jsonl", "rb").read())
    print(created_file)

    # List files
    files = await client.files.list()
    print(files)

    # Retrieve a file
    retrieved_file = await client.files.retrieve(created_file.id)
    print(retrieved_file)

    # Delete a file
    deleted_file = await client.files.delete(created_file.id)
    print(deleted_file)


if __name__ == "__main__":
    asyncio.run(main())
