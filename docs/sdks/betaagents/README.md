# Beta.Agents

## Overview

(beta) Agents API

### Available Operations

* [create](#create) - Create a agent that can be used within a conversation.
* [list](#list) - List agent entities.
* [get](#get) - Retrieve an agent entity.
* [update](#update) - Update an agent entity.
* [delete](#delete) - Delete an agent entity.
* [update_version](#update_version) - Update an agent version.
* [list_versions](#list_versions) - List all versions of an agent.
* [get_version](#get_version) - Retrieve a specific version of an agent.
* [create_version_alias](#create_version_alias) - Create or update an agent version alias.
* [list_version_aliases](#list_version_aliases) - List all aliases for an agent.
* [delete_version_alias](#delete_version_alias) - Delete an agent version alias.
* [connector_usage_count](#connector_usage_count) - Get the count of agents using a connector.
* [create_internal](#create_internal) - Create an agent internally.
* [list_internal](#list_internal) - Retrieve all internal agent entities.
* [update_internal](#update_internal) - Update an agent internally.
* [get_internal](#get_internal) - Retrieve an internal agent entity.
* [delete_internal](#delete_internal) - Retrieve an internal agent entity.
* [get_version_internal](#get_version_internal) - Retrieve an internal agent entity with a version.

## create

Create a new agent giving it instructions, tools, description. The agent is then available to be used as a regular assistant in a conversation or as part of an agent pool from which it can be used.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_create" method="post" path="/v1/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.create(model="LeBaron", name="<value>", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | N/A                                                                               |
| `name`                                                                            | *str*                                                                             | :heavy_check_mark:                                                                | N/A                                                                               |
| `instructions`                                                                    | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | Instruction prompt the model will follow during the conversation.                 |
| `tools`                                                                           | List[[models.AgentCreationRequestTool](../../models/agentcreationrequesttool.md)] | :heavy_minus_sign:                                                                | List of tools which are available to the model during the conversation.           |
| `completion_args`                                                                 | [Optional[models.CompletionArgs]](../../models/completionargs.md)                 | :heavy_minus_sign:                                                                | White-listed arguments from the completion API                                    |
| `guardrails`                                                                      | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                   | :heavy_minus_sign:                                                                | N/A                                                                               |
| `description`                                                                     | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | N/A                                                                               |
| `handoffs`                                                                        | List[*str*]                                                                       | :heavy_minus_sign:                                                                | N/A                                                                               |
| `metadata`                                                                        | Dict[str, *Any*]                                                                  | :heavy_minus_sign:                                                                | N/A                                                                               |
| `version_message`                                                                 | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | N/A                                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

Retrieve a list of agent entities sorted by creation time.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_list" method="get" path="/v1/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.list(page=0, page_size=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Page number (0-indexed)                                             |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Number of agents per page                                           |
| `deployment_chat`                                                   | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sources`                                                           | List[[models.RequestSource](../../models/requestsource.md)]         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Filter by agent name                                                |
| `search`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Search agents by name or ID                                         |
| `id`                                                                | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `metadata`                                                          | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.Agent]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Given an agent, retrieve an agent entity with its attributes. The agent_version parameter can be an integer version number or a string alias.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_get" method="get" path="/v1/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.get(agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                     | Type                                                                                                          | Required                                                                                                      | Description                                                                                                   |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `agent_id`                                                                                                    | *str*                                                                                                         | :heavy_check_mark:                                                                                            | N/A                                                                                                           |
| `agent_version`                                                                                               | [OptionalNullable[models.AgentsAPIV1AgentsGetAgentVersion]](../../models/agentsapiv1agentsgetagentversion.md) | :heavy_minus_sign:                                                                                            | N/A                                                                                                           |
| `retries`                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                              | :heavy_minus_sign:                                                                                            | Configuration to override the default retry behavior of the client.                                           |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update an agent attributes and create a new version.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_update" method="patch" path="/v1/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.update(agent_id="<id>", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `agent_id`                                                                    | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `instructions`                                                                | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Instruction prompt the model will follow during the conversation.             |
| `tools`                                                                       | List[[models.AgentUpdateRequestTool](../../models/agentupdaterequesttool.md)] | :heavy_minus_sign:                                                            | List of tools which are available to the model during the conversation.       |
| `completion_args`                                                             | [Optional[models.CompletionArgs]](../../models/completionargs.md)             | :heavy_minus_sign:                                                            | White-listed arguments from the completion API                                |
| `guardrails`                                                                  | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]               | :heavy_minus_sign:                                                            | N/A                                                                           |
| `model`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `name`                                                                        | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `handoffs`                                                                    | List[*str*]                                                                   | :heavy_minus_sign:                                                            | N/A                                                                           |
| `deployment_chat`                                                             | *OptionalNullable[bool]*                                                      | :heavy_minus_sign:                                                            | N/A                                                                           |
| `metadata`                                                                    | Dict[str, *Any*]                                                              | :heavy_minus_sign:                                                            | N/A                                                                           |
| `version_message`                                                             | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete an agent entity.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_delete" method="delete" path="/v1/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.agents.delete(agent_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_version

Switch the version of an agent.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_update_version" method="patch" path="/v1/agents/{agent_id}/version" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.update_version(agent_id="<id>", version=157995)

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
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_versions

Retrieve all versions for a specific agent with full agent context. Supports pagination.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_list_versions" method="get" path="/v1/agents/{agent_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.list_versions(agent_id="<id>", page=0, page_size=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Page number (0-indexed)                                             |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Number of versions per page                                         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.Agent]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_version

Get a specific agent version by version number.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_get_version" method="get" path="/v1/agents/{agent_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.get_version(agent_id="<id>", version="788393")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Agent](../../models/agent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create_version_alias

Create a new alias or update an existing alias to point to a specific version. Aliases are unique per agent and can be reassigned to different versions.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_create_or_update_alias" method="put" path="/v1/agents/{agent_id}/aliases" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.create_version_alias(agent_id="<id>", alias="<value>", version=595141)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `alias`                                                             | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AgentAliasResponse](../../models/agentaliasresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_version_aliases

Retrieve all version aliases for a specific agent.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_list_version_aliases" method="get" path="/v1/agents/{agent_id}/aliases" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.list_version_aliases(agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.AgentAliasResponse]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_version_alias

Delete an existing alias for an agent.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_delete_alias" method="delete" path="/v1/agents/{agent_id}/aliases" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.agents.delete_version_alias(agent_id="<id>", alias="<value>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `alias`                                                             | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## connector_usage_count

Retrieve the count of agents that use a specific connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_connector_usage_count" method="get" path="/v1/agents/connectors/{connector_id}/count" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.connector_usage_count(connector_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Dict[str, Any]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create_internal

Create an internal agent

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_create" method="post" path="/v1/internal/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.create_internal(model="PT Cruiser", name="<value>", id="<id>", temperature=5280.1, conversation_examples=[], completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `model`                                                                                           | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `name`                                                                                            | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `id`                                                                                              | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `temperature`                                                                                     | *float*                                                                                           | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `conversation_examples`                                                                           | List[Dict[str, *str*]]                                                                            | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `instructions`                                                                                    | *OptionalNullable[str]*                                                                           | :heavy_minus_sign:                                                                                | Instruction prompt the model will follow during the conversation.                                 |
| `tools`                                                                                           | List[[models.InternalAgentCreationRequestTool](../../models/internalagentcreationrequesttool.md)] | :heavy_minus_sign:                                                                                | List of tools which are available to the model during the conversation.                           |
| `completion_args`                                                                                 | [Optional[models.CompletionArgs]](../../models/completionargs.md)                                 | :heavy_minus_sign:                                                                                | White-listed arguments from the completion API                                                    |
| `guardrails`                                                                                      | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                                   | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `description`                                                                                     | *OptionalNullable[str]*                                                                           | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `handoffs`                                                                                        | List[*str*]                                                                                       | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `metadata`                                                                                        | Dict[str, *Any*]                                                                                  | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `version_message`                                                                                 | *OptionalNullable[str]*                                                                           | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.AgentInternal](../../models/agentinternal.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_internal

Get the current agent version and turn into an internal payload

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_list" method="get" path="/v1/internal/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.list_internal(page=0, page_size=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Page number (0-indexed)                                             |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Number of agents per page                                           |
| `deployment_chat`                                                   | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sources`                                                           | List[[models.RequestSource](../../models/requestsource.md)]         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `search`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Search agents by name or ID                                         |
| `id`                                                                | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `metadata`                                                          | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.AgentInternal]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_internal

Update an internal agent, if it does not exist then create it.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_update" method="patch" path="/v1/internal/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.update_internal(agent_id="<id>", completion_args={
        "response_format": {
            "type": "text",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `agent_id`                                                                                    | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `instructions`                                                                                | *OptionalNullable[str]*                                                                       | :heavy_minus_sign:                                                                            | Instruction prompt the model will follow during the conversation.                             |
| `tools`                                                                                       | List[[models.InternalAgentUpdateRequestTool](../../models/internalagentupdaterequesttool.md)] | :heavy_minus_sign:                                                                            | List of tools which are available to the model during the conversation.                       |
| `completion_args`                                                                             | [Optional[models.CompletionArgs]](../../models/completionargs.md)                             | :heavy_minus_sign:                                                                            | White-listed arguments from the completion API                                                |
| `guardrails`                                                                                  | List[[models.GuardrailConfig](../../models/guardrailconfig.md)]                               | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `model`                                                                                       | *OptionalNullable[str]*                                                                       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `name`                                                                                        | *OptionalNullable[str]*                                                                       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `description`                                                                                 | *OptionalNullable[str]*                                                                       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `handoffs`                                                                                    | List[*str*]                                                                                   | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `metadata`                                                                                    | Dict[str, *Any*]                                                                              | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `version_message`                                                                             | *OptionalNullable[str]*                                                                       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `temperature`                                                                                 | *OptionalNullable[float]*                                                                     | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `conversation_examples`                                                                       | List[Dict[str, *str*]]                                                                        | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `created_at`                                                                                  | [date](https://docs.python.org/3/library/datetime.html#date-objects)                          | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `updated_at`                                                                                  | [date](https://docs.python.org/3/library/datetime.html#date-objects)                          | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `deployment_chat`                                                                             | *OptionalNullable[bool]*                                                                      | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.AgentInternal](../../models/agentinternal.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_internal

Get the current agent version and turn into an internal payload

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_get" method="get" path="/v1/internal/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.get_internal(agent_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AgentInternal](../../models/agentinternal.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_internal

Retrieve an internal agent entity.

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_delete" method="delete" path="/v1/internal/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.agents.delete_internal(agent_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_version_internal

Get the current agent version and turn into an internal payload

### Example Usage

<!-- UsageSnippet language="python" operationID="agents_api_v1_agents_internal_get_version" method="get" path="/v1/internal/agents/{agent_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.agents.get_version_internal(agent_id="<id>", version="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AgentInternal](../../models/agentinternal.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |