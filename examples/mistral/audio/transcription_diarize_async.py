#!/usr/bin/env python

import os
import asyncio
import pathlib
from mistralai import Mistral, File

fixture_dir = pathlib.Path(__file__).parents[2] / "fixtures"

async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-mini-2602"

    client = Mistral(api_key=api_key)
    with open(fixture_dir / "bcn_weather.mp3", "rb") as f:
        response = await client.audio.transcriptions.complete_async(
            model=model,
            file=File(content=f, file_name=f.name),
            diarize=True,
            timestamp_granularities=["segment"],
        )
        for segment in response.segments:
            speaker = segment.speaker_id or "unknown"
            print(
                f"[{segment.start:.1f}s → {segment.end:.1f}s] {speaker}: {segment.text.strip()}"
            )


if __name__ == "__main__":
    asyncio.run(main())
