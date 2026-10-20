# Audio.Agents

## Overview

### Available Operations

* [list](#list) - List audio agents
* [create](#create) - Create an audio agent
* [get](#get) - Get an audio agent
* [update](#update) - Update an audio agent
* [delete](#delete) - Delete an audio agent
* [list_versions](#list_versions) - List audio agent versions
* [list_sessions](#list_sessions) - List audio agent sessions

## list

List audio agents

### Example Usage

<!-- UsageSnippet language="python" operationID="list_agents_v1_audio_agents_get" method="get" path="/v1/audio/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.list(page_size=10)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of agents to return                                  |
| `page_token`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Cursor returned as next_page_token by the previous page             |
| `search`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Substring match on the agent name                                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListAgentsV1AudioAgentsGetResponse](../../models/listagentsv1audioagentsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create

Create an audio agent

### Example Usage

<!-- UsageSnippet language="python" operationID="create_agent_v1_audio_agents_post" method="post" path="/v1/audio/agents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.create(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                    | *str*                                                                                                     | :heavy_check_mark:                                                                                        | N/A                                                                                                       |
| `description`                                                                                             | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `configuration`                                                                                           | [OptionalNullable[models.AudioAgentConfigurationRequest]](../../models/audioagentconfigurationrequest.md) | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |

### Response

**[models.AudioAgentResponse](../../models/audioagentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get an audio agent

### Example Usage

<!-- UsageSnippet language="python" operationID="get_agent_v1_audio_agents__agent_id__get" method="get" path="/v1/audio/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.get(agent_id="967ae3d5-7e26-4ae8-9f9e-4dd9ab8fbfb9")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | Version to return. Defaults to the latest version.                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AudioAgentResponse](../../models/audioagentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update an audio agent

### Example Usage

<!-- UsageSnippet language="python" operationID="update_agent_v1_audio_agents__agent_id__put" method="put" path="/v1/audio/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.update(agent_id="70039ed8-34b8-4a49-ac83-e37ca84d423b", name="<value>", configuration={})

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `agent_id`                                                                              | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `name`                                                                                  | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `configuration`                                                                         | [models.AudioAgentConfigurationRequest](../../models/audioagentconfigurationrequest.md) | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `description`                                                                           | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

### Response

**[models.AudioAgentResponse](../../models/audioagentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete an audio agent

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_agent_v1_audio_agents__agent_id__delete" method="delete" path="/v1/audio/agents/{agent_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.audio.agents.delete(agent_id="b6128dca-4b79-48e5-ab7f-d746ef13d05b")

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

## list_versions

List audio agent versions

### Example Usage

<!-- UsageSnippet language="python" operationID="list_agent_versions_v1_audio_agents__agent_id__versions_get" method="get" path="/v1/audio/agents/{agent_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.list_versions(agent_id="89c92180-d7a8-47e4-98cc-96e5539d54cc", page_size=10)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of versions to return                                |
| `page_token`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Cursor returned as next_page_token by the previous page             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListAgentVersionsV1AudioAgentsAgentIDVersionsGetResponse](../../models/listagentversionsv1audioagentsagentidversionsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_sessions

List audio agent sessions

### Example Usage

<!-- UsageSnippet language="python" operationID="list_agent_sessions_v1_audio_agents__agent_id__sessions_get" method="get" path="/v1/audio/agents/{agent_id}/sessions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.agents.list_sessions(agent_id="8acd4f69-1e55-4801-85fe-b7864f46c0ac", page_size=10)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `agent_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of sessions to return                                |
| `page_token`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Cursor returned as next_page_token by the previous page             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListAgentSessionsV1AudioAgentsAgentIDSessionsGetResponse](../../models/listagentsessionsv1audioagentsagentidsessionsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |