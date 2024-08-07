#!/usr/bin/env python

import asyncio
import os

from mistralai_gcp import MistralGoogleCloud
from mistralai_gcp.models.usermessage import UserMessage


async def main():
    model = "mistral-large-2407"

    client = MistralGoogleCloud(project_id=os.environ["GCP_PROJECT_ID"])

    chat_response = await client.chat.complete_async(
        model=model,
        messages=[UserMessage(content="What is the best French cheese?")],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
