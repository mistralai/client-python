# Migration Guide

This guide covers migrating between major versions of the Mistral Python SDK.

---

## Migrating from v1.x to v2.x

Version 2.0 updates the import paths from `mistralai` to `mistralai.client`.

### Import Changes

All imports move from `mistralai` to `mistralai.client`:

```python
# v1
from mistralai import Mistral
from mistralai.models import UserMessage, AssistantMessage
from mistralai.types import BaseModel

# v2
from mistralai.client import Mistral
from mistralai.client.models import UserMessage, AssistantMessage
from mistralai.client.types import BaseModel
```

### Quick Reference

| v1 | v2 |
|---|---|
| `from mistralai import Mistral` | `from mistralai.client import Mistral` |
| `from mistralai.models import ...` | `from mistralai.client.models import ...` |
| `from mistralai.types import ...` | `from mistralai.client.types import ...` |
| `from mistralai.utils import ...` | `from mistralai.client.utils import ...` |

### What Stays the Same

- The `Mistral` client API is unchanged
- All models (`UserMessage`, `AssistantMessage`, etc.) work the same way

### Type Name Changes

Some type names have been updated for clarity and consistency:

| Old Name | New Name |
|---|---|
| `Tools` | `ConversationRequestTool` |
| `ToolsTypedDict` | `ConversationRequestToolTypedDict` |
| `HandoffExecution` | `ConversationRequestHandoffExecution` |
| `AgentVersion` | `ConversationRequestAgentVersion` |

Enums now accept unknown values for forward compatibility with API changes.

---

## Migrating from v0.x to v1.x

Version 1.0 introduced significant changes to improve usability and consistency.

### Major Changes

1. **Unified Client Class**: `MistralClient` and `MistralAsyncClient` consolidated into a single `Mistral` class
2. **Method Structure**: Methods reorganized into resource-based groups (e.g., `client.chat.complete()`)
3. **Message Classes**: `ChatMessage` replaced with typed classes (`UserMessage`, `AssistantMessage`, etc.)
4. **Streaming Response**: Stream chunks now accessed via `chunk.data.choices[0].delta.content`

### Method Mapping

#### Sync Methods

| v0.x | v1.x |
|---|---|
| `MistralClient` | `Mistral` |
| `client.chat` | `client.chat.complete` |
| `client.chat_stream` | `client.chat.stream` |
| `client.completions` | `client.fim.complete` |
| `client.completions_stream` | `client.fim.stream` |
| `client.embeddings` | `client.embeddings.create` |
| `client.list_models` | `client.models.list` |
| `client.delete_model` | `client.models.delete` |
| `client.files.create` | `client.files.upload` |
| `client.jobs.create` | `client.fine_tuning.jobs.create` |
| `client.jobs.list` | `client.fine_tuning.jobs.list` |
| `client.jobs.retrieve` | `client.fine_tuning.jobs.get` |
| `client.jobs.cancel` | `client.fine_tuning.jobs.cancel` |

#### Async Methods

| v0.x | v1.x |
|---|---|
| `MistralAsyncClient` | `Mistral` |
| `async_client.chat` | `client.chat.complete_async` |
| `async_client.chat_stream` | `client.chat.stream_async` |
| `async_client.completions` | `client.fim.complete_async` |
| `async_client.completions_stream` | `client.fim.stream_async` |
| `async_client.embeddings` | `client.embeddings.create_async` |
| `async_client.list_models` | `client.models.list_async` |
| `async_client.files.create` | `client.files.upload_async` |
| `async_client.jobs.create` | `client.fine_tuning.jobs.create_async` |
| `async_client.jobs.list` | `client.fine_tuning.jobs.list_async` |
| `async_client.jobs.retrieve` | `client.fine_tuning.jobs.get_async` |
| `async_client.jobs.cancel` | `client.fine_tuning.jobs.cancel_async` |

### Example: Non-Streaming Chat

**v0.x:**
```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(api_key=api_key)

messages = [ChatMessage(role="user", content="What is the best French cheese?")]
response = client.chat(model="mistral-large-latest", messages=messages)

print(response.choices[0].message.content)
```

**v1.x:**
```python
from mistralai import Mistral, UserMessage

client = Mistral(api_key=api_key)

messages = [UserMessage(content="What is the best French cheese?")]
response = client.chat.complete(model="mistral-large-latest", messages=messages)

print(response.choices[0].message.content)
```

### Example: Streaming Chat

**v0.x:**
```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

client = MistralClient(api_key=api_key)
messages = [ChatMessage(role="user", content="What is the best French cheese?")]

for chunk in client.chat_stream(model="mistral-large-latest", messages=messages):
    print(chunk.choices[0].delta.content)
```

**v1.x:**
```python
from mistralai import Mistral, UserMessage

client = Mistral(api_key=api_key)
messages = [UserMessage(content="What is the best French cheese?")]

for chunk in client.chat.stream(model="mistral-large-latest", messages=messages):
    print(chunk.data.choices[0].delta.content)  # Note: chunk.data
```

### Example: Async Streaming

**v0.x:**
```python
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

client = MistralAsyncClient(api_key=api_key)
messages = [ChatMessage(role="user", content="What is the best French cheese?")]

async for chunk in client.chat_stream(model="mistral-large-latest", messages=messages):
    print(chunk.choices[0].delta.content)
```

**v1.x:**
```python
from mistralai import Mistral, UserMessage

client = Mistral(api_key=api_key)
messages = [UserMessage(content="What is the best French cheese?")]

async for chunk in await client.chat.stream_async(model="mistral-large-latest", messages=messages):
    print(chunk.data.choices[0].delta.content)
```
