#!/usr/bin/env python

import os

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = MistralClient(api_key=api_key)

    chat_response = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],

    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
