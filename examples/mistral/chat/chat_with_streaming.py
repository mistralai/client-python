#!/usr/bin/env python

import os

from mistralai import Mistral
from mistralai.models import UserMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    for chunk in client.chat.stream(
        model=model,
        messages=[UserMessage(content="What is the best French cheese?")],
    ):
        print(chunk.data.choices[0].delta.content, end="")


if __name__ == "__main__":
    main()
