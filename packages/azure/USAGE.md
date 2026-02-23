<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai.azure.client import MistralAzure
import httpx
import os

s = MistralAzure(
    api_key=os.environ["AZURE_API_KEY"],
    server_url=os.environ["AZURE_ENDPOINT"],
    client=httpx.Client(
        follow_redirects=True,
        params={"api-version": os.environ["AZURE_API_VERSION"]},
    ),
)


res = s.chat.complete(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model=os.environ["AZURE_MODEL"])

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai.azure.client import MistralAzure
import httpx
import os

async def main():
    s = MistralAzure(
        api_key=os.environ["AZURE_API_KEY"],
        server_url=os.environ["AZURE_ENDPOINT"],
        async_client=httpx.AsyncClient(
            follow_redirects=True,
            params={"api-version": os.environ["AZURE_API_VERSION"]},
        ),
    )
    res = await s.chat.complete_async(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], model=os.environ["AZURE_MODEL"])
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->
