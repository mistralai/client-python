<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ])

    assert res is not None

    # Handle response
    print(res)
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
    ) as mistral:

        res = await mistral.chat.complete_async(model="mistral-small-latest", messages=[
            {
                "content": "Who is the best French painter? Answer in one short sentence.",
                "role": "user",
            },
        ])

        assert res is not None

        # Handle response
        print(res)

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
) as mistral:

    res = mistral.files.upload(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    })

    assert res is not None

    # Handle response
    print(res)
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
    ) as mistral:

        res = await mistral.files.upload_async(file={
            "file_name": "example.file",
            "content": open("example.file", "rb"),
        })

        assert res is not None

        # Handle response
        print(res)

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
) as mistral:

    res = mistral.agents.complete(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], agent_id="<value>")

    assert res is not None

    # Handle response
    print(res)
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
    ) as mistral:

        res = await mistral.agents.complete_async(messages=[
            {
                "content": "Who is the best French painter? Answer in one short sentence.",
                "role": "user",
            },
        ], agent_id="<value>")

        assert res is not None

        # Handle response
        print(res)

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
) as mistral:

    res = mistral.embeddings.create(inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ], model="Wrangler")

    assert res is not None

    # Handle response
    print(res)
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
    ) as mistral:

        res = await mistral.embeddings.create_async(inputs=[
            "Embed this sentence.",
            "As well as this one.",
        ], model="Wrangler")

        assert res is not None

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->