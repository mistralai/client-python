#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    prompt = "def fibonacci(n: int):"
    suffix = "n = int(input('Enter a number: '))\nprint(fibonacci(n))"

    response = await client.fim.complete_async(
        model="codestral-latest",
        prompt=prompt,
        suffix=suffix,
    )

    print(
        f"""
{prompt}
{response.choices[0].message.content}
{suffix}
"""
    )


if __name__ == "__main__":
    asyncio.run(main())
