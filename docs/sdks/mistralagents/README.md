# MistralAgents
(*beta.agents*)

## Overview

### Available Operations

* [create](#create) - Create a agent that can be used within a conversation.
* [list](#list) - List agent entities.
* [get](#get) - Retrieve an agent entity.
* [update](#update) - Update an agent entity.
* [update_version](#update_version) - Update an agent version.

## create

Create a new agent giving it instructions, tools, description. The agent is then available to be used as a regular assistant in a conversation or as part of an agent pool from which it can be used.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.create(model="Fiesta", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `model`                                                                             | *str*                                                                               | :heavy_check_mark:                                                                  | N/A                                                                                 |
| `name`                                                                              | *str*                                                                               | :heavy_check_mark:                                                                  | N/A                                                                                 |
| `instructions`                                                                      | *OptionalNullable[str]*                                                             | :heavy_minus_sign:                                                                  | Instruction prompt the model will follow during the conversation.                   |
| `tools`                                                                             | List[[models.AgentCreationRequestTools](../../models/agentcreationrequesttools.md)] | :heavy_minus_sign:                                                                  | List of tools which are available to the model during the conversation.             |
| `completion_args`                                                                   | [Optional[models.CompletionArgs]](../../models/completionargs.md)                   | :heavy_minus_sign:                                                                  | White-listed arguments from the completion API                                      |
| `description`                                                                       | *OptionalNullable[str]*                                                             | :heavy_minus_sign:                                                                  | N/A                                                                                 |
| `handoffs`                                                                          | List[*str*]                                                                         | :heavy_minus_sign:                                                                  | N/A                                                                                 |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

Retrieve a list of agent entities sorted by creation time.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.list()

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

**[List[models.Agent]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Given an agent retrieve an agent entity with its attributes.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.get(agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update an agent attributes and create a new version.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.update(agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                       | Type                                                                            | Required                                                                        | Description                                                                     |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `agent_id`                                                                      | *str*                                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `instructions`                                                                  | *OptionalNullable[str]*                                                         | :heavy_minus_sign:                                                              | Instruction prompt the model will follow during the conversation.               |
| `tools`                                                                         | List[[models.AgentUpdateRequestTools](../../models/agentupdaterequesttools.md)] | :heavy_minus_sign:                                                              | List of tools which are available to the model during the conversation.         |
| `completion_args`                                                               | [Optional[models.CompletionArgs]](../../models/completionargs.md)               | :heavy_minus_sign:                                                              | White-listed arguments from the completion API                                  |
| `model`                                                                         | *OptionalNullable[str]*                                                         | :heavy_minus_sign:                                                              | N/A                                                                             |
| `name`                                                                          | *OptionalNullable[str]*                                                         | :heavy_minus_sign:                                                              | N/A                                                                             |
| `description`                                                                   | *OptionalNullable[str]*                                                         | :heavy_minus_sign:                                                              | N/A                                                                             |
| `handoffs`                                                                      | List[*str*]                                                                     | :heavy_minus_sign:                                                              | N/A                                                                             |
| `retries`                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                | :heavy_minus_sign:                                                              | Configuration to override the default retry behavior of the client.             |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_version

Switch the version of an agent.

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.update_version(agent_id="<id>", version=193920)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |