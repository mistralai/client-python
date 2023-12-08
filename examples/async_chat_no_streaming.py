import asyncio
import os

from mistral_client.async_client import MistralAsyncClient
from mistral_client.models.chat_completion import ChatMessage


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = MistralAsyncClient(api_key=api_key)

    chat_response = await client.chat(
        model=model,
        messages=[ChatMessage(role="user", content="What is the best French cheese?")],
    )
    print(chat_response)


if __name__ == "__main__":
    asyncio.run(main())
