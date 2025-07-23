#!/usr/bin/env python

import os

from mistralai import Mistral


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    embeddings_response = client.embeddings.create(
        model="mistral-embed",
        inputs=["What is the best French cheese?"] * 10,
    )

    print(embeddings_response)


if __name__ == "__main__":
    main()
