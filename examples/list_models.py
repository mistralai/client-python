import os

from mimstralai.client import MistralClient


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    list_models_response = client.list_models()
    print(list_models_response)


if __name__ == "__main__":
    main()
