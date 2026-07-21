# Workflows.Deployments

## Overview

### Available Operations

* [list_deployments](#list_deployments) - List Deployments
* [create_deployment](#create_deployment) - Create Deployment
* [update_deployment](#update_deployment) - Update Deployment
* [delete_deployment](#delete_deployment) - Delete Deployment
* [get_deployment](#get_deployment) - Get Deployment
* [stop_deployment](#stop_deployment) - Stop Deployment
* [start_deployment](#start_deployment) - Start Deployment
* [restart_deployment](#restart_deployment) - Restart Deployment
* [get_deployment_logs](#get_deployment_logs) - Get Deployment Logs
* [stream_deployment_logs](#stream_deployment_logs) - Stream Deployment Logs

## list_deployments

List Deployments

### Example Usage

<!-- UsageSnippet language="python" operationID="list_deployments_v1_workflows_deployments_get" method="get" path="/v1/workflows/deployments" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.list_deployments(active_only=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `active_only`                                                           | *Optional[bool]*                                                        | :heavy_minus_sign:                                                      | N/A                                                                     |
| `is_hardened`                                                           | *OptionalNullable[bool]*                                                | :heavy_minus_sign:                                                      | Filter deployments by hardened status                                   |
| `workflow_name`                                                         | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | N/A                                                                     |
| `search`                                                                | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | Filter deployments by name or ID prefix                                 |
| `limit`                                                                 | *OptionalNullable[int]*                                                 | :heavy_minus_sign:                                                      | Maximum number of deployments to return                                 |
| `cursor`                                                                | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | Cursor from a previous response for pagination                          |
| `workspace_id`                                                          | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | Workspace ID to scope the request to. Defaults to the caller's context. |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.DeploymentListResponse](../../models/deploymentlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create_deployment

Create Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="create_deployment_v1_workflows_deployments_post" method="post" path="/v1/workflows/deployments" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.create_deployment(name="<value>", spec={
        "github_url": "https://ugly-parade.com",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `name`                                                                                        | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `spec`                                                                                        | [models.DeploymentWorkerSpecInput](../../models/deploymentworkerspecinput.md)                 | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `resources`                                                                                   | [OptionalNullable[models.DeploymentResourceConfig]](../../models/deploymentresourceconfig.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_deployment

Update Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="update_deployment_v1_workflows_deployments__name__patch" method="patch" path="/v1/workflows/deployments/{name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.update_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                    | *str*                                                                                                     | :heavy_check_mark:                                                                                        | N/A                                                                                                       |
| `spec`                                                                                                    | [OptionalNullable[models.WorkflowsWorkerSpecUpdate]](../../models/workflowsworkerspecupdate.md)           | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `resources`                                                                                               | [OptionalNullable[models.DeploymentResourceConfigUpdate]](../../models/deploymentresourceconfigupdate.md) | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_deployment

Delete Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_deployment_v1_workflows_deployments__name__delete" method="delete" path="/v1/workflows/deployments/{name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.delete_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_deployment

Get Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="get_deployment_v1_workflows_deployments__name__get" method="get" path="/v1/workflows/deployments/{name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.get_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeploymentDetailResponse](../../models/deploymentdetailresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## stop_deployment

Stop Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="stop_deployment_v1_workflows_deployments__name__stop_post" method="post" path="/v1/workflows/deployments/{name}/stop" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.stop_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## start_deployment

Start Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="start_deployment_v1_workflows_deployments__name__start_post" method="post" path="/v1/workflows/deployments/{name}/start" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.start_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## restart_deployment

Restart Deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="restart_deployment_v1_workflows_deployments__name__restart_post" method="post" path="/v1/workflows/deployments/{name}/restart" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.restart_deployment(name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedDeploymentResponse](../../models/manageddeploymentresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_deployment_logs

Retrieve logs for a deployment (across all of its workers).

Use `after`/`before`/`order` on the first request to set the time range and sort order; for
the next pages pass the `cursor` from the previous response (it remembers the range and order).

### Example Usage

<!-- UsageSnippet language="python" operationID="get_deployment_logs" method="get" path="/v1/workflows/deployments/{name}/logs" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.get_deployment_logs(name="<value>", order="asc", limit=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `name`                                                                                   | *str*                                                                                    | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `worker_name`                                                                            | *OptionalNullable[str]*                                                                  | :heavy_minus_sign:                                                                       | Filter logs by worker name                                                               |
| `workflow_name`                                                                          | *OptionalNullable[str]*                                                                  | :heavy_minus_sign:                                                                       | Filter logs by workflow name                                                             |
| `after`                                                                                  | [date](https://docs.python.org/3/library/datetime.html#date-objects)                     | :heavy_minus_sign:                                                                       | Only return logs at or after this timestamp                                              |
| `before`                                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects)                     | :heavy_minus_sign:                                                                       | Only return logs before this timestamp                                                   |
| `order`                                                                                  | [Optional[models.GetDeploymentLogsOrder]](../../models/getdeploymentlogsorder.md)        | :heavy_minus_sign:                                                                       | First-page sort order: 'asc' (oldest first) or 'desc'. Ignored when `cursor` is set.     |
| `cursor`                                                                                 | *OptionalNullable[str]*                                                                  | :heavy_minus_sign:                                                                       | Pagination cursor from a previous response's `next_cursor`; carries the window and order |
| `limit`                                                                                  | *Optional[int]*                                                                          | :heavy_minus_sign:                                                                       | Maximum number of logs to return                                                         |
| `retries`                                                                                | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                         | :heavy_minus_sign:                                                                       | Configuration to override the default retry behavior of the client.                      |

### Response

**[models.DeploymentLogSearchResponse](../../models/deploymentlogsearchresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## stream_deployment_logs

Stream logs for a deployment (all of its workers) via SSE.

Resume cursor comes from the `Last-Event-ID` header or `last_event_id` query param (header wins)
and takes precedence over `after`; omit all to tail from the deployment start.

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_deployment_logs" method="get" path="/v1/workflows/deployments/{name}/logs/stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.deployments.stream_deployment_logs(name="<value>")

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                        | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `name`                                                                           | *str*                                                                            | :heavy_check_mark:                                                               | N/A                                                                              |
| `worker_name`                                                                    | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Filter logs by worker name                                                       |
| `workflow_name`                                                                  | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Filter logs by workflow name                                                     |
| `after`                                                                          | [date](https://docs.python.org/3/library/datetime.html#date-objects)             | :heavy_minus_sign:                                                               | Start a fresh stream at this timestamp (ignored when resuming via last_event_id) |
| `last_event_id`                                                                  | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Resume from this cursor (a prior response's SSE id)                              |
| `retries`                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                 | :heavy_minus_sign:                                                               | Configuration to override the default retry behavior of the client.              |

### Response

**[Union[eventstreaming.EventStream[models.StreamDeploymentLogsResponseBody], eventstreaming.EventStreamAsync[models.StreamDeploymentLogsResponseBody]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |