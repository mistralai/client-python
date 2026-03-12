#!/usr/bin/env python
import asyncio
import os

from mistralai.client import Mistral
from mistralai.client.models import File
from mistralai.client.transcriptions import CompleteAcceptEnum


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-mini-2507"

    client = Mistral(api_key=api_key)
    with open("examples/fixtures/bcn_weather.mp3", "rb") as f:
        response = await client.audio.transcriptions.complete_async(
            model=model,
            file=File(content=f, file_name=f.name),
            accept_header_override=CompleteAcceptEnum.TEXT_EVENT_STREAM,
        )
        async for chunk in response:
            print(chunk.event, chunk.data)


if __name__ == "__main__":
    asyncio.run(main())
