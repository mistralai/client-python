#!/usr/bin/env python

import asyncio
import os

from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = MistralAsyncClient(api_key=api_key)

    print("Chat response:")
    async for chunk in client.chat_stream(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
    ):
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

    print("\n")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
