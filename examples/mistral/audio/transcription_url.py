#!/usr/bin/env python

import os

from mistralai import Mistral


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-mini-latest"

    client = Mistral(api_key=api_key)
    response = client.audio.transcriptions.complete(
        model=model,
        file_url="https://docs.mistral.ai/audio/bcn_weather.mp3",
    )
    print(response.text)


if __name__ == "__main__":
    main()
