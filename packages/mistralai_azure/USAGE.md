<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.complete(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai_azure import MistralAzure
import os

async def main():
    s = MistralAzure(
        azure_api_key=os.getenv("AZURE_API_KEY", ""),
        azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
    )
    res = await s.chat.complete_async(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], model="azureai")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->