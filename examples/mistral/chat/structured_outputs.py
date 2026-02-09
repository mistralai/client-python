#!/usr/bin/env python

import os
from pydantic import BaseModel

from mistralai.client import Mistral


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    class Explanation(BaseModel):
        explanation: str
        output: str

    class MathDemonstration(BaseModel):
        steps: list[Explanation]
        final_answer: str

    print("Using the .parse method to parse the response into a Pydantic model:\n")
    chat_response = client.chat.parse(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. You will be provided with a math problem, and your goal will be to output a step by step solution, along with a final answer. For each step, just provide the output as an equation use the explanation field to detail the reasoning.",
            },
            {"role": "user", "content": "How can I solve 8x + 7 = -23"},
        ],
        response_format=MathDemonstration,
    )
    print(chat_response.choices[0].message.parsed)

    # Or with the streaming API
    print(
        "\nUsing the .parse_stream method to stream back the response into a JSON Schema:\n"
    )
    with client.chat.parse_stream(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. You will be provided with a math problem, and your goal will be to output a step by step solution, along with a final answer. For each step, just provide the output as an equation use the explanation field to detail the reasoning.",
            },
            {"role": "user", "content": "How can I solve 8x + 7 = -23"},
        ],
        response_format=MathDemonstration,
    ) as stream:
        for chunk in stream:
            print(chunk.data.choices[0].delta.content, end="")


if __name__ == "__main__":
    main()
