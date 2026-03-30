# Workflows.Metrics

## Overview

### Available Operations

* [get_workflow_metrics](#get_workflow_metrics) - Get Workflow Metrics

## get_workflow_metrics

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

    res = mistral.workflows.metrics.get_workflow_metrics(workflow_name="<value>")

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