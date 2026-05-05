#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import TextChunk, ThinkChunk, UserMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-medium-3-5"

    # Bump request timeout because reasoning runs can be long.
    client = Mistral(api_key=api_key, timeout_ms=300_000)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            UserMessage(
                content=(
                    "John is one of 4 children. The first sister is 4 years old. "
                    "Next year, the second sister will be twice as old as the first sister. "
                    "The third sister is two years older than the second sister. "
                    "The third sister is half the age of her older brother. "
                    "How old is John?"
                )
            )
        ],
        reasoning_effort="high",
        temperature=0.7,
    )

    # With reasoning_effort="high", message.content is a list of chunks.
    # With reasoning_effort="none", message.content is a plain string.
    content = chat_response.choices[0].message.content
    if isinstance(content, str):
        print(content)
        return

    for chunk in content or []:
        if isinstance(chunk, ThinkChunk):
            print("--- thinking ---")
            for inner in chunk.thinking:
                if isinstance(inner, TextChunk):
                    print(inner.text)
            print("--- /thinking ---")
        elif isinstance(chunk, TextChunk):
            print(chunk.text)


if __name__ == "__main__":
    main()
