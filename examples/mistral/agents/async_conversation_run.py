#!/usr/bin/env python
import asyncio
import os

from mistralai.client import Mistral
from mistralai.extra.run.context import RunContext
from mistralai.client.types import BaseModel

MODEL = "mistral-medium-2505"


def math_question_generator(question_num: int):
    """Random generator of mathematical question

    Args:
        question_num (int): the number of the question that will be returned, should be between 1-100
    """
    return (
        "solve the following differential equation: `y'' + 3y' + 2y = 0`"
        if question_num % 2 == 0
        else "solve the following differential equation: `y'' - 4y' + 4y = e^x`"
    )


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    class Explanation(BaseModel):
        explanation: str
        output: str

    class MathDemonstration(BaseModel):
        steps: list[Explanation]
        final_answer: str

    async with RunContext(model=MODEL, output_format=MathDemonstration) as run_ctx:
        # register a new function that can be executed on the client side
        run_ctx.register_func(math_question_generator)
        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            instructions="Use the code interpreter to help you when asked mathematical questions.",
            inputs=[
                {"role": "user", "content": "hey"},
                {"role": "assistant", "content": "hello"},
                {"role": "user", "content": "Request a math question and answer it."},
            ],
            tools=[{"type": "code_interpreter"}],
        )
        print("All run entries:")
        for entry in run_result.output_entries:
            print(f"{entry}")
        print(f"Final model: {run_result.output_as_model}")


if __name__ == "__main__":
    asyncio.run(main())
