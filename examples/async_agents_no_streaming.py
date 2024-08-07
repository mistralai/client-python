#!/usr/bin/env python

import asyncio
import os

from mistralai import Mistral
from mistralai.models import UserMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    chat_response = await client.agents.complete_async(
        agent_id="<your_agent_id>",
        messages=[UserMessage(content="What is the best French cheese?")],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
