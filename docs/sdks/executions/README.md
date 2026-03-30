# Workflows.Executions

## Overview

### Available Operations

* [get_workflow_execution](#get_workflow_execution) - Get Workflow Execution
* [get_workflow_execution_history](#get_workflow_execution_history) - Get Workflow Execution History
* [signal_workflow_execution](#signal_workflow_execution) - Signal Workflow Execution
* [query_workflow_execution](#query_workflow_execution) - Query Workflow Execution
* [terminate_workflow_execution](#terminate_workflow_execution) - Terminate Workflow Execution
* [batch_terminate_workflow_executions](#batch_terminate_workflow_executions) - Batch Terminate Workflow Executions
* [cancel_workflow_execution](#cancel_workflow_execution) - Cancel Workflow Execution
* [batch_cancel_workflow_executions](#batch_cancel_workflow_executions) - Batch Cancel Workflow Executions
* [reset_workflow](#reset_workflow) - Reset Workflow
* [update_workflow_execution](#update_workflow_execution) - Update Workflow Execution
* [get_workflow_execution_trace_otel](#get_workflow_execution_trace_otel) - Get Workflow Execution Trace Otel
* [get_workflow_execution_trace_summary](#get_workflow_execution_trace_summary) - Get Workflow Execution Trace Summary
* [get_workflow_execution_trace_events](#get_workflow_execution_trace_events) - Get Workflow Execution Trace Events
* [stream](#stream) - Stream

## get_workflow_execution

Get Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_v1_workflows_executions__execution_id__get" method="get" path="/v1/workflows/executions/{execution_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.get_workflow_execution(execution_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowExecutionResponse](../../models/workflowexecutionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_execution_history

Get Workflow Execution History

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_history_v1_workflows_executions__execution_id__history_get" method="get" path="/v1/workflows/executions/{execution_id}/history" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.get_workflow_execution_history(execution_id="<id>", decode_payloads=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `decode_payloads`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## signal_workflow_execution

Signal Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="signal_workflow_execution_v1_workflows_executions__execution_id__signals_post" method="post" path="/v1/workflows/executions/{execution_id}/signals" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.signal_workflow_execution(execution_id="<id>", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                       | Type                                                                                            | Required                                                                                        | Description                                                                                     |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `execution_id`                                                                                  | *str*                                                                                           | :heavy_check_mark:                                                                              | N/A                                                                                             |
| `name`                                                                                          | *str*                                                                                           | :heavy_check_mark:                                                                              | The name of the signal to send                                                                  |
| `input`                                                                                         | [OptionalNullable[models.SignalInvocationBodyInput]](../../models/signalinvocationbodyinput.md) | :heavy_minus_sign:                                                                              | Input data for the signal, matching its schema                                                  |
| `retries`                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                | :heavy_minus_sign:                                                                              | Configuration to override the default retry behavior of the client.                             |

### Response

**[models.SignalWorkflowResponse](../../models/signalworkflowresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## query_workflow_execution

Query Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="query_workflow_execution_v1_workflows_executions__execution_id__queries_post" method="post" path="/v1/workflows/executions/{execution_id}/queries" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.query_workflow_execution(execution_id="<id>", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `execution_id`                                                                                | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `name`                                                                                        | *str*                                                                                         | :heavy_check_mark:                                                                            | The name of the query to request                                                              |
| `input`                                                                                       | [OptionalNullable[models.QueryInvocationBodyInput]](../../models/queryinvocationbodyinput.md) | :heavy_minus_sign:                                                                            | Input data for the query, matching its schema                                                 |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.QueryWorkflowResponse](../../models/queryworkflowresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## terminate_workflow_execution

Terminate Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="terminate_workflow_execution_v1_workflows_executions__execution_id__terminate_post" method="post" path="/v1/workflows/executions/{execution_id}/terminate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.executions.terminate_workflow_execution(execution_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## batch_terminate_workflow_executions

Batch Terminate Workflow Executions

### Example Usage

<!-- UsageSnippet language="python" operationID="batch_terminate_workflow_executions_v1_workflows_executions_terminate_post" method="post" path="/v1/workflows/executions/terminate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.batch_terminate_workflow_executions(execution_ids=[
        "<value 1>",
        "<value 2>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_ids`                                                     | List[*str*]                                                         | :heavy_check_mark:                                                  | List of execution IDs to process                                    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BatchExecutionResponse](../../models/batchexecutionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## cancel_workflow_execution

Cancel Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="cancel_workflow_execution_v1_workflows_executions__execution_id__cancel_post" method="post" path="/v1/workflows/executions/{execution_id}/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.executions.cancel_workflow_execution(execution_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## batch_cancel_workflow_executions

Batch Cancel Workflow Executions

### Example Usage

<!-- UsageSnippet language="python" operationID="batch_cancel_workflow_executions_v1_workflows_executions_cancel_post" method="post" path="/v1/workflows/executions/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.batch_cancel_workflow_executions(execution_ids=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_ids`                                                     | List[*str*]                                                         | :heavy_check_mark:                                                  | List of execution IDs to process                                    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.BatchExecutionResponse](../../models/batchexecutionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## reset_workflow

Reset Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="reset_workflow_v1_workflows_executions__execution_id__reset_post" method="post" path="/v1/workflows/executions/{execution_id}/reset" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.executions.reset_workflow(execution_id="<id>", event_id=24149, exclude_signals=False, exclude_updates=False)

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `event_id`                                                          | *int*                                                               | :heavy_check_mark:                                                  | The event ID to reset the workflow execution to                     |
| `reason`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Reason for resetting the workflow execution                         |
| `exclude_signals`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to exclude signals that happened after the reset point      |
| `exclude_updates`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to exclude updates that happened after the reset point      |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_workflow_execution

Update Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="update_workflow_execution_v1_workflows_executions__execution_id__updates_post" method="post" path="/v1/workflows/executions/{execution_id}/updates" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.update_workflow_execution(execution_id="<id>", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                       | Type                                                                                            | Required                                                                                        | Description                                                                                     |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `execution_id`                                                                                  | *str*                                                                                           | :heavy_check_mark:                                                                              | N/A                                                                                             |
| `name`                                                                                          | *str*                                                                                           | :heavy_check_mark:                                                                              | The name of the update to request                                                               |
| `input`                                                                                         | [OptionalNullable[models.UpdateInvocationBodyInput]](../../models/updateinvocationbodyinput.md) | :heavy_minus_sign:                                                                              | Input data for the update, matching its schema                                                  |
| `retries`                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                | :heavy_minus_sign:                                                                              | Configuration to override the default retry behavior of the client.                             |

### Response

**[models.UpdateWorkflowResponse](../../models/updateworkflowresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_execution_trace_otel

Get Workflow Execution Trace Otel

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_trace_otel" method="get" path="/v1/workflows/executions/{execution_id}/trace/otel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.get_workflow_execution_trace_otel(execution_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowExecutionTraceOTelResponse](../../models/workflowexecutiontraceotelresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_execution_trace_summary

Get Workflow Execution Trace Summary

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_trace_summary" method="get" path="/v1/workflows/executions/{execution_id}/trace/summary" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.get_workflow_execution_trace_summary(execution_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowExecutionTraceSummaryResponse](../../models/workflowexecutiontracesummaryresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_execution_trace_events

Get Workflow Execution Trace Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_trace_events" method="get" path="/v1/workflows/executions/{execution_id}/trace/events" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.get_workflow_execution_trace_events(execution_id="<id>", merge_same_id_events=False, include_internal_events=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `merge_same_id_events`                                              | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `include_internal_events`                                           | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowExecutionTraceEventsResponse](../../models/workflowexecutiontraceeventsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## stream

Stream

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_v1_workflows_executions__execution_id__stream_get" method="get" path="/v1/workflows/executions/{execution_id}/stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.executions.stream(execution_id="<id>")

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `event_source`                                                      | [OptionalNullable[models.EventSource]](../../models/eventsource.md) | :heavy_minus_sign:                                                  | N/A                                                                 |
| `last_event_id`                                                     | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Union[eventstreaming.EventStream[models.StreamV1WorkflowsExecutionsExecutionIDStreamGetResponseBody], eventstreaming.EventStreamAsync[models.StreamV1WorkflowsExecutionsExecutionIDStreamGetResponseBody]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |