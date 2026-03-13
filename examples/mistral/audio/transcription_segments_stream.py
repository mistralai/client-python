#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.transcriptions import CompleteAcceptEnum


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-mini-latest"

    client = Mistral(api_key=api_key)
    response = client.audio.transcriptions.complete(
        model=model,
        file_url="https://docs.mistral.ai/audio/bcn_weather.mp3",
        timestamp_granularities=["segment"],
        accept_header_override=CompleteAcceptEnum.TEXT_EVENT_STREAM,
    )
    for chunk in response:
        print(chunk)


if __name__ == "__main__":
    main()
