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
                        "image_url": "https://raw.githubusercontent.com/mistralai/mistral-common/7edf6f651b3579135f44686e345d51b7e19a536a/docs/assets/logo_favicon.png",
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
