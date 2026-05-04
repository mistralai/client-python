#!/usr/bin/env python

# Multi-turn conversation with a reasoning model.
#
# When the assistant returns a list of chunks (ThinkChunk + TextChunk),
# you must choose what to put back into `messages` for the next turn.
# This example runs the same 3-turn math chain with two strategies and
# prints the resulting token usage so you can see the tradeoff:
#
#   A) keep ThinkChunks  -> the prompt grows fast as reasoning accumulates
#   B) drop ThinkChunks  -> only the final answer is replayed
#
# Both produce the correct answer here. Pick based on whether your task
# benefits from the model seeing its prior reasoning.

import os

import httpx

from mistralai.client import Mistral
from mistralai.client.models import (
    AssistantMessage,
    TextChunk,
    ThinkChunk,
    UserMessage,
)

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


def keep_thinking(content):
    return content


def drop_thinking(content):
    if isinstance(content, str):
        return content
    return [c for c in (content or []) if not isinstance(c, ThinkChunk)]


def run_chain(client, label, build_history):
    print(f"\n========== {label} ==========")
    messages = []
    total_prompt = 0
    total_completion = 0
    last_answer = ""

    for i, user_text in enumerate(TURNS, start=1):
        messages.append(UserMessage(content=user_text))
        response = client.chat.complete(
            model=MODEL,
            messages=messages,
            reasoning_effort="high",
            temperature=0.7,
        )
        content = response.choices[0].message.content
        usage = response.usage
        total_prompt += usage.prompt_tokens
        total_completion += usage.completion_tokens
        last_answer = final_text(content)

        print(
            f"turn {i}: prompt={usage.prompt_tokens:>4} "
            f"completion={usage.completion_tokens:>4}  -> {last_answer}"
        )
        messages.append(AssistantMessage(content=build_history(content)))

    print(
        f"TOTAL: prompt={total_prompt} completion={total_completion} "
        f"(sum {total_prompt + total_completion})"
    )


def main():
    client = Mistral(
        api_key=os.environ["MISTRAL_API_KEY"],
        client=httpx.Client(timeout=httpx.Timeout(300.0)),
    )

    run_chain(client, "A) keep ThinkChunks across turns", keep_thinking)
    run_chain(client, "B) drop ThinkChunks across turns", drop_thinking)


if __name__ == "__main__":
    main()
