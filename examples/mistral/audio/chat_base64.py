#!/usr/bin/env python
import base64
import os

from mistralai import Mistral
from mistralai.models import UserMessage



def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-small-latest"

    client = Mistral(api_key=api_key)
    with open("examples/fixtures/bcn_weather.mp3", "rb") as f:
        content = f.read()
    chat_response = client.chat.complete(
        model=model,
        messages=[UserMessage(content=[
            {"type": "text", "text": "What's in this audio file?"},
            {
                "type": "input_audio",
                "input_audio": base64.b64encode(content).decode('utf-8'),
            },
        ])],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
