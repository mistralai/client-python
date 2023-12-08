import asyncio
import os

from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage


async def main():

    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralAsyncClient(api_key=api_key)

    ### LIST MODELS
    list_models_response = await client.list_models()
    print(list_models_response)


    ### CHAT NO STREAMING
    chat_response =  await client.chat(
        model="le-tiny",
        messages=[ChatMessage(role="user", content="Hello, how are you?")],
    )

    print(chat_response)

    ### CHAT STREAMING
    async for chunk in client.chat_stream(
        model="le-tiny",
        messages=[ChatMessage(role="user", content="Hello, how are you?")],
    ):
        print(chunk)

    ### EMBEDDINGS
    embeddings_response = await client.embeddings(
        model="le-embed",
        input="Hello, how are you?",
    )

    print(embeddings_response)

    ### EMBEDDINGS BATCH
    embeddings_batch_response = await client.embeddings(
        model="le-embed",
        input=["Hello, how are you?"] * 10,
    )

    print(embeddings_batch_response)


if __name__ == "__main__":
    asyncio.run(main())
