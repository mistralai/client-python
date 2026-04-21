# Workflows

## Overview

### Available Operations

* [get_workflows](#get_workflows) - Get Workflows
* [get_workflow_registrations](#get_workflow_registrations) - Get Workflow Registrations
* [execute_workflow](#execute_workflow) - Execute Workflow
* [~~execute_workflow_registration~~](#execute_workflow_registration) - Execute Workflow Registration :warning: **Deprecated**
* [get_workflow](#get_workflow) - Get Workflow
* [update_workflow](#update_workflow) - Update Workflow
* [get_workflow_registration](#get_workflow_registration) - Get Workflow Registration
* [archive_workflow](#archive_workflow) - Archive Workflow
* [unarchive_workflow](#unarchive_workflow) - Unarchive Workflow

## get_workflows

Get Workflows

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflows_v1_workflows_get" method="get" path="/v1/workflows" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflows(active_only=False, include_shared=True, limit=50)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                              | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `active_only`                                                                          | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Whether to only return active workflows                                                |
| `include_shared`                                                                       | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Whether to include shared workflows                                                    |
| `available_in_chat_assistant`                                                          | *OptionalNullable[bool]*                                                               | :heavy_minus_sign:                                                                     | Whether to only return workflows compatible with chat assistant                        |
| `archived`                                                                             | *OptionalNullable[bool]*                                                               | :heavy_minus_sign:                                                                     | Filter by archived state. False=exclude archived, True=only archived, None=include all |
| `cursor`                                                                               | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | The cursor for pagination                                                              |
| `limit`                                                                                | *Optional[int]*                                                                        | :heavy_minus_sign:                                                                     | The maximum number of workflows to return                                              |
| `retries`                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                       | :heavy_minus_sign:                                                                     | Configuration to override the default retry behavior of the client.                    |

### Response

**[models.GetWorkflowsV1WorkflowsGetResponse](../../models/getworkflowsv1workflowsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow_registrations

Get Workflow Registrations

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registrations_v1_workflows_registrations_get" method="get" path="/v1/workflows/registrations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registrations(active_only=False, include_shared=True, with_workflow=False, limit=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                              | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `workflow_id`                                                                          | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | The workflow ID to filter by                                                           |
| `task_queue`                                                                           | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | The task queue to filter by                                                            |
| `active_only`                                                                          | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Whether to only return active workflows versions                                       |
| `include_shared`                                                                       | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Whether to include shared workflow versions                                            |
| `workflow_search`                                                                      | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | The workflow name to filter by                                                         |
| `archived`                                                                             | *OptionalNullable[bool]*                                                               | :heavy_minus_sign:                                                                     | Filter by archived state. False=exclude archived, True=only archived, None=include all |
| `with_workflow`                                                                        | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Whether to include the workflow definition                                             |
| `available_in_chat_assistant`                                                          | *OptionalNullable[bool]*                                                               | :heavy_minus_sign:                                                                     | Whether to only return workflows compatible with chat assistant                        |
| `limit`                                                                                | *Optional[int]*                                                                        | :heavy_minus_sign:                                                                     | The maximum number of workflows versions to return                                     |
| `cursor`                                                                               | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | The cursor for pagination                                                              |
| `retries`                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                       | :heavy_minus_sign:                                                                     | Configuration to override the default retry behavior of the client.                    |

### Response

**[models.WorkflowRegistrationListResponse](../../models/workflowregistrationlistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## execute_workflow

Execute Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_workflow_v1_workflows__workflow_identifier__execute_post" method="post" path="/v1/workflows/{workflow_identifier}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.execute_workflow(workflow_identifier="<value>", wait_for_result=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                         | Type                                                                                                                                                              | Required                                                                                                                                                          | Description                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_identifier`                                                                                                                                             | *str*                                                                                                                                                             | :heavy_check_mark:                                                                                                                                                | N/A                                                                                                                                                               |
| `execution_id`                                                                                                                                                    | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | Allows you to specify a custom execution ID. If not provided, a random ID will be generated.                                                                      |
| `input`                                                                                                                                                           | *OptionalNullable[Any]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | The input to the workflow. This should be a dictionary or a BaseModel that matches the workflow's input schema.                                                   |
| `encoded_input`                                                                                                                                                   | [OptionalNullable[models.NetworkEncodedInput]](../../models/networkencodedinput.md)                                                                               | :heavy_minus_sign:                                                                                                                                                | Encoded input to the workflow, used when payload encoding is enabled.                                                                                             |
| `wait_for_result`                                                                                                                                                 | *Optional[bool]*                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | If true, wait for the workflow to complete and return the result directly.                                                                                        |
| `timeout_seconds`                                                                                                                                                 | *OptionalNullable[float]*                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                | Maximum time to wait for completion when wait_for_result is true.                                                                                                 |
| `custom_tracing_attributes`                                                                                                                                       | Dict[str, *str*]                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `extensions`                                                                                                                                                      | Dict[str, *Any*]                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | Plugin-specific data to propagate into WorkflowContext.extensions at execution time.                                                                              |
| `task_queue`                                                                                                                                                      | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | : warning: ** DEPRECATED **: This will be removed in a future release, please migrate away from it as soon as possible.<br/><br/>Deprecated. Use deployment_name instead. |
| `deployment_name`                                                                                                                                                 | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | Name of the deployment to route this execution to                                                                                                                 |
| `retries`                                                                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                  | :heavy_minus_sign:                                                                                                                                                | Configuration to override the default retry behavior of the client.                                                                                               |

### Response

**[models.ResponseExecuteWorkflowV1WorkflowsWorkflowIdentifierExecutePost](../../models/responseexecuteworkflowv1workflowsworkflowidentifierexecutepost.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## ~~execute_workflow_registration~~

Execute Workflow Registration

> :warning: **DEPRECATED**: This will be removed in a future release, please migrate away from it as soon as possible.

### Example Usage

<!-- UsageSnippet language="python" operationID="execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post" method="post" path="/v1/workflows/registrations/{workflow_registration_id}/execute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.execute_workflow_registration(workflow_registration_id="de11d76a-e0fb-44dd-abd9-2e75fc275b94", wait_for_result=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                         | Type                                                                                                                                                              | Required                                                                                                                                                          | Description                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_registration_id`                                                                                                                                        | *str*                                                                                                                                                             | :heavy_check_mark:                                                                                                                                                | N/A                                                                                                                                                               |
| `execution_id`                                                                                                                                                    | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | Allows you to specify a custom execution ID. If not provided, a random ID will be generated.                                                                      |
| `input`                                                                                                                                                           | *OptionalNullable[Any]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | The input to the workflow. This should be a dictionary or a BaseModel that matches the workflow's input schema.                                                   |
| `encoded_input`                                                                                                                                                   | [OptionalNullable[models.NetworkEncodedInput]](../../models/networkencodedinput.md)                                                                               | :heavy_minus_sign:                                                                                                                                                | Encoded input to the workflow, used when payload encoding is enabled.                                                                                             |
| `wait_for_result`                                                                                                                                                 | *Optional[bool]*                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | If true, wait for the workflow to complete and return the result directly.                                                                                        |
| `timeout_seconds`                                                                                                                                                 | *OptionalNullable[float]*                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                | Maximum time to wait for completion when wait_for_result is true.                                                                                                 |
| `custom_tracing_attributes`                                                                                                                                       | Dict[str, *str*]                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `extensions`                                                                                                                                                      | Dict[str, *Any*]                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | Plugin-specific data to propagate into WorkflowContext.extensions at execution time.                                                                              |
| `task_queue`                                                                                                                                                      | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | : warning: ** DEPRECATED **: This will be removed in a future release, please migrate away from it as soon as possible.<br/><br/>Deprecated. Use deployment_name instead. |
| `deployment_name`                                                                                                                                                 | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | Name of the deployment to route this execution to                                                                                                                 |
| `retries`                                                                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                  | :heavy_minus_sign:                                                                                                                                                | Configuration to override the default retry behavior of the client.                                                                                               |

### Response

**[models.ResponseExecuteWorkflowRegistrationV1WorkflowsRegistrationsWorkflowRegistrationIDExecutePost](../../models/responseexecuteworkflowregistrationv1workflowsregistrationsworkflowregistrationidexecutepost.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_workflow

Get Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_v1_workflows__workflow_identifier__get" method="get" path="/v1/workflows/{workflow_identifier}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow(workflow_identifier="<value>")

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

## update_workflow

Update Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="update_workflow_v1_workflows__workflow_identifier__put" method="put" path="/v1/workflows/{workflow_identifier}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.update_workflow(workflow_identifier="<value>")

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

## get_workflow_registration

Get Workflow Registration

### Example Usage

<!-- UsageSnippet language="python" operationID="get_workflow_registration_v1_workflows_registrations__workflow_registration_id__get" method="get" path="/v1/workflows/registrations/{workflow_registration_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflow_registration(workflow_registration_id="c4d86c40-960f-4e9a-9d6f-ad8342d7aa83", with_workflow=False, include_shared=True)

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

## archive_workflow

Archive Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="archive_workflow_v1_workflows__workflow_identifier__archive_put" method="put" path="/v1/workflows/{workflow_identifier}/archive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.archive_workflow(workflow_identifier="<value>")

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

## unarchive_workflow

Unarchive Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="unarchive_workflow_v1_workflows__workflow_identifier__unarchive_put" method="put" path="/v1/workflows/{workflow_identifier}/unarchive" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.unarchive_workflow(workflow_identifier="<value>")

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