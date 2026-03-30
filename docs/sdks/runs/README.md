# Workflows.Runs

## Overview

### Available Operations

* [list_runs](#list_runs) - List Runs
* [get_run](#get_run) - Get Run
* [get_run_history](#get_run_history) - Get Run History

## list_runs

List Runs

### Example Usage

<!-- UsageSnippet language="python" operationID="list_runs_v1_workflows_runs_get" method="get" path="/v1/workflows/runs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.runs.list_runs(page_size=50)

    while res is not None:
        # Handle items

        res = res.next()

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

**[models.ListRunsV1WorkflowsRunsGetResponse](../../models/listrunsv1workflowsrunsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_run

Get Run

### Example Usage

<!-- UsageSnippet language="python" operationID="get_run_v1_workflows_runs__run_id__get" method="get" path="/v1/workflows/runs/{run_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.runs.get_run(run_id="553b071e-3d04-46aa-aa9a-0fca61dc60fa")

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

## get_run_history

Get Run History

### Example Usage

<!-- UsageSnippet language="python" operationID="get_run_history_v1_workflows_runs__run_id__history_get" method="get" path="/v1/workflows/runs/{run_id}/history" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.runs.get_run_history(run_id="f7296489-0212-4239-9e35-12fabfe8cd11", decode_payloads=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `decode_payloads`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |