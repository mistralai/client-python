#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import UserMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            UserMessage(
                content="What is the best French cheese? Answer shortly in JSON.",
            )
        ],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
