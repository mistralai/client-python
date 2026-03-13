# Beta.Conversations

## Overview

(beta) Conversations API

### Available Operations

* [start](#start) - Create a conversation and append entries to it.
* [list](#list) - List all created conversations.
* [get](#get) - Retrieve a conversation information.
* [delete](#delete) - Delete a conversation.
* [append](#append) - Append new entries to an existing conversation.
* [get_history](#get_history) - Retrieve all entries in a conversation.
* [get_messages](#get_messages) - Retrieve all messages in a conversation.
* [restart](#restart) - Restart a conversation starting from a given entry.
* [list_internal](#list_internal) - List conversations filtered by user_id and conversation_source.
* [debug](#debug) - Debug a conversation by returning the complete completion payload.
* [debug_start](#debug_start) - Debug the start of a conversation by returning the initial completion request.
* [start_stream](#start_stream) - Create a conversation and append entries to it.
* [append_stream](#append_stream) - Append new entries to an existing conversation.
* [restart_stream](#restart_stream) - Restart a conversation starting from a given entry.

## start

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation_id to continue the conversation.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_start" method="post" path="/v1/conversations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.start(inputs="<value>", stream=False, completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `inputs`                                                                                                            | [models.ConversationInputs](../../models/conversationinputs.md)                                                     | :heavy_check_mark:                                                                                                  | N/A                                                                                                                 |
| `stream`                                                                                                            | *Optional[bool]*                                                                                                    | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `store`                                                                                                             | *OptionalNullable[bool]*                                                                                            | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `handoff_execution`                                                                                                 | [OptionalNullable[models.ConversationRequestHandoffExecution]](../../models/conversationrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `instructions`                                                                                                      | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `tools`                                                                                                             | List[[models.ConversationRequestTool](../../models/conversationrequesttool.md)]                                     | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `completion_args`                                                                                                   | [OptionalNullable[models.CompletionArgs]](../../models/completionargs.md)                                           | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `guardrails`                                                                                                        | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                                     | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `name`                                                                                                              | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `description`                                                                                                       | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `metadata`                                                                                                          | Dict[str, *Any*]                                                                                                    | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `agent_id`                                                                                                          | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `agent_version`                                                                                                     | [OptionalNullable[models.ConversationRequestAgentVersion]](../../models/conversationrequestagentversion.md)         | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `model`                                                                                                             | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

Retrieve a list of conversation entities sorted by creation time.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_list" method="get" path="/v1/conversations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.list(page=0, page_size=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `metadata`                                                          | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.AgentsAPIV1ConversationsListResponse]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Given a conversation_id retrieve a conversation entity with its attributes.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_get" method="get" path="/v1/conversations/{conversation_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.get(conversation_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | ID of the conversation from which we are fetching metadata.         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ResponseV1ConversationsGet](../../models/responsev1conversationsget.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete a conversation given a conversation_id.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_delete" method="delete" path="/v1/conversations/{conversation_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.conversations.delete(conversation_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | ID of the conversation from which we are fetching metadata.         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## append

Run completion on the history of the conversation and the user entries. Return the new created entries.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_append" method="post" path="/v1/conversations/{conversation_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.append(conversation_id="<id>", stream=False, store=True, handoff_execution="server", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                               | Type                                                                                                                    | Required                                                                                                                | Description                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                       | *str*                                                                                                                   | :heavy_check_mark:                                                                                                      | ID of the conversation to which we append entries.                                                                      |
| `inputs`                                                                                                                | [Optional[models.ConversationInputs]](../../models/conversationinputs.md)                                               | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `stream`                                                                                                                | *Optional[bool]*                                                                                                        | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `store`                                                                                                                 | *Optional[bool]*                                                                                                        | :heavy_minus_sign:                                                                                                      | Whether to store the results into our servers or not.                                                                   |
| `handoff_execution`                                                                                                     | [Optional[models.ConversationAppendRequestHandoffExecution]](../../models/conversationappendrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `completion_args`                                                                                                       | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                       | :heavy_minus_sign:                                                                                                      | White-listed arguments from the completion API                                                                          |
| `tool_confirmations`                                                                                                    | List[[models.ToolCallConfirmation](../../models/toolcallconfirmation.md)]                                               | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `retries`                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                        | :heavy_minus_sign:                                                                                                      | Configuration to override the default retry behavior of the client.                                                     |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_history

Given a conversation_id retrieve all the entries belonging to that conversation. The entries are sorted in the order they were appended, those can be messages, connectors or function_call.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_history" method="get" path="/v1/conversations/{conversation_id}/history" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.get_history(conversation_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | ID of the conversation from which we are fetching entries.          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ConversationHistory](../../models/conversationhistory.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_messages

Given a conversation_id retrieve all the messages belonging to that conversation. This is similar to retrieving all entries except we filter the messages only.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_messages" method="get" path="/v1/conversations/{conversation_id}/messages" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.get_messages(conversation_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | ID of the conversation from which we are fetching messages.         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ConversationMessages](../../models/conversationmessages.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## restart

Given a conversation_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_restart" method="post" path="/v1/conversations/{conversation_id}/restart" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.restart(conversation_id="<id>", from_entry_id="<id>", stream=False, store=True, handoff_execution="server", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                 | Type                                                                                                                      | Required                                                                                                                  | Description                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                         | *str*                                                                                                                     | :heavy_check_mark:                                                                                                        | ID of the original conversation which is being restarted.                                                                 |
| `from_entry_id`                                                                                                           | *str*                                                                                                                     | :heavy_check_mark:                                                                                                        | N/A                                                                                                                       |
| `inputs`                                                                                                                  | [Optional[models.ConversationInputs]](../../models/conversationinputs.md)                                                 | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `stream`                                                                                                                  | *Optional[bool]*                                                                                                          | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `store`                                                                                                                   | *Optional[bool]*                                                                                                          | :heavy_minus_sign:                                                                                                        | Whether to store the results into our servers or not.                                                                     |
| `handoff_execution`                                                                                                       | [Optional[models.ConversationRestartRequestHandoffExecution]](../../models/conversationrestartrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `instructions`                                                                                                            | *OptionalNullable[str]*                                                                                                   | :heavy_minus_sign:                                                                                                        | Instruction prompt the model will follow during the conversation.                                                         |
| `tools`                                                                                                                   | List[[models.ConversationRestartRequestTool](../../models/conversationrestartrequesttool.md)]                             | :heavy_minus_sign:                                                                                                        | List of tools which are available to the model during the conversation.                                                   |
| `completion_args`                                                                                                         | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                         | :heavy_minus_sign:                                                                                                        | White-listed arguments from the completion API                                                                            |
| `guardrails`                                                                                                              | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                                           | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `name`                                                                                                                    | *OptionalNullable[str]*                                                                                                   | :heavy_minus_sign:                                                                                                        | Name given to the conversation.                                                                                           |
| `description`                                                                                                             | *OptionalNullable[str]*                                                                                                   | :heavy_minus_sign:                                                                                                        | Description of the what the conversation is about.                                                                        |
| `metadata`                                                                                                                | Dict[str, *Any*]                                                                                                          | :heavy_minus_sign:                                                                                                        | Custom metadata for the conversation.                                                                                     |
| `model`                                                                                                                   | *OptionalNullable[str]*                                                                                                   | :heavy_minus_sign:                                                                                                        | Model which is used as assistant of the conversation. If not provided, will use the original conversation's model.        |
| `agent_id`                                                                                                                | *OptionalNullable[str]*                                                                                                   | :heavy_minus_sign:                                                                                                        | Agent which will be used as assistant to the conversation. If not provided, will use the original conversation's agent.   |
| `agent_version`                                                                                                           | [OptionalNullable[models.ConversationRestartRequestAgentVersion]](../../models/conversationrestartrequestagentversion.md) | :heavy_minus_sign:                                                                                                        | Specific version of the agent to use when restarting. If not provided, uses the current version.                          |
| `retries`                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                          | :heavy_minus_sign:                                                                                                        | Configuration to override the default retry behavior of the client.                                                       |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_internal

Internal endpoint to retrieve conversations filtered by user_id and conversation_source.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_internal_conversations_list" method="get" path="/v1/internal/conversations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.list_internal(page=0, page_size=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `page`                                                                  | *Optional[int]*                                                         | :heavy_minus_sign:                                                      | N/A                                                                     |
| `page_size`                                                             | *Optional[int]*                                                         | :heavy_minus_sign:                                                      | N/A                                                                     |
| `metadata`                                                              | Dict[str, *Any*]                                                        | :heavy_minus_sign:                                                      | N/A                                                                     |
| `user_id`                                                               | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | N/A                                                                     |
| `source`                                                                | [OptionalNullable[models.RequestSource]](../../models/requestsource.md) | :heavy_minus_sign:                                                      | N/A                                                                     |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[List[models.AgentsAPIV1InternalConversationsListResponse]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## debug

Debug a conversation by returning the complete completion payload.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_debug" method="get" path="/internal/v1/conversations/{conversation_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.debug(conversation_id="<id>", no_agents_prompt=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `no_agents_prompt`                                                  | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Dict[str, Any]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## debug_start

Debug the start of a conversation by returning the initial completion request.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_debug_start" method="post" path="/internal/v1/conversations/start" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.debug_start(inputs="<value>", stream=False, completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `inputs`                                                                                                            | [models.ConversationInputs](../../models/conversationinputs.md)                                                     | :heavy_check_mark:                                                                                                  | N/A                                                                                                                 |
| `stream`                                                                                                            | *Optional[bool]*                                                                                                    | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `store`                                                                                                             | *OptionalNullable[bool]*                                                                                            | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `handoff_execution`                                                                                                 | [OptionalNullable[models.ConversationRequestHandoffExecution]](../../models/conversationrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `instructions`                                                                                                      | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `tools`                                                                                                             | List[[models.ConversationRequestTool](../../models/conversationrequesttool.md)]                                     | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `completion_args`                                                                                                   | [OptionalNullable[models.CompletionArgs]](../../models/completionargs.md)                                           | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `guardrails`                                                                                                        | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                                     | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `name`                                                                                                              | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `description`                                                                                                       | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `metadata`                                                                                                          | Dict[str, *Any*]                                                                                                    | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `agent_id`                                                                                                          | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `agent_version`                                                                                                     | [OptionalNullable[models.ConversationRequestAgentVersion]](../../models/conversationrequestagentversion.md)         | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `model`                                                                                                             | *OptionalNullable[str]*                                                                                             | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |

### Response

**[Dict[str, Any]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## start_stream

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation_id to continue the conversation.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_start_stream" method="post" path="/v1/conversations#stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.start_stream(inputs=[
        {
            "object": "entry",
            "type": "function.result",
            "tool_call_id": "<id>",
            "result": "<value>",
        },
    ], stream=True, completion_args={
        "response_format": {
            "type": "text",
        },
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `inputs`                                                                                                                        | [models.ConversationInputs](../../models/conversationinputs.md)                                                                 | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `stream`                                                                                                                        | *Optional[bool]*                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `store`                                                                                                                         | *OptionalNullable[bool]*                                                                                                        | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `handoff_execution`                                                                                                             | [OptionalNullable[models.ConversationStreamRequestHandoffExecution]](../../models/conversationstreamrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `instructions`                                                                                                                  | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `tools`                                                                                                                         | List[[models.ConversationStreamRequestTool](../../models/conversationstreamrequesttool.md)]                                     | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `completion_args`                                                                                                               | [OptionalNullable[models.CompletionArgs]](../../models/completionargs.md)                                                       | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `guardrails`                                                                                                                    | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `name`                                                                                                                          | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `description`                                                                                                                   | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `metadata`                                                                                                                      | Dict[str, *Any*]                                                                                                                | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `agent_id`                                                                                                                      | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `agent_version`                                                                                                                 | [OptionalNullable[models.ConversationStreamRequestAgentVersion]](../../models/conversationstreamrequestagentversion.md)         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `model`                                                                                                                         | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## append_stream

Run completion on the history of the conversation and the user entries. Return the new created entries.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_append_stream" method="post" path="/v1/conversations/{conversation_id}#stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.append_stream(conversation_id="<id>", stream=True, store=True, handoff_execution="server", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                           | Type                                                                                                                                | Required                                                                                                                            | Description                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                                   | *str*                                                                                                                               | :heavy_check_mark:                                                                                                                  | ID of the conversation to which we append entries.                                                                                  |
| `inputs`                                                                                                                            | [Optional[models.ConversationInputs]](../../models/conversationinputs.md)                                                           | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `stream`                                                                                                                            | *Optional[bool]*                                                                                                                    | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `store`                                                                                                                             | *Optional[bool]*                                                                                                                    | :heavy_minus_sign:                                                                                                                  | Whether to store the results into our servers or not.                                                                               |
| `handoff_execution`                                                                                                                 | [Optional[models.ConversationAppendStreamRequestHandoffExecution]](../../models/conversationappendstreamrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `completion_args`                                                                                                                   | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                                   | :heavy_minus_sign:                                                                                                                  | White-listed arguments from the completion API                                                                                      |
| `tool_confirmations`                                                                                                                | List[[models.ToolCallConfirmation](../../models/toolcallconfirmation.md)]                                                           | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `retries`                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                    | :heavy_minus_sign:                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                 |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## restart_stream

Given a conversation_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_conversations_restart_stream" method="post" path="/v1/conversations/{conversation_id}/restart#stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.restart_stream(conversation_id="<id>", from_entry_id="<id>", stream=True, store=True, handoff_execution="server", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                             | Type                                                                                                                                  | Required                                                                                                                              | Description                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                                     | *str*                                                                                                                                 | :heavy_check_mark:                                                                                                                    | ID of the original conversation which is being restarted.                                                                             |
| `from_entry_id`                                                                                                                       | *str*                                                                                                                                 | :heavy_check_mark:                                                                                                                    | N/A                                                                                                                                   |
| `inputs`                                                                                                                              | [Optional[models.ConversationInputs]](../../models/conversationinputs.md)                                                             | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `stream`                                                                                                                              | *Optional[bool]*                                                                                                                      | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `store`                                                                                                                               | *Optional[bool]*                                                                                                                      | :heavy_minus_sign:                                                                                                                    | Whether to store the results into our servers or not.                                                                                 |
| `handoff_execution`                                                                                                                   | [Optional[models.ConversationRestartStreamRequestHandoffExecution]](../../models/conversationrestartstreamrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `instructions`                                                                                                                        | *OptionalNullable[str]*                                                                                                               | :heavy_minus_sign:                                                                                                                    | Instruction prompt the model will follow during the conversation.                                                                     |
| `tools`                                                                                                                               | List[[models.ConversationRestartStreamRequestTool](../../models/conversationrestartstreamrequesttool.md)]                             | :heavy_minus_sign:                                                                                                                    | List of tools which are available to the model during the conversation.                                                               |
| `completion_args`                                                                                                                     | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                                     | :heavy_minus_sign:                                                                                                                    | White-listed arguments from the completion API                                                                                        |
| `guardrails`                                                                                                                          | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                                                       | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `name`                                                                                                                                | *OptionalNullable[str]*                                                                                                               | :heavy_minus_sign:                                                                                                                    | Name given to the conversation.                                                                                                       |
| `description`                                                                                                                         | *OptionalNullable[str]*                                                                                                               | :heavy_minus_sign:                                                                                                                    | Description of the what the conversation is about.                                                                                    |
| `metadata`                                                                                                                            | Dict[str, *Any*]                                                                                                                      | :heavy_minus_sign:                                                                                                                    | Custom metadata for the conversation.                                                                                                 |
| `model`                                                                                                                               | *OptionalNullable[str]*                                                                                                               | :heavy_minus_sign:                                                                                                                    | Model which is used as assistant of the conversation. If not provided, will use the original conversation's model.                    |
| `agent_id`                                                                                                                            | *OptionalNullable[str]*                                                                                                               | :heavy_minus_sign:                                                                                                                    | Agent which will be used as assistant to the conversation. If not provided, will use the original conversation's agent.               |
| `agent_version`                                                                                                                       | [OptionalNullable[models.ConversationRestartStreamRequestAgentVersion]](../../models/conversationrestartstreamrequestagentversion.md) | :heavy_minus_sign:                                                                                                                    | Specific version of the agent to use when restarting. If not provided, uses the current version.                                      |
| `retries`                                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                      | :heavy_minus_sign:                                                                                                                    | Configuration to override the default retry behavior of the client.                                                                   |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |