#!/usr/bin/env python

import asyncio
import os

from mistralai.client import Mistral
from mistralai.client.models import UserMessage

MODEL = "mistral-medium-latest"


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    # Create a fresh agent for this run to avoid version accumulation
    agent = client.beta.agents.create(
        model=MODEL,
        name="cheese-expert-example",
        instructions="You are a helpful assistant.",
    )

    try:
        chat_response = await client.agents.complete_async(
            agent_id=agent.id,
            messages=[UserMessage(content="What is the best French cheese?")],
            timeout_ms=120000,
        )

        print(chat_response.choices[0].message.content)
    finally:
        client.beta.agents.delete(agent_id=agent.id)


if __name__ == "__main__":
    asyncio.run(main())
