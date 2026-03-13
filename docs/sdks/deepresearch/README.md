# Beta.Deepresearch

## Overview

### Available Operations

* [submit](#submit) - Submits a task for execution.
* [get](#get) - Get task
* [cancel](#cancel) - Cancel task
* [skip](#skip) - Skip task execution
* [export](#export) - Export task
* [debug](#debug) - Debug a deep research task by returning the complete completion payload.
* [get_stream](#get_stream) - Get task

## submit

Submits a task for execution.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_submit" method="post" path="/v1/tasks/deep_research" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.submit(query="<value>", steps=[
        "<value 1>",
        "<value 2>",
        "<value 3>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                             | Type                                                                                  | Required                                                                              | Description                                                                           |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `query`                                                                               | *str*                                                                                 | :heavy_check_mark:                                                                    | N/A                                                                                   |
| `steps`                                                                               | List[*str*]                                                                           | :heavy_check_mark:                                                                    | N/A                                                                                   |
| `task_type`                                                                           | [Optional[models.TaskType]](../../models/tasktype.md)                                 | :heavy_minus_sign:                                                                    | N/A                                                                                   |
| `model`                                                                               | *OptionalNullable[str]*                                                               | :heavy_minus_sign:                                                                    | N/A                                                                                   |
| `metadata`                                                                            | [OptionalNullable[models.DeepResearchMetadata]](../../models/deepresearchmetadata.md) | :heavy_minus_sign:                                                                    | N/A                                                                                   |
| `retries`                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                      | :heavy_minus_sign:                                                                    | Configuration to override the default retry behavior of the client.                   |

### Response

**[models.DeepResearchSubmitTaskResponse](../../models/deepresearchsubmittaskresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get task status.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_get" method="get" path="/v1/tasks/deep_research/{task_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.get(task_id="<id>", stream=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `stream`                                                            | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeepResearchTask](../../models/deepresearchtask.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## cancel

Cancel a task.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_cancel" method="post" path="/v1/tasks/deep_research/{task_id}/cancel" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.cancel(task_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## skip

Skip task execution.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_skip" method="post" path="/v1/tasks/deep_research/{task_id}/skip" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.skip(task_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## export

Export a task as PDF.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_export" method="get" path="/v1/tasks/deep_research/{task_id}/export" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.export(task_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeepResearchExportResponse](../../models/deepresearchexportresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## debug

Debug a deep research task by returning the complete completion payload.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deep_research_debug" method="get" path="/v1/tasks/deep_research/debug/{task_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.debug(task_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Dict[str, Any]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_stream

Get task status.

### Example Usage

<!-- UsageSnippet language="python" operationID="tasks_api_v1_tasks_deepresearch_get_stream" method="get" path="/v1/tasks/deep_research/{task_id}#stream" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.deepresearch.get_stream(task_id="<id>", stream=True)

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `task_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `stream`                                                            | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Union[eventstreaming.EventStream[models.DeepResearchTaskEvents], eventstreaming.EventStreamAsync[models.DeepResearchTaskEvents]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |