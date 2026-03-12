<!-- Start SDK Example Usage [usage] -->
### Create Chat Completions

This example shows how to create chat completions.

The SDK automatically:
- Detects credentials via `google.auth.default()`
- Auto-refreshes tokens when they expire
- Builds the Vertex AI URL from `project_id` and `region`

```python
# Synchronous Example
import os
from mistralai.gcp.client import MistralGCP

# The SDK auto-detects credentials and builds the Vertex AI URL
s = MistralGCP(
    project_id=os.environ.get("GCP_PROJECT_ID"),  # Optional: auto-detected from credentials
    region=os.environ.get("GCP_REGION", "us-central1"),
)

res = s.chat.complete(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model="mistral-small-2503")

if res is not None:
    # handle response
    print(res.choices[0].message.content)
```

<br/>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
from mistralai.gcp.client import MistralGCP

async def main():
    # The SDK auto-detects credentials and builds the Vertex AI URL
    s = MistralGCP(
        project_id=os.environ.get("GCP_PROJECT_ID"),  # Optional: auto-detected
        region=os.environ.get("GCP_REGION", "us-central1"),
    )
    res = await s.chat.complete_async(messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], model="mistral-small-2503")
    if res is not None:
        # handle response
        print(res.choices[0].message.content)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->
