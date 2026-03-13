# Beta.Observability.Judges

## Overview

(beta) Define LLM judges to annotate or evaluate conversations

### Available Operations

* [create](#create) - Create a new judge
* [list](#list) - Get judges with optional filtering and search
* [fetch_metadata](#fetch_metadata) - Get available judge types and models for filtering
* [fetch](#fetch) - Get judge by id
* [delete](#delete) - Delete a judge
* [update](#update) - Update a judge
* [check_save_availability](#check_save_availability) - Get whether judge can be saved
* [generate_partially_hydrated_template](#generate_partially_hydrated_template) - Get partially hydrated template of judges
* [validate_template](#validate_template) - Validate Jinja2 template syntax for judge instructions template

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

| Parameter                                                                 | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `name`                                                                    | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `description`                                                             | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `model_name`                                                              | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `output`                                                                  | [models.PostJudgeInSchemaOutput](../../models/postjudgeinschemaoutput.md) | :heavy_check_mark:                                                        | N/A                                                                       |
| `instructions`                                                            | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `tools`                                                                   | List[*str*]                                                               | :heavy_check_mark:                                                        | N/A                                                                       |
| `retries`                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)          | :heavy_minus_sign:                                                        | Configuration to override the default retry behavior of the client.       |

### Response

**[models.JudgePreview](../../models/judgepreview.md)**

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

**[models.JudgePreviews](../../models/judgepreviews.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_metadata

Get available judge types and models for filtering

### Example Usage

<!-- UsageSnippet language="python" operationID="get_judges_metadata_v1_observability_judges_metadata_get" method="get" path="/v1/observability/judges/metadata" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.fetch_metadata()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JudgeMetadata](../../models/judgemetadata.md)**

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

**[models.JudgePreview](../../models/judgepreview.md)**

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

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `judge_id`                                                              | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `name`                                                                  | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `description`                                                           | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `model_name`                                                            | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `output`                                                                | [models.PutJudgeInSchemaOutput](../../models/putjudgeinschemaoutput.md) | :heavy_check_mark:                                                      | N/A                                                                     |
| `instructions`                                                          | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `tools`                                                                 | List[*str*]                                                             | :heavy_check_mark:                                                      | N/A                                                                     |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## check_save_availability

Get whether judge can be saved

### Example Usage

<!-- UsageSnippet language="python" operationID="get_can_save_judge_v1_observability_can_save_judge_post" method="post" path="/v1/observability/can-save-judge" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.check_save_availability(name="<value>", description="mortally inure shanghai", model_name="<value>", output={
        "type": "CLASSIFICATION",
        "options": [
            {
                "value": "<value>",
                "description": "incidentally geez impassioned",
            },
        ],
    }, instructions="<value>", tools=[
        "<value 1>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                       | Type                                                                            | Required                                                                        | Description                                                                     |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `name`                                                                          | *str*                                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `description`                                                                   | *str*                                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `model_name`                                                                    | *str*                                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `output`                                                                        | [models.CanSaveJudgeInSchemaOutput](../../models/cansavejudgeinschemaoutput.md) | :heavy_check_mark:                                                              | N/A                                                                             |
| `instructions`                                                                  | *str*                                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `tools`                                                                         | List[*str*]                                                                     | :heavy_check_mark:                                                              | N/A                                                                             |
| `judge_id`                                                                      | *OptionalNullable[str]*                                                         | :heavy_minus_sign:                                                              | N/A                                                                             |
| `retries`                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                | :heavy_minus_sign:                                                              | Configuration to override the default retry behavior of the client.             |

### Response

**[models.CanSaveJudge](../../models/cansavejudge.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## generate_partially_hydrated_template

Get partially hydrated template of judges

### Example Usage

<!-- UsageSnippet language="python" operationID="get_judges_template_v1_observability_judge_template_post" method="post" path="/v1/observability/judge-template" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.generate_partially_hydrated_template()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `output`                                                                                                  | [OptionalNullable[models.GetJudgeTemplateInSchemaOutput]](../../models/getjudgetemplateinschemaoutput.md) | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `instructions`                                                                                            | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `tools`                                                                                                   | List[*str*]                                                                                               | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `model_name`                                                                                              | *OptionalNullable[str]*                                                                                   | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `messages`                                                                                                | List[Dict[str, *Any*]]                                                                                    | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `response`                                                                                                | List[Dict[str, *Any*]]                                                                                    | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `properties`                                                                                              | Dict[str, *Any*]                                                                                          | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |

### Response

**[models.JudgeTemplate](../../models/judgetemplate.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## validate_template

Validate Jinja2 template syntax for judge instructions template

### Example Usage

<!-- UsageSnippet language="python" operationID="validate_judge_instructions_v1_observability_judge_template_validate_post" method="post" path="/v1/observability/judge-template/validate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.judges.validate_template(instructions="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `instructions`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ValidateJudgeInstructions](../../models/validatejudgeinstructions.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |