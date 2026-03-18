# Workflows.Schedules

## Overview

### Available Operations

* [get_schedules](#get_schedules) - Get Schedules
* [schedule_workflow](#schedule_workflow) - Schedule Workflow
* [unschedule_workflow](#unschedule_workflow) - Unschedule Workflow

## get_schedules

Get Schedules

### Example Usage

<!-- UsageSnippet language="python" operationID="get_schedules_v1_workflows_schedules_get" method="get" path="/v1/workflows/schedules" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.schedules.get_schedules()

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

## schedule_workflow

Schedule Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="schedule_workflow_v1_workflows_schedules_post" method="post" path="/v1/workflows/schedules" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.schedules.schedule_workflow(schedule={
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

## unschedule_workflow

Unschedule Workflow

### Example Usage

<!-- UsageSnippet language="python" operationID="unschedule_workflow_v1_workflows_schedules__schedule_id__delete" method="delete" path="/v1/workflows/schedules/{schedule_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.schedules.unschedule_workflow(schedule_id="<id>")

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