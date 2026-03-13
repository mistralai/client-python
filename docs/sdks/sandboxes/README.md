# Beta.Sandboxes

## Overview

(beta) Sandboxes API

### Available Operations

* [list](#list) - List Sandboxes
* [create](#create) - Create Sandbox
* [get](#get) - Get Sandbox
* [delete](#delete) - Delete Sandbox
* [execute_command](#execute_command) - Execute Command

## list

List all active sandboxes for the authenticated user and workspace.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_sandboxes_v1_sandboxes_get" method="get" path="/v1/sandboxes" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.sandboxes.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.APIResponseSandboxListData](../../models/apiresponsesandboxlistdata.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

Create a new sandbox instance.

Backend is configured server-side via environment variables.
Client can optionally override sandbox_type and ttl_seconds.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_sandbox_v1_sandboxes_post" method="post" path="/v1/sandboxes" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.sandboxes.create()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                    | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `ttl_seconds`                                                                | *OptionalNullable[int]*                                                      | :heavy_minus_sign:                                                           | Time-to-live in seconds (max: 1 hour). Uses server default if not specified. |
| `image`                                                                      | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Container image for the sandbox. Default: python:3.13-slim                   |
| `cpu_request`                                                                | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | CPU request (e.g., '100m')                                                   |
| `cpu_limit`                                                                  | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | CPU limit (e.g., '500m')                                                     |
| `memory_request`                                                             | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Memory request (e.g., '128Mi')                                               |
| `memory_limit`                                                               | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Memory limit (e.g., '512Mi')                                                 |
| `storage_limit`                                                              | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Ephemeral storage limit (e.g., '1Gi')                                        |
| `setup_script`                                                               | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Bash script to execute during sandbox initialization                         |
| `envs`                                                                       | Dict[str, *str*]                                                             | :heavy_minus_sign:                                                           | Environment variables to set in the sandbox                                  |
| `secrets`                                                                    | Dict[str, *str*]                                                             | :heavy_minus_sign:                                                           | Secret environment variables to set in the sandbox                           |
| `retries`                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)             | :heavy_minus_sign:                                                           | Configuration to override the default retry behavior of the client.          |

### Response

**[models.APIResponseSandboxData](../../models/apiresponsesandboxdata.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get information about a specific sandbox.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_sandbox_v1_sandboxes__sandbox_id__get" method="get" path="/v1/sandboxes/{sandbox_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.sandboxes.get(sandbox_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `sandbox_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.APIResponseSandboxData](../../models/apiresponsesandboxdata.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete a sandbox instance and cancel its cleanup workflow.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_sandbox_v1_sandboxes__sandbox_id__delete" method="delete" path="/v1/sandboxes/{sandbox_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.sandboxes.delete(sandbox_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `sandbox_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.APIResponseNoneType](../../models/apiresponsenonetype.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## execute_command

Execute a command in a sandbox.

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_command_v1_sandboxes__sandbox_id__execute_post" method="post" path="/v1/sandboxes/{sandbox_id}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.sandboxes.execute_command(sandbox_id="<id>", command="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `sandbox_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `command`                                                           | *str*                                                               | :heavy_check_mark:                                                  | Command to execute                                                  |
| `timeout`                                                           | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | Optional timeout in seconds (integer)                               |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.APIResponseExecutionData](../../models/apiresponseexecutiondata.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |