# Workflows.Schedules

## Overview

### Available Operations

* [get_schedules](#get_schedules) - Get Schedules
* [schedule_workflow](#schedule_workflow) - Schedule Workflow
* [get_schedule](#get_schedule) - Get Schedule
* [unschedule_workflow](#unschedule_workflow) - Unschedule Workflow
* [update_schedule](#update_schedule) - Update Schedule
* [pause_schedule](#pause_schedule) - Pause Schedule
* [resume_schedule](#resume_schedule) - Resume Schedule
* [trigger_schedule](#trigger_schedule) - Trigger Schedule

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

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_name`                                                                                                                 | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | Filter by workflow name                                                                                                         |
| `user_id`                                                                                                                       | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | Filter by user ID. Pass 'current' to resolve to the authenticated user's ID.                                                    |
| `status`                                                                                                                        | [OptionalNullable[models.GetSchedulesV1WorkflowsSchedulesGetStatus]](../../models/getschedulesv1workflowsschedulesgetstatus.md) | :heavy_minus_sign:                                                                                                              | Filter by schedule status: 'active' or 'paused'                                                                                 |
| `page_size`                                                                                                                     | *OptionalNullable[int]*                                                                                                         | :heavy_minus_sign:                                                                                                              | Number of items per page. Omitting this parameter fetches all results at once (deprecated — pass page_size to use pagination).  |
| `next_page_token`                                                                                                               | *OptionalNullable[str]*                                                                                                         | :heavy_minus_sign:                                                                                                              | Token for the next page of results                                                                                              |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[models.GetSchedulesV1WorkflowsSchedulesGetResponse](../../models/getschedulesv1workflowsschedulesgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

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
| `workflow_task_queue`                                                                                                                                                                                                                                                                     | *OptionalNullable[str]*                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                        | : warning: ** DEPRECATED **: This will be removed in a future release, please migrate away from it as soon as possible.<br/><br/>Deprecated. Use deployment_name instead.                                                                                                                 |
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

## get_schedule

Get Schedule

### Example Usage

<!-- UsageSnippet language="python" operationID="get_schedule_v1_workflows_schedules__schedule_id__get" method="get" path="/v1/workflows/schedules/{schedule_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.schedules.get_schedule(schedule_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `schedule_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ScheduleDefinitionOutput](../../models/scheduledefinitionoutput.md)**

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

## update_schedule

Update Schedule

### Example Usage

<!-- UsageSnippet language="python" operationID="update_schedule_v1_workflows_schedules__schedule_id__patch" method="patch" path="/v1/workflows/schedules/{schedule_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.schedules.update_schedule(schedule_id="<id>", schedule={})

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                             | Type                                                                                                                                                                                                                  | Required                                                                                                                                                                                                              | Description                                                                                                                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schedule_id`                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                    | N/A                                                                                                                                                                                                                   |
| `schedule`                                                                                                                                                                                                            | [models.PartialScheduleDefinition](../../models/partialscheduledefinition.md)                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                    | Schedule definition for partial updates.<br/><br/>All fields are optional (inherited from _ScheduleRequestBase). Only explicitly-set<br/>fields are applied during an update; unset fields preserve the existing schedule values. |
| `retries`                                                                                                                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                    | Configuration to override the default retry behavior of the client.                                                                                                                                                   |

### Response

**[models.WorkflowScheduleResponse](../../models/workflowscheduleresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## pause_schedule

Pause Schedule

### Example Usage

<!-- UsageSnippet language="python" operationID="pause_schedule_v1_workflows_schedules__schedule_id__pause_post" method="post" path="/v1/workflows/schedules/{schedule_id}/pause" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.schedules.pause_schedule(schedule_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                              | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `schedule_id`                                                          | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `note`                                                                 | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Optional note recorded in Temporal when pausing or resuming a schedule |
| `retries`                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)       | :heavy_minus_sign:                                                     | Configuration to override the default retry behavior of the client.    |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## resume_schedule

Resume Schedule

### Example Usage

<!-- UsageSnippet language="python" operationID="resume_schedule_v1_workflows_schedules__schedule_id__resume_post" method="post" path="/v1/workflows/schedules/{schedule_id}/resume" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.schedules.resume_schedule(schedule_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                              | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `schedule_id`                                                          | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `note`                                                                 | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Optional note recorded in Temporal when pausing or resuming a schedule |
| `retries`                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)       | :heavy_minus_sign:                                                     | Configuration to override the default retry behavior of the client.    |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## trigger_schedule

Trigger Schedule

### Example Usage

<!-- UsageSnippet language="python" operationID="trigger_schedule_v1_workflows_schedules__schedule_id__trigger_post" method="post" path="/v1/workflows/schedules/{schedule_id}/trigger" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.workflows.schedules.trigger_schedule(schedule_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `schedule_id`                                                                           | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `overlap`                                                                               | [OptionalNullable[models.ScheduleOverlapPolicy]](../../models/scheduleoverlappolicy.md) | :heavy_minus_sign:                                                                      | Optional overlap policy override to use for the immediate trigger.                      |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |