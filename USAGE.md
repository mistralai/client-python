<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.chat.complete(model="mistral-small-latest", messages=[

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
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.chat.complete_async(model="mistral-small-latest", messages=[

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

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

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
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
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

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.agents.complete(messages=[
    {
        "content": "<value>",
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
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.agents.complete_async(messages=[
        {
            "content": "<value>",
        },
    ], agent_id="<value>")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->