import os

from mistral_client.client import MistralClient
from mistral_client.models.chat_completion import ChatMessage


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    ### LIST MODELS
    list_models_response = client.list_models()
    print(list_models_response)


    ### CHAT NO STREAMING
    chat_response = client.chat(
        model="le-tiny",
        messages=[ChatMessage(role="user", content="Hello, how are you?")],
    )

    print(chat_response)

    ### CHAT STREAMING
    for chunk in client.chat_stream(
        model="le-tiny",
        messages=[ChatMessage(role="user", content="Hello, how are you?")],
    ):
        print(chunk)

    ### EMBEDDINGS
    embeddings_response = client.embeddings(
        model="le-embed",
        input="Hello, how are you?",
    )

    print(embeddings_response)

    ### EMBEDDINGS BATCH
    embeddings_batch_response = client.embeddings(
        model="le-embed",
        input=["Hello, how are you?"] * 10,
    )

    print(embeddings_batch_response)



if __name__ == "__main__":
    main()
