#!/usr/bin/env python

# Print the raw shape of a chat response when using `reasoning_effort`.
# Run this first to see what ThinkChunk / TextChunk look like in the wire
# format, then move on to the other reasoning_*.py examples.

import json
import os

from mistralai.client import Mistral
from mistralai.client.models import UserMessage


def main():
    # Bump request timeout because reasoning runs can be long.
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"], timeout_ms=300_000)

    prompt = "What is 12 * 14? Answer in one short sentence."

    for effort in ["high", "none"]:
        print(f"\n========== reasoning_effort={effort!r} ==========")
        response = client.chat.complete(
            model="mistral-medium-3-5",
            messages=[UserMessage(content=prompt)],
            reasoning_effort=effort,
            temperature=0.7,
        )
        message = response.choices[0].message
        print(f"type(message.content) = {type(message.content).__name__}")
        print("message.content =")
        if isinstance(message.content, str):
            print(json.dumps(message.content, indent=2))
        else:
            print(
                json.dumps(
                    [chunk.model_dump() for chunk in message.content],
                    indent=2,
                )
            )


if __name__ == "__main__":
    main()
