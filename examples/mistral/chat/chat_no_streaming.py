#!/usr/bin/env python

import os

from mistralai import Mistral
from mistralai.models import UserMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[UserMessage(content="What is the best French cheese?")],
    )
    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
