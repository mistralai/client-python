
# Migration Guide for MistralAI Client from 0.\*.\* to 1.0.0

We have made significant changes to the `mistralai` library to improve its usability and consistency. This guide will help you migrate your code from the old client to the new one.

## Major Changes

1. **Unified Client Class**:
   - The `MistralClient` and `MistralAsyncClient` classes have been consolidated into a single `Mistral` class.
   - This simplifies the API by providing a single entry point for both synchronous and asynchronous operations.

2. **Method Names and Structure**:
   - The method names and structure have been updated for better clarity and consistency.
   - For example:
      - `client.chat` is now `client.chat.complete` for non-streaming calls
      - `client.chat_stream` is now `client.chat.stream` for streaming calls
      - Async `client.chat` is now `client.chat.complete_async` for async non-streaming calls
      - Async `client.chat_stream` is now `client.chat.stream_async` for async streaming calls


## Method changes

### Sync

| Old Methods                | New Methods                      |
| -------------------------- | -------------------------------- |
| `MistralCLient`            | `Mistral`                        |
| `client.chat`              | `client.chat.complete`           |
| `client.chat_stream`       | `client.chat.stream`             |
| `client.completions`       | `client.fim.complete`            |
| `client.completions_strem` | `client.fim.stream`              |
| `client.embeddings`        | `client.embeddings.create`       |
| `client.list_models`       | `client.models.list`             |
| `client.delete_model`      | `client.models.delete`           |
| `client.files.create`      | `client.files.upload`            |
| `client.files.list`        | `client.files.list`              |
| `client.files.retrieve`    | `client.files.retrieve`          |
| `client.files.delete`      | `client.files.delete`            |
| `client.jobs.create`       | `client.fine_tuning.jobs.create` |
| `client.jobs.list`         | `client.fine_tuning.jobs.list`   |
| `client.jobs.retrieve`     | `client.fine_tuning.jobs.get`    |
| `client.jobs.cancel`       | `client.fine_tuning.jobs.cancel` |

### Async

| Old Methods                      | New Methods                            |
| -------------------------------- | -------------------------------------- |
| `MistralAsyncClient`             | `Mistral`                              |
| `async_client.chat`              | `client.chat.complete_async`           |
| `async_client.chat_stream`       | `client.chat.stream_async`             |
| `async_client.completions`       | `client.fim.complete_async`            |
| `async_client.completions_strem` | `client.fim.stream_async`              |
| `async_client.embeddings`        | `client.embeddings.create_async`       |
| `async_client.list_models`       | `client.models.list_async`             |
| `async_client.delete_model`      | `client.models.delete_async`           |
| `async_client.files.create`      | `client.files.upload_async`            |
| `async_client.files.list`        | `client.files.list_async`              |
| `async_client.files.retrieve`    | `client.files.retrieve_async`          |
| `async_client.files.delete`      | `client.files.delete_async`            |
| `async_client.jobs.create`       | `client.fine_tuning.jobs.create_async` |
| `async_client.jobs.list`         | `client.fine_tuning.jobs.list_async`   |
| `async_client.jobs.retrieve`     | `client.fine_tuning.jobs.get_async`    |
| `async_client.jobs.cancel`       | `client.fine_tuning.jobs.cancel_async` |

### Message Changes

The `ChatMessage` class has been replaced with a more flexible system. You can now use the `SystemMessage`, `UserMessage`, `AssistantMessage`, and `ToolMessage` classes to create messages.

The return object of the stream call methods have been modified to `chunk.data.choices[0].delta.content` from `chunk.choices[0].delta.content`. 

## Example Migrations

### Example 1: Non-Streaming Chat

**Old:**
```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)
```

**New:**

```python
import os

from mistralai import Mistral, UserMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

messages = [
    {
        "role": "user",
        "content": "What is the best French cheese?",
    },
]
# Or using the new message classes
# messages = [
#     UserMessage(content="What is the best French cheese?"),
# ]

chat_response = client.chat.complete(
    model=model,
    messages=messages,
)

print(chat_response.choices[0].message.content)
```

### Example 2: Streaming Chat

**Old:**

```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# With streaming
stream_response = client.chat_stream(model=model, messages=messages)

for chunk in stream_response:
    print(chunk.choices[0].delta.content)
```
**New:**
```python
import os

from mistralai import Mistral, UserMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

messages = [
    {
        "role": "user",
        "content": "What is the best French cheese?",
    },
]
# Or using the new message classes
# messages = [
#     UserMessage(content="What is the best French cheese?"),
# ]

stream_response = client.chat.stream(
    model=model,
    messages=messages,
)

for chunk in stream_response:
    print(chunk.data.choices[0].delta.content)

```

### Example 3: Async

**Old:**
```python
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralAsyncClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# With async
async_response = client.chat_stream(model=model, messages=messages)

async for chunk in async_response:
    print(chunk.choices[0].delta.content)
```

**New:**
```python
import asyncio
import os

from mistralai import Mistral, UserMessage


async def main():
    client = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )

    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
    # Or using the new message classes
    # messages = [
    #     UserMessage(
    #         content="What is the best French cheese?",
    #     ),
    # ]
    async_response = await client.chat.stream_async(
        messages=messages,
        model="mistral-large-latest",
    )

    async for chunk in async_response:
        print(chunk.data.choices[0].delta.content)


asyncio.run(main())
```
