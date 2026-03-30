<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-large-latest", messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], stream=False, response_format={
        "type": models.ResponseFormats.TEXT,
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral, models
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "role": "user",
                "content": "Who is the best French painter? Answer in one short sentence.",
            },
        ], stream=False, response_format={
            "type": models.ResponseFormats.TEXT,
        })

        # Handle response
        print(res)

asyncio.run(main())
```

### Upload a file

This example shows how to upload a file.

```python
# Synchronous Example
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.upload(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    }, visibility=models.FilesAPIRoutesUploadFileFileVisibility.WORKSPACE)

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral, models
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.files.upload_async(file={
            "file_name": "example.file",
            "content": open("example.file", "rb"),
        }, visibility=models.FilesAPIRoutesUploadFileFileVisibility.WORKSPACE)

        # Handle response
        print(res)

asyncio.run(main())
```

### Create Agents Completions

This example shows how to create agents completions.

```python
# Synchronous Example
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.agents.complete(messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], agent_id="<id>", stream=False, response_format={
        "type": models.ResponseFormats.TEXT,
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral, models
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.agents.complete_async(messages=[
            {
                "role": "user",
                "content": "Who is the best French painter? Answer in one short sentence.",
            },
        ], agent_id="<id>", stream=False, response_format={
            "type": models.ResponseFormats.TEXT,
        })

        # Handle response
        print(res)

asyncio.run(main())
```

### Create Embedding Request

This example shows how to create embedding request.

```python
# Synchronous Example
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.embeddings.create(model="mistral-embed", inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ])

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.embeddings.create_async(model="mistral-embed", inputs=[
            "Embed this sentence.",
            "As well as this one.",
        ])

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->