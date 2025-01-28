#!/usr/bin/env python

import asyncio
import os


from mistralai import Mistral
from mistralai.models import UserMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "pixtral-12b"
    client = Mistral(api_key=api_key)

    chat_response = await client.chat.complete_async(
        model=model,
        messages=[
            UserMessage(
                content=[
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": "https://mistral.ai/images/news/codestral/FIM_table.png",
                    },
                ]
            )
        ],
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
