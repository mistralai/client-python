#!/usr/bin/env python

import os

from mistralai.client import Mistral
from mistralai.client.models import File


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # create new library
    library = client.beta.libraries.create(name="My API Library")
    print(library)

    # Upload a new file
    uploaded_file = client.beta.libraries.documents.upload(
        library_id=library.id,
        file=File(
            file_name="lorem_ipsum.md",
            content=open("examples/fixtures/lorem_ipsum.md", "rb").read(),
        )
    )
    print(uploaded_file)

    # List files
    files = client.beta.libraries.documents.list(library_id=library.id).data
    print(files)

    # Retrieve a file
    retrieved_file = client.beta.libraries.documents.get(library_id=library.id, document_id=uploaded_file.id)
    print(retrieved_file)

    # Retrieve a file content
    retrieved_file_content = client.beta.libraries.documents.text_content(library_id=library.id, document_id=uploaded_file.id)
    print(retrieved_file_content)


    # Rename a file
    renamed_file = client.beta.libraries.documents.update(library_id=library.id, document_id=uploaded_file.id, name="renamed_file.md")
    print(renamed_file)

    # Delete a file
    deleted_file = client.beta.libraries.documents.delete(library_id=library.id, document_id=uploaded_file.id)
    print(deleted_file)

    # Delete a library
    deleted_library = client.beta.libraries.delete(library_id=library.id)
    print(deleted_library)



if __name__ == "__main__":
    main()
