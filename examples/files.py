#!/usr/bin/env python

import os

from mistralai.client import MistralClient


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = MistralClient(api_key=api_key)

    # Create a new file
    created_file = client.files.create(file=("training_file.jsonl", open("examples/file.jsonl", "rb").read()))
    print(created_file)

    # List files
    files = client.files.list()
    print(files)

    # Retrieve a file
    retrieved_file = client.files.retrieve(created_file.id)
    print(retrieved_file)

    # Delete a file
    deleted_file = client.files.delete(created_file.id)
    print(deleted_file)


if __name__ == "__main__":
    main()
