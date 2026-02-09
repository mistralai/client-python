#!/usr/bin/env python

import os
import asyncio

from mistralai.client import Mistral
from mistralai.client.models import File


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # create new library
    library = await client.beta.libraries.create_async(name="My API Library")
    print(library)

    # Upload a new file
    uploaded_file = await client.beta.libraries.documents.upload_async(
        library_id=library.id,
        file=File(
            file_name="lorem_ipsum.md",
            content=open("examples/fixtures/lorem_ipsum.md", "rb").read(),
        )
    )
    print(uploaded_file)

    # List files
    files = (await client.beta.libraries.documents.list_async(library_id=library.id)).data
    print(files)

    # Retrieve a file
    retrieved_file = await  client.beta.libraries.documents.get_async(library_id=library.id, document_id=uploaded_file.id)
    print(retrieved_file)

    # Retrieve a file content
    retrieved_file_content = await client.beta.libraries.documents.text_content_async(library_id=library.id, document_id=uploaded_file.id)
    print(retrieved_file_content)


    # Rename a file
    renamed_file = await client.beta.libraries.documents.update_async(library_id=library.id, document_id=uploaded_file.id, name="renamed_file.md")
    print(renamed_file)

    # Delete a file
    deleted_file = await client.beta.libraries.documents.delete_async(library_id=library.id, document_id=uploaded_file.id)
    print(deleted_file)

    # Delete a library
    deleted_library = await client.beta.libraries.delete_async(library_id=library.id)
    print(deleted_library)



if __name__ == "__main__":
    asyncio.run(main())
