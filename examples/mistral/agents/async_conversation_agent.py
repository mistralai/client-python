#!/usr/bin/env python
import asyncio
import os

from mistralai import Mistral

MODEL = "mistral-medium-latest"


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    agent = client.beta.agents.create(
        model=MODEL,
        name="WebSearch Agent",
        instructions="Use your websearch abilities when answering requests you don't know.",
        description="Agent able to fetch new information on the web.",
        tools = [{"type": "web_search"}],
    )

    result = await client.beta.conversations.start_async(
        agent_id=agent.id,
        inputs="Who won the last Champions League?"
    )

    print("All result entries:")
    for entry in result.outputs:
        print(f"{entry}")

    result = await client.beta.conversations.append_async(
        conversation_id=result.conversation_id,
        inputs="And what about the previous year?"
    )

    print("All result entries:")
    for entry in result.outputs:
        print(f"{entry}")



if __name__ == "__main__":
    asyncio.run(main())
