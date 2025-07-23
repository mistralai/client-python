#!/usr/bin/env python

import os

from mistralai import Mistral, File
from mistralai.models import UserMessage



def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "voxtral-small-latest"

    client = Mistral(api_key=api_key)
    with open("examples/fixtures/bcn_weather.mp3", "rb") as f:
        file = client.files.upload(file=File(content=f, file_name=f.name), purpose="audio")
        print(f"Uploaded audio file, id={file.id}")
        signed_url = client.files.get_signed_url(file_id=file.id)
    try:
        chat_response = client.chat.stream(
            model=model,
            messages=[UserMessage(content=[
                {"type": "text", "text": "What is this audio about?"},
                {
                    "type": "input_audio",
                    "input_audio": signed_url.url,
                },
            ])],
        )
        for chunk in chat_response:
            print(chunk.data.choices[0].delta.content)
    finally:
        client.files.delete(file_id=file.id)
        print(f"Deleted audio file, id={file.id}")

if __name__ == "__main__":
    main()
