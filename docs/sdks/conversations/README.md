# Conversations
(*beta.conversations*)

## Overview

(beta) Conversations API

### Available Operations

* [start](#start) - Create a conversation and append entries to it.
* [list](#list) - List all created conversations.
* [get](#get) - Retrieve a conversation information.
* [append](#append) - Append new entries to an existing conversation.
* [get_history](#get_history) - Retrieve all entries in a conversation.
* [get_messages](#get_messages) - Retrieve all messages in a conversation.
* [restart](#restart) - Restart a conversation starting from a given entry.
* [start_stream](#start_stream) - Create a conversation and append entries to it.
* [append_stream](#append_stream) - Append new entries to an existing conversation.
* [restart_stream](#restart_stream) - Restart a conversation starting from a given entry.

## start

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation_id to continue the conversation.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.start(inputs="<value>", stream=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `inputs`                                                                      | [models.ConversationInputs](../../models/conversationinputs.md)               | :heavy_check_mark:                                                            | N/A                                                                           |
| `stream`                                                                      | *Optional[bool]*                                                              | :heavy_minus_sign:                                                            | N/A                                                                           |
| `store`                                                                       | *OptionalNullable[bool]*                                                      | :heavy_minus_sign:                                                            | N/A                                                                           |
| `handoff_execution`                                                           | [OptionalNullable[models.HandoffExecution]](../../models/handoffexecution.md) | :heavy_minus_sign:                                                            | N/A                                                                           |
| `instructions`                                                                | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `tools`                                                                       | List[[models.Tools](../../models/tools.md)]                                   | :heavy_minus_sign:                                                            | N/A                                                                           |
| `completion_args`                                                             | [OptionalNullable[models.CompletionArgs]](../../models/completionargs.md)     | :heavy_minus_sign:                                                            | N/A                                                                           |
| `name`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `agent_id`                                                                    | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `model`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

Retrieve a list of conversation entities sorted by creation time.

### Example Usage

```python
from mistralai import Mistral
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
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.ResponseBody]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Given a conversation_id retrieve a conversation entity with its attributes.

### Example Usage

```python
from mistralai import Mistral
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
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AgentsAPIV1ConversationsGetResponseV1ConversationsGet](../../models/agentsapiv1conversationsgetresponsev1conversationsget.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## append

Run completion on the history of the conversation and the user entries. Return the new created entries.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.append(conversation_id="<id>", inputs=[], stream=False, store=True, handoff_execution="server")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                               | Type                                                                                                                    | Required                                                                                                                | Description                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                       | *str*                                                                                                                   | :heavy_check_mark:                                                                                                      | ID of the conversation to which we append entries.                                                                      |
| `inputs`                                                                                                                | [models.ConversationInputs](../../models/conversationinputs.md)                                                         | :heavy_check_mark:                                                                                                      | N/A                                                                                                                     |
| `stream`                                                                                                                | *Optional[bool]*                                                                                                        | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `store`                                                                                                                 | *Optional[bool]*                                                                                                        | :heavy_minus_sign:                                                                                                      | Whether to store the results into our servers or not.                                                                   |
| `handoff_execution`                                                                                                     | [Optional[models.ConversationAppendRequestHandoffExecution]](../../models/conversationappendrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `completion_args`                                                                                                       | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                       | :heavy_minus_sign:                                                                                                      | White-listed arguments from the completion API                                                                          |
| `retries`                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                        | :heavy_minus_sign:                                                                                                      | Configuration to override the default retry behavior of the client.                                                     |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_history

Given a conversation_id retrieve all the entries belonging to that conversation. The entries are sorted in the order they were appended, those can be messages, connectors or function_call.

### Example Usage

```python
from mistralai import Mistral
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
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ConversationHistory](../../models/conversationhistory.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_messages

Given a conversation_id retrieve all the messages belonging to that conversation. This is similar to retrieving all entries except we filter the messages only.

### Example Usage

```python
from mistralai import Mistral
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
| `conversation_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ConversationMessages](../../models/conversationmessages.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## restart

Given a conversation_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.restart(conversation_id="<id>", inputs="<value>", from_entry_id="<id>", stream=False, store=True, handoff_execution="server")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                 | Type                                                                                                                      | Required                                                                                                                  | Description                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                         | *str*                                                                                                                     | :heavy_check_mark:                                                                                                        | N/A                                                                                                                       |
| `inputs`                                                                                                                  | [models.ConversationInputs](../../models/conversationinputs.md)                                                           | :heavy_check_mark:                                                                                                        | N/A                                                                                                                       |
| `from_entry_id`                                                                                                           | *str*                                                                                                                     | :heavy_check_mark:                                                                                                        | N/A                                                                                                                       |
| `stream`                                                                                                                  | *Optional[bool]*                                                                                                          | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `store`                                                                                                                   | *Optional[bool]*                                                                                                          | :heavy_minus_sign:                                                                                                        | Whether to store the results into our servers or not.                                                                     |
| `handoff_execution`                                                                                                       | [Optional[models.ConversationRestartRequestHandoffExecution]](../../models/conversationrestartrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                        | N/A                                                                                                                       |
| `completion_args`                                                                                                         | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                         | :heavy_minus_sign:                                                                                                        | White-listed arguments from the completion API                                                                            |
| `retries`                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                          | :heavy_minus_sign:                                                                                                        | Configuration to override the default retry behavior of the client.                                                       |

### Response

**[models.ConversationResponse](../../models/conversationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## start_stream

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation_id to continue the conversation.

### Example Usage

```python
from mistralai import Mistral
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
    ], stream=True)

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
| `tools`                                                                                                                         | List[[models.ConversationStreamRequestTools](../../models/conversationstreamrequesttools.md)]                                   | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `completion_args`                                                                                                               | [OptionalNullable[models.CompletionArgs]](../../models/completionargs.md)                                                       | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `name`                                                                                                                          | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `description`                                                                                                                   | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `agent_id`                                                                                                                      | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `model`                                                                                                                         | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## append_stream

Run completion on the history of the conversation and the user entries. Return the new created entries.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.append_stream(conversation_id="<id>", inputs="<value>", stream=True, store=True, handoff_execution="server")

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                           | Type                                                                                                                                | Required                                                                                                                            | Description                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                                   | *str*                                                                                                                               | :heavy_check_mark:                                                                                                                  | ID of the conversation to which we append entries.                                                                                  |
| `inputs`                                                                                                                            | [models.ConversationInputs](../../models/conversationinputs.md)                                                                     | :heavy_check_mark:                                                                                                                  | N/A                                                                                                                                 |
| `stream`                                                                                                                            | *Optional[bool]*                                                                                                                    | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `store`                                                                                                                             | *Optional[bool]*                                                                                                                    | :heavy_minus_sign:                                                                                                                  | Whether to store the results into our servers or not.                                                                               |
| `handoff_execution`                                                                                                                 | [Optional[models.ConversationAppendStreamRequestHandoffExecution]](../../models/conversationappendstreamrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                                  | N/A                                                                                                                                 |
| `completion_args`                                                                                                                   | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                                   | :heavy_minus_sign:                                                                                                                  | White-listed arguments from the completion API                                                                                      |
| `retries`                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                    | :heavy_minus_sign:                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                 |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## restart_stream

Given a conversation_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.conversations.restart_stream(conversation_id="<id>", inputs=[
        {
            "object": "entry",
            "type": "message.input",
            "role": "assistant",
            "content": "<value>",
        },
    ], from_entry_id="<id>", stream=True, store=True, handoff_execution="server")

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                             | Type                                                                                                                                  | Required                                                                                                                              | Description                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `conversation_id`                                                                                                                     | *str*                                                                                                                                 | :heavy_check_mark:                                                                                                                    | N/A                                                                                                                                   |
| `inputs`                                                                                                                              | [models.ConversationInputs](../../models/conversationinputs.md)                                                                       | :heavy_check_mark:                                                                                                                    | N/A                                                                                                                                   |
| `from_entry_id`                                                                                                                       | *str*                                                                                                                                 | :heavy_check_mark:                                                                                                                    | N/A                                                                                                                                   |
| `stream`                                                                                                                              | *Optional[bool]*                                                                                                                      | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `store`                                                                                                                               | *Optional[bool]*                                                                                                                      | :heavy_minus_sign:                                                                                                                    | Whether to store the results into our servers or not.                                                                                 |
| `handoff_execution`                                                                                                                   | [Optional[models.ConversationRestartStreamRequestHandoffExecution]](../../models/conversationrestartstreamrequesthandoffexecution.md) | :heavy_minus_sign:                                                                                                                    | N/A                                                                                                                                   |
| `completion_args`                                                                                                                     | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                                                     | :heavy_minus_sign:                                                                                                                    | White-listed arguments from the completion API                                                                                        |
| `retries`                                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                      | :heavy_minus_sign:                                                                                                                    | Configuration to override the default retry behavior of the client.                                                                   |

### Response

**[Union[eventstreaming.EventStream[models.ConversationEvents], eventstreaming.EventStreamAsync[models.ConversationEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |