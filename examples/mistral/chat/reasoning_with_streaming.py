#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import TextChunk, ThinkChunk, UserMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-medium-3-5"

    # Bump request timeout because reasoning runs can be long.
    client = Mistral(api_key=api_key, timeout_ms=300_000)

    # While the model is thinking, delta.content is a list containing a
    # ThinkChunk. After the thinking phase ends, delta.content arrives as
    # plain string fragments. The transition event may contain both a closing
    # ThinkChunk and the first TextChunk in a single list.
    in_thinking = False
    for event in client.chat.stream(
        model=model,
        messages=[
            UserMessage(
                content=(
                    "If a train leaves Paris at 9am going 120 km/h and another "
                    "leaves Lyon at 10am going 150 km/h on the same track, "
                    "when do they meet? Paris-Lyon is 465 km."
                )
            )
        ],
        reasoning_effort="high",
        temperature=0.7,
    ):
        delta = event.data.choices[0].delta.content
        if not delta:
            continue

        if isinstance(delta, str):
            if in_thinking:
                print("\n--- /thinking ---")
                in_thinking = False
            print(delta, end="", flush=True)
            continue

        for chunk in delta:
            if isinstance(chunk, ThinkChunk):
                if not in_thinking:
                    print("--- thinking ---")
                    in_thinking = True
                for inner in chunk.thinking:
                    if isinstance(inner, TextChunk):
                        print(inner.text, end="", flush=True)
            elif isinstance(chunk, TextChunk):
                if in_thinking:
                    print("\n--- /thinking ---")
                    in_thinking = False
                print(chunk.text, end="", flush=True)

    print()


if __name__ == "__main__":
    main()
