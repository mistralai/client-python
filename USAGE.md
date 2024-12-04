<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as s:
    res = s.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ])

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as s:
        res = await s.chat.complete_async(model="mistral-small-latest", messages=[
            {
                "content": "Who is the best French painter? Answer in one short sentence.",
                "role": "user",
            },
        ])

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```

### Upload a file

This example shows how to upload a file.

```python
# Synchronous Example
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as s:
    res = s.files.upload(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    })

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as s:
        res = await s.files.upload_async(file={
            "file_name": "example.file",
            "content": open("example.file", "rb"),
        })

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```

### Create Agents Completions

This example shows how to create agents completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as s:
    res = s.agents.complete(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], agent_id="<value>")

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as s:
        res = await s.agents.complete_async(messages=[
            {
                "content": "Who is the best French painter? Answer in one short sentence.",
                "role": "user",
            },
        ], agent_id="<value>")

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```

### Create Embedding Request

This example shows how to create embedding request.

```python
# Synchronous Example
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as s:
    res = s.embeddings.create(inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ], model="Wrangler")

    if res is not None:
        # handle response
        pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as s:
        res = await s.embeddings.create_async(inputs=[
            "Embed this sentence.",
            "As well as this one.",
        ], model="Wrangler")

        if res is not None:
            # handle response
            pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->