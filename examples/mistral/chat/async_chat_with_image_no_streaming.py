#!/usr/bin/env python

import asyncio
import os


from mistralai.client import Mistral
from mistralai.client.models import UserMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "pixtral-12b-2409"
    client = Mistral(api_key=api_key)

    chat_response = await client.chat.complete_async(
        model=model,
        messages=[
            UserMessage(
                content=[
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": "https://mistral.ai/_astro/ai-app_Z2q9iqE.webp?dpl=6a57bb9ad483ec680851599b",
                    },
                ]
            )
        ],
    )

    if chat_response.choices:
        message = chat_response.choices[0].message
        if message is not None:
            print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
