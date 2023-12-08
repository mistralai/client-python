import os

from mistralai.client import MistralClient


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    embeddings_response = client.embeddings(
        model="mistral-embed",
        input=["What is the best French cheese?"] * 10,
    )

    print(embeddings_response)


if __name__ == "__main__":
    main()
