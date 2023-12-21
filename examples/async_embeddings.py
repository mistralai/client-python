#!/usr/bin/env python

import asyncio
import os

from mistralai.async_client import MistralAsyncClient


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralAsyncClient(api_key=api_key)

    embeddings_batch_response = await client.embeddings(
        model="mistral-embed",
        input=["What is the best French cheese?"] * 10,
    )
    print(embeddings_batch_response)


if __name__ == "__main__":
    asyncio.run(main())
