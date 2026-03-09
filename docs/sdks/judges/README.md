# Beta.Observability.Judges

## Overview

### Available Operations

* [create](#create) - Create a new judge
* [list](#list) - Get judges with optional filtering and search
* [fetch](#fetch) - Get judge by id
* [delete](#delete) - Delete a judge
* [update](#update) - Update a judge

## create

Create a new judge

### Example Usage

<!-- UsageSnippet language="python" operationID="create_judge_v1_observability_judges_post" method="post" path="/v1/observability/judges" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.create(name="<value>", description="border freely down whenever broadly whenever restructure catalyze after", model_name="<value>", output={
        "type": "REGRESSION",
        "min": 0,
        "min_description": "<value>",
        "max": 1,
        "max_description": "<value>",
    }, instructions="<value>", tools=[
        "<value 1>",
        "<value 2>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `name`                                                                      | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `description`                                                               | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `model_name`                                                                | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `output`                                                                    | [models.CreateJudgeRequestOutput](../../models/createjudgerequestoutput.md) | :heavy_check_mark:                                                          | N/A                                                                         |
| `instructions`                                                              | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `tools`                                                                     | List[*str*]                                                                 | :heavy_check_mark:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.Judge](../../models/judge.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list

Get judges with optional filtering and search

### Example Usage

<!-- UsageSnippet language="python" operationID="get_judges_v1_observability_judges_get" method="get" path="/v1/observability/judges" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.list(page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `type_filter`                                                       | List[[models.JudgeOutputType](../../models/judgeoutputtype.md)]     | :heavy_minus_sign:                                                  | Filter by judge output types                                        |
| `model_filter`                                                      | List[*str*]                                                         | :heavy_minus_sign:                                                  | Filter by model names                                               |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `q`                                                                 | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListJudgesResponse](../../models/listjudgesresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch

Get judge by id

### Example Usage

<!-- UsageSnippet language="python" operationID="get_judge_by_id_v1_observability_judges__judge_id__get" method="get" path="/v1/observability/judges/{judge_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.fetch(judge_id="19ae5cf8-2ade-4a40-b9d2-730aaebe8429")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `judge_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Judge](../../models/judge.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete

Delete a judge

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_judge_v1_observability_judges__judge_id__delete" method="delete" path="/v1/observability/judges/{judge_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.judges.delete(judge_id="80deecde-e10f-409c-a13a-c242d3760f6e")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `judge_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update

Update a judge

### Example Usage

<!-- UsageSnippet language="python" operationID="update_judge_v1_observability_judges__judge_id__put" method="put" path="/v1/observability/judges/{judge_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.judges.update(judge_id="9f28c7db-1fb7-4e1c-b137-d7039561ddb7", name="<value>", description="noteworthy and unless", model_name="<value>", output={
        "type": "REGRESSION",
        "min": 0,
        "min_description": "<value>",
        "max": 1,
        "max_description": "<value>",
    }, instructions="<value>", tools=[])

    # Use the SDK ...

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `judge_id`                                                                  | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `name`                                                                      | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `description`                                                               | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `model_name`                                                                | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `output`                                                                    | [models.UpdateJudgeRequestOutput](../../models/updatejudgerequestoutput.md) | :heavy_check_mark:                                                          | N/A                                                                         |
| `instructions`                                                              | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `tools`                                                                     | List[*str*]                                                                 | :heavy_check_mark:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |