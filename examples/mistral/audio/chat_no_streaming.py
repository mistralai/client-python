#!/usr/bin/env python

import os

from mistralai import Mistral
from mistralai.models import UserMessage



def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-small-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[UserMessage(content=[
            {"type": "text", "text": "What is this audio about?"},
            {
                "type": "input_audio",
                "input_audio": "https://docs.mistral.ai/audio/bcn_weather.mp3",
            },
        ])],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
