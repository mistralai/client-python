#!/usr/bin/env python

import asyncio
import os
from pydantic import BaseModel

from mistralai import Mistral


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    class Explanation(BaseModel):
        explanation: str
        output: str

    class MathDemonstration(BaseModel):
        steps: list[Explanation]
        final_answer: str

    chat_response = await client.chat.parse_async(
        model="mistral-large-2411",
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


if __name__ == "__main__":
    asyncio.run(main())
