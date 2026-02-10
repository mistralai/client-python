#!/usr/bin/env python
import asyncio
import os

from mistralai.client import Mistral
from mistralai.extra.run.context import RunContext
from mistralai.client.types import BaseModel

MODEL = "mistral-medium-2505"


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    class MathResult(BaseModel):
        answer: int

    async with RunContext(model=MODEL, output_format=MathResult) as run_ctx:
        run_result = await client.beta.conversations.run_async(
            run_ctx=run_ctx,
            inputs=[{"role": "user", "content": "What is 2 + 2?"}],
        )
        print(f"Result: {run_result.output_as_model}")


if __name__ == "__main__":
    asyncio.run(main())
