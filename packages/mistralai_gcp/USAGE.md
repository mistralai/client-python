<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai_gcp import MistralGCP
import os

s = MistralGCP()


res = s.chat.complete(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="mistral-small-latest")

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai_gcp import MistralGCP
import os

async def main():
    s = MistralGCP(
        api_key=os.getenv("API_KEY", ""),
    )
    res = await s.chat.complete_async(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], model="mistral-small-latest")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->