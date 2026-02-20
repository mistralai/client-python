#!/usr/bin/env python

import asyncio
import os

from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.models.usermessage import UserMessage


async def main():
    model = "mistral-large-2407"

    client = MistralGCP(api_key=os.environ["GCP_API_KEY"])

    chat_response = await client.chat.complete_async(
        model=model,
        messages=[UserMessage(content="What is the best French cheese?")],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
