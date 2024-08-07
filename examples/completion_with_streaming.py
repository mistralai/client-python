#!/usr/bin/env python

import asyncio
import os

from mistralai import Mistral


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    prompt = "def fibonacci(n: int):"
    suffix = "n = int(input('Enter a number: '))\nprint(fibonacci(n))"

    print(prompt)
    for chunk in client.fim.stream(
        model="codestral-latest",
        prompt=prompt,
        suffix=suffix,
    ):
        print(chunk.data.choices[0].delta.content, end="")
    print(suffix)


if __name__ == "__main__":
    asyncio.run(main())
