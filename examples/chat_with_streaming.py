#!/usr/bin/env python

import os

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = MistralClient(api_key=api_key)

    for chunk in client.chat_stream(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
    ):
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


if __name__ == "__main__":
    main()
