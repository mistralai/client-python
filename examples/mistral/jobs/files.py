#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import File


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Create a new file
    created_file = client.files.upload(
        file=File(
            file_name="batch_file.jsonl",
            # One Batch API request per line: a custom_id and the request body.
            content=b'{"custom_id": "0", "body": {"messages": [{"role": "user", "content": "What is the best French cheese?"}]}}\n',
        ),
        purpose="batch",
    )
    print(created_file)

    # List files
    files = client.files.list()
    print(files)

    # Retrieve a file
    retrieved_file = client.files.retrieve(file_id=created_file.id)
    print(retrieved_file)

    # Delete a file
    deleted_file = client.files.delete(file_id=created_file.id)
    print(deleted_file)


if __name__ == "__main__":
    main()
