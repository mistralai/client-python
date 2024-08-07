#!/usr/bin/env python

import asyncio
import os

from mistralai import Mistral
from mistralai.models import UserMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = Mistral(api_key=api_key)

    print("Chat response:")
    response = await client.chat.stream_async(
        model=model,
        messages=[
            UserMessage(content="What is the best French cheese?give the best 50")
        ],
    )
    async for chunk in response:
        if chunk.data.choices[0].delta.content is not None:
            print(chunk.data.choices[0].delta.content, end="")

    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
