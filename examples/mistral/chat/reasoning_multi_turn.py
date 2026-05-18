#!/usr/bin/env python

# Multi-turn conversation with a reasoning model.
#
# IMPORTANT: for Mistral Medium 3.5, always replay the assistant turn
# back into `messages` with its ThinkChunks intact. Dropping the
# reasoning trace across turns DEGRADES the model's performance.
#
# This example runs a 3-turn math chain and prints per-turn token
# usage. The prompt grows as the reasoning trace accumulates; that
# growth is expected.

import os

from mistralai.client import Mistral
from mistralai.client.models import TextChunk, UserMessage

MODEL = "mistral-medium-3-5"
TURNS = [
    "What is 17 * 23?",
    "Now multiply that by 3.",
    "And subtract 100 from the result.",
]


def final_text(content):
    if isinstance(content, str):
        return content
    return "".join(c.text for c in (content or []) if isinstance(c, TextChunk))


def main():
    # Bump request timeout because reasoning runs can be long.
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"], timeout_ms=300_000)

    messages = []
    total_prompt = 0
    total_completion = 0

    for i, user_text in enumerate(TURNS, start=1):
        messages.append(UserMessage(content=user_text))
        response = client.chat.complete(
            model=MODEL,
            messages=messages,
            reasoning_effort="high",
            temperature=0.7,
        )
        message = response.choices[0].message
        usage = response.usage
        total_prompt += usage.prompt_tokens
        total_completion += usage.completion_tokens

        print(
            f"turn {i}: prompt={usage.prompt_tokens:>4} "
            f"completion={usage.completion_tokens:>4}  -> {final_text(message.content)}"
        )
        # Append the full assistant message back into history so the
        # ThinkChunks are preserved across turns.
        messages.append(message)

    print(
        f"TOTAL: prompt={total_prompt} completion={total_completion} "
        f"(sum {total_prompt + total_completion})"
    )


if __name__ == "__main__":
    main()
