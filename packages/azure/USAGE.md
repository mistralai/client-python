<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

The SDK automatically injects the `api-version` query parameter.

```python
# Synchronous Example
from mistralai.azure.client import MistralAzure
import os

AZURE_API_KEY = os.environ["AZURE_API_KEY"]
AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]
AZURE_MODEL = os.environ["AZURE_MODEL"]
AZURE_API_VERSION = os.environ.get("AZURE_API_VERSION", "2024-05-01-preview")

# The SDK automatically injects api-version as a query parameter
s = MistralAzure(
    api_key=AZURE_API_KEY,
    server_url=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
)

res = s.chat.complete(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model=AZURE_MODEL)

if res is not None:
    # handle response
    print(res.choices[0].message.content)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
from mistralai.azure.client import MistralAzure

AZURE_API_KEY = os.environ["AZURE_API_KEY"]
AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"]
AZURE_MODEL = os.environ["AZURE_MODEL"]
AZURE_API_VERSION = os.environ.get("AZURE_API_VERSION", "2024-05-01-preview")

async def main():
    # The SDK automatically injects api-version as a query parameter
    s = MistralAzure(
        api_key=AZURE_API_KEY,
        server_url=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
    )
    res = await s.chat.complete_async(messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], model=AZURE_MODEL)
    if res is not None:
        # handle response
        print(res.choices[0].message.content)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->
