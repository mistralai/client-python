import asyncio
import os

from mistralai.async_client import MistralAsyncClient


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralAsyncClient(api_key=api_key)

    list_models_response = await client.list_models()
    print(list_models_response)


if __name__ == "__main__":
    asyncio.run(main())
