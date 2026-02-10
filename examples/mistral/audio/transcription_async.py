#!/usr/bin/env python

import os
import asyncio
from mistralai.client import Mistral, File


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-mini-latest"

    client = Mistral(api_key=api_key)
    with open("examples/fixtures/bcn_weather.mp3", "rb") as f:
        response = await client.audio.transcriptions.complete_async(
            model=model,
            file=File(content=f, file_name=f.name),
        )
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
