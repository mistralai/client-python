# Workflows

## Overview

### Available Operations

* [~~get_executions_v1_workflows_executions_get~~](#get_executions_v1_workflows_executions_get) - Get Executions :warning: **Deprecated**
* [get_workflow_execution_v1_workflows_executions_execution_id_get](#get_workflow_execution_v1_workflows_executions_execution_id_get) - Get Workflow Execution
* [get_workflow_execution_history_v1_workflows_executions_execution_id_history_get](#get_workflow_execution_history_v1_workflows_executions_execution_id_history_get) - Get Workflow Execution History
* [signal_workflow_execution_v1_workflows_executions_execution_id_signals_post](#signal_workflow_execution_v1_workflows_executions_execution_id_signals_post) - Signal Workflow Execution
* [query_workflow_execution_v1_workflows_executions_execution_id_queries_post](#query_workflow_execution_v1_workflows_executions_execution_id_queries_post) - Query Workflow Execution
* [terminate_workflow_execution_v1_workflows_executions_execution_id_terminate_post](#terminate_workflow_execution_v1_workflows_executions_execution_id_terminate_post) - Terminate Workflow Execution
* [batch_terminate_workflow_executions_v1_workflows_executions_terminate_post](#batch_terminate_workflow_executions_v1_workflows_executions_terminate_post) - Batch Terminate Workflow Executions
* [cancel_workflow_execution_v1_workflows_executions_execution_id_cancel_post](#cancel_workflow_execution_v1_workflows_executions_execution_id_cancel_post) - Cancel Workflow Execution
* [batch_cancel_workflow_executions_v1_workflows_executions_cancel_post](#batch_cancel_workflow_executions_v1_workflows_executions_cancel_post) - Batch Cancel Workflow Executions
* [reset_workflow_v1_workflows_executions_execution_id_reset_post](#reset_workflow_v1_workflows_executions_execution_id_reset_post) - Reset Workflow
* [update_workflow_execution_v1_workflows_executions_execution_id_updates_post](#update_workflow_execution_v1_workflows_executions_execution_id_updates_post) - Update Workflow Execution
* [get_workflow_execution_trace_otel](#get_workflow_execution_trace_otel) - Get Workflow Execution Trace Otel
* [get_workflow_execution_trace_summary](#get_workflow_execution_trace_summary) - Get Workflow Execution Trace Summary
* [get_workflow_execution_trace_events](#get_workflow_execution_trace_events) - Get Workflow Execution Trace Events
* [stream_v1_workflows_executions_execution_id_stream_get](#stream_v1_workflows_executions_execution_id_stream_get) - Stream
* [get_workflow_metrics_v1_workflows_workflow_name_metrics_get](#get_workflow_metrics_v1_workflows_workflow_name_metrics_get) - Get Workflow Metrics
* [list_runs_v1_workflows_runs_get](#list_runs_v1_workflows_runs_get) - List Runs
* [get_run_v1_workflows_runs_run_id_get](#get_run_v1_workflows_runs_run_id_get) - Get Run
* [get_run_history_v1_workflows_runs_run_id_history_get](#get_run_history_v1_workflows_runs_run_id_history_get) - Get Run History
* [get_schedules_v1_workflows_schedules_get](#get_schedules_v1_workflows_schedules_get) - Get Schedules
* [schedule_workflow_v1_workflows_schedules_post](#schedule_workflow_v1_workflows_schedules_post) - Schedule Workflow
* [unschedule_workflow_v1_workflows_schedules_schedule_id_delete](#unschedule_workflow_v1_workflows_schedules_schedule_id_delete) - Unschedule Workflow
* [receive_workflow_event_v1_workflows_events_post](#receive_workflow_event_v1_workflows_events_post) - Receive Workflow Event
* [get_stream_events_v1_workflows_events_stream_get](#get_stream_events_v1_workflows_events_stream_get) - Get Stream Events
* [get_workflow_events_v1_workflows_events_list_get](#get_workflow_events_v1_workflows_events_list_get) - Get Workflow Events
* [get_workflows_v1_workflows_get](#get_workflows_v1_workflows_get) - Get Workflows
* [get_workflow_registrations_v1_workflows_registrations_get](#get_workflow_registrations_v1_workflows_registrations_get) - Get Workflow Registrations
* [~~get_workflow_registrations_deprecated_v1_workflows_versions_get~~](#get_workflow_registrations_deprecated_v1_workflows_versions_get) - Get Workflow Registrations Deprecated :warning: **Deprecated**
* [register_workflow_definitions_v1_workflows_register_post](#register_workflow_definitions_v1_workflows_register_post) - Register Workflow Definitions
* [execute_workflow_v1_workflows_workflow_identifier_execute_post](#execute_workflow_v1_workflows_workflow_identifier_execute_post) - Execute Workflow
* [execute_workflow_registration_v1_workflows_registrations_workflow_registration_id_execute_post](#execute_workflow_registration_v1_workflows_registrations_workflow_registration_id_execute_post) - Execute Workflow Registration
* [~~execute_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_execute_post~~](#execute_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_execute_post) - Execute Workflow Registration Deprecated :warning: **Deprecated**
* [get_workflow_v1_workflows_workflow_identifier_get](#get_workflow_v1_workflows_workflow_identifier_get) - Get Workflow
* [update_workflow_v1_workflows_workflow_identifier_put](#update_workflow_v1_workflows_workflow_identifier_put) - Update Workflow
* [get_workflow_registration_v1_workflows_registrations_workflow_registration_id_get](#get_workflow_registration_v1_workflows_registrations_workflow_registration_id_get) - Get Workflow Registration
* [~~get_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_get~~](#get_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_get) - Get Workflow Registration Deprecated :warning: **Deprecated**
* [archive_workflow_v1_workflows_workflow_identifier_archive_put](#archive_workflow_v1_workflows_workflow_identifier_archive_put) - Archive Workflow
* [unarchive_workflow_v1_workflows_workflow_identifier_unarchive_put](#unarchive_workflow_v1_workflows_workflow_identifier_unarchive_put) - Unarchive Workflow

## ~~get_executions_v1_workflows_executions_get~~

Get Executions

> :warning: **DEPRECATED**: This will be removed in a future release, please migrate away from it as soon as possible.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_executions_v1_workflows_executions_get" method="get" path="/v1/workflows/executions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_executions_v1_workflows_executions_get(page_size=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                           | Type                                                                                                                                | Required                                                                                                                            | Description                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_identifier`                                                                                                               | *OptionalNullable[str]*                                                                                                             | :heavy_minus_sign:                                                                                                                  | Filter by workflow name or id                                                                                                       |
| `search`                                                                                                                            | *OptionalNullable[str]*                                                                                                             | :heavy_minus_sign:                                                                                                                  | Search by workflow name, display name or id                                                                                         |
| `status`                                                                                                                            | [OptionalNullable[models.GetExecutionsV1WorkflowsExecutionsGetStatus]](../../models/getexecutionsv1workflowsexecutionsgetstatus.md) | :heavy_minus_sign:                                                                                                                  | Filter by workflow status                                                                                                           |
| `page_size`                                                                                                                         | *Optional[int]*                                                                                                                     | :heavy_minus_sign:                                                                                                                  | Number of items per page                                                                                                            |
| `next_page_token`                                                                                                                   | *OptionalNullable[str]*                                                                                                             | :heavy_minus_sign:                                                                                                                  | Token for the next page of results                                                                                                  |
| `retries`                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                    | :heavy_minus_sign:                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                 |

### Response

**[models.WorkflowExecutionListResponse](../../models/workflowexecutionlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_execution_v1_workflows_executions_execution_id_get

Get Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_v1_workflows_executions__execution_id__get" method="get" path="/v1/workflows/executions/{execution_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_execution_v1_workflows_executions_execution_id_get(execution_id="<id>")

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

## get_workflow_execution_history_v1_workflows_executions_execution_id_history_get

Get Workflow Execution History

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_execution_history_v1_workflows_executions__execution_id__history_get" method="get" path="/v1/workflows/executions/{execution_id}/history" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_execution_history_v1_workflows_executions_execution_id_history_get(execution_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `execution_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## signal_workflow_execution_v1_workflows_executions_execution_id_signals_post

Signal Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="signal_workflow_execution_v1_workflows_executions__execution_id__signals_post" method="post" path="/v1/workflows/executions/{execution_id}/signals" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.signal_workflow_execution_v1_workflows_executions_execution_id_signals_post(execution_id="<id>", name="<value>")

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

## query_workflow_execution_v1_workflows_executions_execution_id_queries_post

Query Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="query_workflow_execution_v1_workflows_executions__execution_id__queries_post" method="post" path="/v1/workflows/executions/{execution_id}/queries" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.query_workflow_execution_v1_workflows_executions_execution_id_queries_post(execution_id="<id>", name="<value>")

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

## terminate_workflow_execution_v1_workflows_executions_execution_id_terminate_post

Terminate Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="terminate_workflow_execution_v1_workflows_executions__execution_id__terminate_post" method="post" path="/v1/workflows/executions/{execution_id}/terminate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.terminate_workflow_execution_v1_workflows_executions_execution_id_terminate_post(execution_id="<id>")

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

## batch_terminate_workflow_executions_v1_workflows_executions_terminate_post

Batch Terminate Workflow Executions

### Example Usage

<!-- UsageSnippet language="python" operationID="batch_terminate_workflow_executions_v1_workflows_executions_terminate_post" method="post" path="/v1/workflows/executions/terminate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.batch_terminate_workflow_executions_v1_workflows_executions_terminate_post(execution_ids=[
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

## cancel_workflow_execution_v1_workflows_executions_execution_id_cancel_post

Cancel Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="cancel_workflow_execution_v1_workflows_executions__execution_id__cancel_post" method="post" path="/v1/workflows/executions/{execution_id}/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.cancel_workflow_execution_v1_workflows_executions_execution_id_cancel_post(execution_id="<id>")

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

## batch_cancel_workflow_executions_v1_workflows_executions_cancel_post

Batch Cancel Workflow Executions

### Example Usage

<!-- UsageSnippet language="python" operationID="batch_cancel_workflow_executions_v1_workflows_executions_cancel_post" method="post" path="/v1/workflows/executions/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.batch_cancel_workflow_executions_v1_workflows_executions_cancel_post(execution_ids=[])

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

## reset_workflow_v1_workflows_executions_execution_id_reset_post

Reset Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="reset_workflow_v1_workflows_executions__execution_id__reset_post" method="post" path="/v1/workflows/executions/{execution_id}/reset" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.reset_workflow_v1_workflows_executions_execution_id_reset_post(execution_id="<id>", event_id=24149, exclude_signals=False, exclude_updates=False)

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

## update_workflow_execution_v1_workflows_executions_execution_id_updates_post

Update Workflow Execution

### Example Usage

<!-- UsageSnippet language="python" operationID="update_workflow_execution_v1_workflows_executions__execution_id__updates_post" method="post" path="/v1/workflows/executions/{execution_id}/updates" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.update_workflow_execution_v1_workflows_executions_execution_id_updates_post(execution_id="<id>", name="<value>")

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

    res = mistral.workflows.get_workflow_execution_trace_otel(execution_id="<id>")

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

    res = mistral.workflows.get_workflow_execution_trace_summary(execution_id="<id>")

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

    res = mistral.workflows.get_workflow_execution_trace_events(execution_id="<id>", merge_same_id_events=False, include_internal_events=False)

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

## stream_v1_workflows_executions_execution_id_stream_get

Stream

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_v1_workflows_executions__execution_id__stream_get" method="get" path="/v1/workflows/executions/{execution_id}/stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.stream_v1_workflows_executions_execution_id_stream_get(execution_id="<id>")

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

## get_workflow_metrics_v1_workflows_workflow_name_metrics_get

Get comprehensive metrics for a specific workflow.

Args:
    workflow_name: The name of the workflow type to get metrics for
    start_time: Optional start time filter (ISO 8601 format)
    end_time: Optional end time filter (ISO 8601 format)

Returns:
    WorkflowMetrics: Dictionary containing metrics:
        - execution_count: Total number of executions
        - success_count: Number of successful executions
        - error_count: Number of failed/terminated executions
        - average_latency_ms: Average execution duration in milliseconds
        - retry_rate: Proportion of workflows with retries
        - latency_over_time: Time-series data of execution durations

Example:
    GET /v1/workflows/MyWorkflow/metrics
    GET /v1/workflows/MyWorkflow/metrics?start_time=2025-01-01T00:00:00Z
    GET /v1/workflows/MyWorkflow/metrics?start_time=2025-01-01T00:00:00Z&end_time=2025-12-31T23:59:59Z

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_metrics_v1_workflows__workflow_name__metrics_get" method="get" path="/v1/workflows/{workflow_name}/metrics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_metrics_v1_workflows_workflow_name_metrics_get(workflow_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `workflow_name`                                                      | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `start_time`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | Filter workflows started after this time (ISO 8601)                  |
| `end_time`                                                           | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | Filter workflows started before this time (ISO 8601)                 |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.WorkflowMetrics](../../models/workflowmetrics.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_runs_v1_workflows_runs_get

List Runs

### Example Usage

<!-- UsageSnippet language="python" operationID="list_runs_v1_workflows_runs_get" method="get" path="/v1/workflows/runs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.list_runs_v1_workflows_runs_get(page_size=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                     | Type                                                                                                          | Required                                                                                                      | Description                                                                                                   |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `workflow_identifier`                                                                                         | *OptionalNullable[str]*                                                                                       | :heavy_minus_sign:                                                                                            | Filter by workflow name or id                                                                                 |
| `search`                                                                                                      | *OptionalNullable[str]*                                                                                       | :heavy_minus_sign:                                                                                            | Search by workflow name, display name or id                                                                   |
| `status`                                                                                                      | [OptionalNullable[models.ListRunsV1WorkflowsRunsGetStatus]](../../models/listrunsv1workflowsrunsgetstatus.md) | :heavy_minus_sign:                                                                                            | Filter by workflow status                                                                                     |
| `page_size`                                                                                                   | *Optional[int]*                                                                                               | :heavy_minus_sign:                                                                                            | Number of items per page                                                                                      |
| `next_page_token`                                                                                             | *OptionalNullable[str]*                                                                                       | :heavy_minus_sign:                                                                                            | Token for the next page of results                                                                            |
| `retries`                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                              | :heavy_minus_sign:                                                                                            | Configuration to override the default retry behavior of the client.                                           |

### Response

**[models.WorkflowExecutionListResponse](../../models/workflowexecutionlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_run_v1_workflows_runs_run_id_get

Get Run

### Example Usage

<!-- UsageSnippet language="python" operationID="get_run_v1_workflows_runs__run_id__get" method="get" path="/v1/workflows/runs/{run_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_run_v1_workflows_runs_run_id_get(run_id="553b071e-3d04-46aa-aa9a-0fca61dc60fa")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowExecutionResponse](../../models/workflowexecutionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_run_history_v1_workflows_runs_run_id_history_get

Get Run History

### Example Usage

<!-- UsageSnippet language="python" operationID="get_run_history_v1_workflows_runs__run_id__history_get" method="get" path="/v1/workflows/runs/{run_id}/history" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_run_history_v1_workflows_runs_run_id_history_get(run_id="f7296489-0212-4239-9e35-12fabfe8cd11")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_schedules_v1_workflows_schedules_get

Get Schedules

### Example Usage

<!-- UsageSnippet language="python" operationID="get_schedules_v1_workflows_schedules_get" method="get" path="/v1/workflows/schedules" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_schedules_v1_workflows_schedules_get()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowScheduleListResponse](../../models/workflowschedulelistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## schedule_workflow_v1_workflows_schedules_post

Schedule Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="schedule_workflow_v1_workflows_schedules_post" method="post" path="/v1/workflows/schedules" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.schedule_workflow_v1_workflows_schedules_post(schedule={
        "input": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                 | Type                                                                                                                                                                                                                                                                                      | Required                                                                                                                                                                                                                                                                                  | Description                                                                                                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schedule`                                                                                                                                                                                                                                                                                | [models.ScheduleDefinition](../../models/scheduledefinition.md)                                                                                                                                                                                                                           | :heavy_check_mark:                                                                                                                                                                                                                                                                        | Specification of the times scheduled actions may occur.<br/><br/>The times are the union of :py:attr:`calendars`, :py:attr:`intervals`, and<br/>:py:attr:`cron_expressions` excluding anything in :py:attr:`skip`.<br/><br/>Used for input where schedule_id is optional (can be provided or auto-generated). |
| `workflow_registration_id`                                                                                                                                                                                                                                                                | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | The ID of the workflow registration to schedule                                                                                                                                                                                                                                           |
| `workflow_version_id`                                                                                                                                                                                                                                                                     | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | Deprecated: use workflow_registration_id                                                                                                                                                                                                                                                  |
| `workflow_identifier`                                                                                                                                                                                                                                                                     | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | The name or ID of the workflow to schedule                                                                                                                                                                                                                                                |
| `workflow_task_queue`                                                                                                                                                                                                                                                                     | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | The task queue of the workflow to schedule                                                                                                                                                                                                                                                |
| `schedule_id`                                                                                                                                                                                                                                                                             | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | Allows you to specify a custom schedule ID. If not provided, a random ID will be generated.                                                                                                                                                                                               |
| `deployment_name`                                                                                                                                                                                                                                                                         | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | Name of the deployment to route this schedule to                                                                                                                                                                                                                                          |
| `retries`                                                                                                                                                                                                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                       |

### Response

**[models.WorkflowScheduleResponse](../../models/workflowscheduleresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unschedule_workflow_v1_workflows_schedules_schedule_id_delete

Unschedule Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="unschedule_workflow_v1_workflows_schedules__schedule_id__delete" method="delete" path="/v1/workflows/schedules/{schedule_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.unschedule_workflow_v1_workflows_schedules_schedule_id_delete(schedule_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `schedule_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## receive_workflow_event_v1_workflows_events_post

Receive workflow events from workers.

Events are published to NATS for real-time streaming and persisted in the database.

For shared workers, the actual execution owner is resolved from the execution record,
ensuring events are streamed to the correct user's namespace.

### Example Usage

<!-- UsageSnippet language="python" operationID="receive_workflow_event_v1_workflows_events_post" method="post" path="/v1/workflows/events" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.receive_workflow_event_v1_workflows_events_post(event={
        "event_id": "<id>",
        "root_workflow_exec_id": "<id>",
        "workflow_exec_id": "<id>",
        "workflow_run_id": "<id>",
        "workflow_name": "<value>",
        "event_type": "CUSTOM_TASK_STARTED",
        "attributes": {
            "custom_task_id": "<id>",
            "custom_task_type": "<value>",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `event`                                                                       | [models.WorkflowEventRequestEvent](../../models/workfloweventrequestevent.md) | :heavy_check_mark:                                                            | The workflow event payload.                                                   |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.WorkflowEventResponse](../../models/workfloweventresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_stream_events_v1_workflows_events_stream_get

Get Stream Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_stream_events_v1_workflows_events_stream_get" method="get" path="/v1/workflows/events/stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_stream_events_v1_workflows_events_stream_get(scope="*", activity_name="*", activity_id="*", workflow_name="*", workflow_exec_id="*", root_workflow_exec_id="*", parent_workflow_exec_id="*", stream="*", start_seq=0)

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

## get_workflow_events_v1_workflows_events_list_get

Get Workflow Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_events_v1_workflows_events_list_get" method="get" path="/v1/workflows/events/list" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_events_v1_workflows_events_list_get(limit=100)

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

## get_workflows_v1_workflows_get

Get Workflows

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflows_v1_workflows_get" method="get" path="/v1/workflows" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflows_v1_workflows_get(active_only=False, include_shared=True, include_archived=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `active_only`                                                       | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to only return active workflows                             |
| `include_shared`                                                    | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include shared workflows                                 |
| `available_in_chat_assistant`                                       | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | Whether to only return workflows compatible with chat assistant     |
| `include_archived`                                                  | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include archived workflows                               |
| `cursor`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The cursor for pagination                                           |
| `limit`                                                             | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | The maximum number of workflows to return                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowListResponse](../../models/workflowlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_registrations_v1_workflows_registrations_get

Get Workflow Registrations

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registrations_v1_workflows_registrations_get" method="get" path="/v1/workflows/registrations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registrations_v1_workflows_registrations_get(active_only=False, include_shared=True, include_archived=False, with_workflow=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_id`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The workflow ID to filter by                                        |
| `task_queue`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The task queue to filter by                                         |
| `active_only`                                                       | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to only return active workflows versions                    |
| `include_shared`                                                    | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include shared workflow versions                         |
| `workflow_search`                                                   | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The workflow name to filter by                                      |
| `include_archived`                                                  | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include archived workflows                               |
| `with_workflow`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include the workflow definition                          |
| `available_in_chat_assistant`                                       | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | Whether to only return workflows compatible with chat assistant     |
| `limit`                                                             | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | The maximum number of workflows versions to return                  |
| `cursor`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The cursor for pagination                                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowRegistrationListResponse](../../models/workflowregistrationlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## ~~get_workflow_registrations_deprecated_v1_workflows_versions_get~~

Get Workflow Registrations Deprecated

> :warning: **DEPRECATED**: This will be removed in a future release, please migrate away from it as soon as possible.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registrations_deprecated_v1_workflows_versions_get" method="get" path="/v1/workflows/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registrations_deprecated_v1_workflows_versions_get(active_only=False, include_shared=True, include_archived=False, with_workflow=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_id`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `task_queue`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `active_only`                                                       | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `include_shared`                                                    | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `workflow_search`                                                   | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `include_archived`                                                  | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `with_workflow`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `available_in_chat_assistant`                                       | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | N/A                                                                 |
| `limit`                                                             | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `cursor`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowRegistrationListResponse](../../models/workflowregistrationlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## register_workflow_definitions_v1_workflows_register_post

Register workflow specs. This endpoint is only meant to be used by workers.

### Example Usage

<!-- UsageSnippet language="python" operationID="register_workflow_definitions_v1_workflows_register_post" method="post" path="/v1/workflows/register" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.register_workflow_definitions_v1_workflows_register_post(definitions=[
        {
            "input_schema": {
                "key": "<value>",
                "key1": "<value>",
            },
            "name": "<value>",
            "task_queue": "<value>",
        },
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `definitions`                                                                       | List[[models.WorkflowSpecWithTaskQueue](../../models/workflowspecwithtaskqueue.md)] | :heavy_check_mark:                                                                  | List of workflow specs to register                                                  |
| `deployment_name`                                                                   | *OptionalNullable[str]*                                                             | :heavy_minus_sign:                                                                  | Name of the deployment this worker belongs to                                       |
| `worker_name`                                                                       | *OptionalNullable[str]*                                                             | :heavy_minus_sign:                                                                  | Human-readable name of this worker process (hostname or pod name)                   |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |

### Response

**[models.WorkflowSpecsRegisterResponse](../../models/workflowspecsregisterresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## execute_workflow_v1_workflows_workflow_identifier_execute_post

Execute Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_workflow_v1_workflows__workflow_identifier__execute_post" method="post" path="/v1/workflows/{workflow_identifier}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.execute_workflow_v1_workflows_workflow_identifier_execute_post(workflow_identifier="<value>", wait_for_result=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                        | Type                                                                                             | Required                                                                                         | Description                                                                                      |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `workflow_identifier`                                                                            | *str*                                                                                            | :heavy_check_mark:                                                                               | N/A                                                                                              |
| `execution_id`                                                                                   | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Allows you to specify a custom execution ID. If not provided, a random ID will be generated.     |
| `input`                                                                                          | Dict[str, *Any*]                                                                                 | :heavy_minus_sign:                                                                               | The input to the workflow. This should be a dictionary that matches the workflow's input schema. |
| `encoded_input`                                                                                  | [OptionalNullable[models.NetworkEncodedInput]](../../models/networkencodedinput.md)              | :heavy_minus_sign:                                                                               | Encoded input to the workflow, used when payload encoding is enabled.                            |
| `wait_for_result`                                                                                | *Optional[bool]*                                                                                 | :heavy_minus_sign:                                                                               | If true, wait for the workflow to complete and return the result directly.                       |
| `timeout_seconds`                                                                                | *OptionalNullable[float]*                                                                        | :heavy_minus_sign:                                                                               | Maximum time to wait for completion when wait_for_result is true.                                |
| `custom_tracing_attributes`                                                                      | Dict[str, *str*]                                                                                 | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `task_queue`                                                                                     | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | The name of the task queue to use for the workflow                                               |
| `deployment_name`                                                                                | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Name of the deployment to route this execution to                                                |
| `retries`                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                 | :heavy_minus_sign:                                                                               | Configuration to override the default retry behavior of the client.                              |

### Response

**[models.ResponseExecuteWorkflowV1WorkflowsWorkflowIdentifierExecutePost](../../models/responseexecuteworkflowv1workflowsworkflowidentifierexecutepost.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## execute_workflow_registration_v1_workflows_registrations_workflow_registration_id_execute_post

Execute Workflow Registration

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post" method="post" path="/v1/workflows/registrations/{workflow_registration_id}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.execute_workflow_registration_v1_workflows_registrations_workflow_registration_id_execute_post(workflow_registration_id="de11d76a-e0fb-44dd-abd9-2e75fc275b94", wait_for_result=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                        | Type                                                                                             | Required                                                                                         | Description                                                                                      |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `workflow_registration_id`                                                                       | *str*                                                                                            | :heavy_check_mark:                                                                               | N/A                                                                                              |
| `execution_id`                                                                                   | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Allows you to specify a custom execution ID. If not provided, a random ID will be generated.     |
| `input`                                                                                          | Dict[str, *Any*]                                                                                 | :heavy_minus_sign:                                                                               | The input to the workflow. This should be a dictionary that matches the workflow's input schema. |
| `encoded_input`                                                                                  | [OptionalNullable[models.NetworkEncodedInput]](../../models/networkencodedinput.md)              | :heavy_minus_sign:                                                                               | Encoded input to the workflow, used when payload encoding is enabled.                            |
| `wait_for_result`                                                                                | *Optional[bool]*                                                                                 | :heavy_minus_sign:                                                                               | If true, wait for the workflow to complete and return the result directly.                       |
| `timeout_seconds`                                                                                | *OptionalNullable[float]*                                                                        | :heavy_minus_sign:                                                                               | Maximum time to wait for completion when wait_for_result is true.                                |
| `custom_tracing_attributes`                                                                      | Dict[str, *str*]                                                                                 | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `task_queue`                                                                                     | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | The name of the task queue to use for the workflow                                               |
| `deployment_name`                                                                                | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Name of the deployment to route this execution to                                                |
| `retries`                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                 | :heavy_minus_sign:                                                                               | Configuration to override the default retry behavior of the client.                              |

### Response

**[models.ResponseExecuteWorkflowRegistrationV1WorkflowsRegistrationsWorkflowRegistrationIDExecutePost](../../models/responseexecuteworkflowregistrationv1workflowsregistrationsworkflowregistrationidexecutepost.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## ~~execute_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_execute_post~~

Execute Workflow Registration Deprecated

> :warning: **DEPRECATED**: This will be removed in a future release, please migrate away from it as soon as possible.

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_workflow_registration_deprecated_v1_workflows_versions__workflow_version_id__execute_post" method="post" path="/v1/workflows/versions/{workflow_version_id}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.execute_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_execute_post(workflow_version_id="23a76588-231d-43dc-abfb-66057817ac5b", wait_for_result=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                        | Type                                                                                             | Required                                                                                         | Description                                                                                      |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `workflow_version_id`                                                                            | *str*                                                                                            | :heavy_check_mark:                                                                               | N/A                                                                                              |
| `execution_id`                                                                                   | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Allows you to specify a custom execution ID. If not provided, a random ID will be generated.     |
| `input`                                                                                          | Dict[str, *Any*]                                                                                 | :heavy_minus_sign:                                                                               | The input to the workflow. This should be a dictionary that matches the workflow's input schema. |
| `encoded_input`                                                                                  | [OptionalNullable[models.NetworkEncodedInput]](../../models/networkencodedinput.md)              | :heavy_minus_sign:                                                                               | Encoded input to the workflow, used when payload encoding is enabled.                            |
| `wait_for_result`                                                                                | *Optional[bool]*                                                                                 | :heavy_minus_sign:                                                                               | If true, wait for the workflow to complete and return the result directly.                       |
| `timeout_seconds`                                                                                | *OptionalNullable[float]*                                                                        | :heavy_minus_sign:                                                                               | Maximum time to wait for completion when wait_for_result is true.                                |
| `custom_tracing_attributes`                                                                      | Dict[str, *str*]                                                                                 | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `task_queue`                                                                                     | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | The name of the task queue to use for the workflow                                               |
| `deployment_name`                                                                                | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | Name of the deployment to route this execution to                                                |
| `retries`                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                 | :heavy_minus_sign:                                                                               | Configuration to override the default retry behavior of the client.                              |

### Response

**[models.ResponseExecuteWorkflowRegistrationDeprecatedV1WorkflowsVersionsWorkflowVersionIDExecutePost](../../models/responseexecuteworkflowregistrationdeprecatedv1workflowsversionsworkflowversionidexecutepost.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_v1_workflows_workflow_identifier_get

Get Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_v1_workflows__workflow_identifier__get" method="get" path="/v1/workflows/{workflow_identifier}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_v1_workflows_workflow_identifier_get(workflow_identifier="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_identifier`                                               | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowGetResponse](../../models/workflowgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_workflow_v1_workflows_workflow_identifier_put

Update Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="update_workflow_v1_workflows__workflow_identifier__put" method="put" path="/v1/workflows/{workflow_identifier}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.update_workflow_v1_workflows_workflow_identifier_put(workflow_identifier="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_identifier`                                               | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `display_name`                                                      | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | New display name value                                              |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | New description value                                               |
| `available_in_chat_assistant`                                       | *OptionalNullable[bool]*                                            | :heavy_minus_sign:                                                  | Whether to make the workflow available in the chat assistant        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowUpdateResponse](../../models/workflowupdateresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_registration_v1_workflows_registrations_workflow_registration_id_get

Get Workflow Registration

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registration_v1_workflows_registrations__workflow_registration_id__get" method="get" path="/v1/workflows/registrations/{workflow_registration_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registration_v1_workflows_registrations_workflow_registration_id_get(workflow_registration_id="c4d86c40-960f-4e9a-9d6f-ad8342d7aa83", with_workflow=False, include_shared=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_registration_id`                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `with_workflow`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include the workflow definition                          |
| `include_shared`                                                    | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Whether to include shared workflow versions                         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowRegistrationGetResponse](../../models/workflowregistrationgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## ~~get_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_get~~

Get Workflow Registration Deprecated

> :warning: **DEPRECATED**: This will be removed in a future release, please migrate away from it as soon as possible.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registration_deprecated_v1_workflows_versions__workflow_version_id__get" method="get" path="/v1/workflows/versions/{workflow_version_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registration_deprecated_v1_workflows_versions_workflow_version_id_get(workflow_version_id="534a1c4d-4959-4650-92b5-73183571afc4", with_workflow=False, include_shared=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_version_id`                                               | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `with_workflow`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `include_shared`                                                    | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowRegistrationGetResponse](../../models/workflowregistrationgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## archive_workflow_v1_workflows_workflow_identifier_archive_put

Archive Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="archive_workflow_v1_workflows__workflow_identifier__archive_put" method="put" path="/v1/workflows/{workflow_identifier}/archive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.archive_workflow_v1_workflows_workflow_identifier_archive_put(workflow_identifier="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_identifier`                                               | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowArchiveResponse](../../models/workflowarchiveresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unarchive_workflow_v1_workflows_workflow_identifier_unarchive_put

Unarchive Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="unarchive_workflow_v1_workflows__workflow_identifier__unarchive_put" method="put" path="/v1/workflows/{workflow_identifier}/unarchive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.unarchive_workflow_v1_workflows_workflow_identifier_unarchive_put(workflow_identifier="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workflow_identifier`                                               | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WorkflowUnarchiveResponse](../../models/workflowunarchiveresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |