#!/usr/bin/env python

import asyncio
import os

from mistralai.client import MistralClient


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    prompt = "def fibonacci(n: int):"
    suffix = "n = int(input('Enter a number: '))\nprint(fibonacci(n))"

    print(prompt)
    for chunk in client.completion_stream(
        model="codestral-latest",
        prompt=prompt,
        suffix=suffix,
    ):
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print(suffix)


if __name__ == "__main__":
    asyncio.run(main())
