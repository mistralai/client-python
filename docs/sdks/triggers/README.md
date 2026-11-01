# Beta.Triggers

## Overview

### Available Operations

* [create](#create) - Create Trigger
* [list](#list) - List Triggers
* [get](#get) - Get Trigger
* [delete](#delete) - Delete Trigger
* [list_events](#list_events) - List Trigger Events

## create

Create Trigger

### Example Usage

<!-- UsageSnippet language="python" operationID="create_trigger_v1_triggers_post" method="post" path="/v1/triggers" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.triggers.create(event_source_id="07adfb82-bcd1-462d-94df-cd3f8421627e", handler="spaces", action={
        "primitive_id": "<id>",
        "type": "start_workflow",
    }, owner_type="workspace", title="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `event_source_id`                                                                                 | *str*                                                                                             | :heavy_check_mark:                                                                                | ID of the event source that fires this trigger                                                    |
| `handler`                                                                                         | [models.TriggerHandler](../../models/triggerhandler.md)                                           | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `action`                                                                                          | [models.CreateTriggerAction](../../models/createtriggeraction.md)                                 | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `owner_type`                                                                                      | [models.TriggersOwnerType](../../models/triggersownertype.md)                                     | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `title`                                                                                           | *str*                                                                                             | :heavy_check_mark:                                                                                | Human-readable title of the trigger                                                               |
| `filters`                                                                                         | *OptionalNullable[str]*                                                                           | :heavy_minus_sign:                                                                                | jmespath expression to filter events, e.g. event_type == 'push' && repository.name == 'dashboard' |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.Trigger](../../models/trigger.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

List Triggers

### Example Usage

<!-- UsageSnippet language="python" operationID="list_triggers_v1_triggers_get" method="get" path="/v1/triggers" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.triggers.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                 | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `handler`                                                                 | [OptionalNullable[models.TriggerHandler]](../../models/triggerhandler.md) | :heavy_minus_sign:                                                        | Filter by handler type                                                    |
| `primitive_id`                                                            | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | Filter by primitive ID (workflow, agent, or app)                          |
| `event_source_id`                                                         | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | Filter by event source ID (webhook id)                                    |
| `retries`                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)          | :heavy_minus_sign:                                                        | Configuration to override the default retry behavior of the client.       |

### Response

**[List[models.Trigger]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get Trigger

### Example Usage

<!-- UsageSnippet language="python" operationID="get_trigger_v1_triggers__trigger_id__get" method="get" path="/v1/triggers/{trigger_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.triggers.get(trigger_id="8a031c37-160a-4451-9fb0-960dab51da01")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `trigger_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Trigger](../../models/trigger.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete Trigger

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_trigger_v1_triggers__trigger_id__delete" method="delete" path="/v1/triggers/{trigger_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.triggers.delete(trigger_id="c36bea2b-c2da-4ac5-b1bf-26d98b1c90b3")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `trigger_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_events

List Trigger Events

### Example Usage

<!-- UsageSnippet language="python" operationID="list_trigger_events_v1_triggers__trigger_id__events_get" method="get" path="/v1/triggers/{trigger_id}/events" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.triggers.list_events(trigger_id="a4a77501-7106-45dd-ba40-61b80d862c18", limit=10)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `trigger_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of events to return                                  |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.TriggerEventList](../../models/triggereventlist.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |