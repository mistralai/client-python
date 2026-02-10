#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    list_models_response = await client.models.list_async()
    print(list_models_response)


if __name__ == "__main__":
    asyncio.run(main())
