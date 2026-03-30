# Workflows.Events

## Overview

### Available Operations

* [get_stream_events](#get_stream_events) - Get Stream Events
* [get_workflow_events](#get_workflow_events) - Get Workflow Events

## get_stream_events

Get Stream Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_stream_events_v1_workflows_events_stream_get" method="get" path="/v1/workflows/events/stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.events.get_stream_events(scope="*", activity_name="*", activity_id="*", workflow_name="*", workflow_exec_id="*", root_workflow_exec_id="*", parent_workflow_exec_id="*", stream="*", start_seq=0)

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `scope`                                                             | [Optional[models.Scope]](../../models/scope.md)                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `activity_name`                                                     | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `activity_id`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `workflow_name`                                                     | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `workflow_exec_id`                                                  | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `root_workflow_exec_id`                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `parent_workflow_exec_id`                                           | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `stream`                                                            | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `start_seq`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `metadata_filters`                                                  | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `workflow_event_types`                                              | List[[models.WorkflowEventType](../../models/workfloweventtype.md)] | :heavy_minus_sign:                                                  | N/A                                                                 |
| `last_event_id`                                                     | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Union[eventstreaming.EventStream[models.GetStreamEventsV1WorkflowsEventsStreamGetResponseBody], eventstreaming.EventStreamAsync[models.GetStreamEventsV1WorkflowsEventsStreamGetResponseBody]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_events

Get Workflow Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_events_v1_workflows_events_list_get" method="get" path="/v1/workflows/events/list" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.events.get_workflow_events(limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                              | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `root_workflow_exec_id`                                                | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Execution ID of the root workflow that initiated this execution chain. |
| `workflow_exec_id`                                                     | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Execution ID of the workflow that emitted this event.                  |
| `workflow_run_id`                                                      | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Run ID of the workflow that emitted this event.                        |
| `limit`                                                                | *Optional[int]*                                                        | :heavy_minus_sign:                                                     | Maximum number of events to return.                                    |
| `cursor`                                                               | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Cursor for pagination.                                                 |
| `retries`                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)       | :heavy_minus_sign:                                                     | Configuration to override the default retry behavior of the client.    |

### Response

**[models.ListWorkflowEventResponse](../../models/listworkfloweventresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |