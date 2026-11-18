# Beta.Observability.Evaluations.Scorers

## Overview

### Available Operations

* [list](#list) - List scorers
* [create](#create) - Create a scorer
* [get](#get) - Get a scorer by slug
* [update](#update) - Edit a scorer

## list

List scorers

### Example Usage

<!-- UsageSnippet language="python" operationID="list_scorers_v1_observability_scorers_get" method="get" path="/v1/observability/scorers" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY"),
) as mistral:

    res = mistral.beta.observability.evaluations.scorers.list(created_by_me=False, ootb=False, page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `created_by_me`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Only return scorers created by the current user                     |
| `ootb`                                                              | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | Only return out-of-the-box scorers                                  |
| `q`                                                                 | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Case-insensitive filter on scorer slug, name, or description        |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListScorersResponse](../../models/listscorersresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## create

Create a scorer

### Example Usage

<!-- UsageSnippet language="python" operationID="create_scorer_v1_observability_scorers_post" method="post" path="/v1/observability/scorers" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY"),
) as mistral:

    res = mistral.beta.observability.evaluations.scorers.create(name="<value>", kind="llm_judge", config={
        "model": "A4",
        "prompt_template": "<value>",
        "output_spec": {
            "type": "categorical",
            "labels": [
                "<value 1>",
                "<value 2>",
            ],
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `kind`                                                              | [models.ScorerKind](../../models/scorerkind.md)                     | :heavy_check_mark:                                                  | N/A                                                                 |
| `config`                                                            | [models.LlmJudgeConfig](../../models/llmjudgeconfig.md)             | :heavy_check_mark:                                                  | N/A                                                                 |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Scorer](../../models/scorer.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get

Get a scorer by slug

### Example Usage

<!-- UsageSnippet language="python" operationID="get_scorer_v1_observability_scorers__scorer_slug__get" method="get" path="/v1/observability/scorers/{scorer_slug}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY"),
) as mistral:

    res = mistral.beta.observability.evaluations.scorers.get(scorer_slug="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `scorer_slug`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Scorer](../../models/scorer.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## update

Edit a scorer

### Example Usage

<!-- UsageSnippet language="python" operationID="edit_scorer_v1_observability_scorers__scorer_slug__patch" method="patch" path="/v1/observability/scorers/{scorer_slug}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY"),
) as mistral:

    res = mistral.beta.observability.evaluations.scorers.update(scorer_slug="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                 | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `scorer_slug`                                                             | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `name`                                                                    | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | N/A                                                                       |
| `description`                                                             | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | N/A                                                                       |
| `config`                                                                  | [OptionalNullable[models.LlmJudgeConfig]](../../models/llmjudgeconfig.md) | :heavy_minus_sign:                                                        | N/A                                                                       |
| `retries`                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)          | :heavy_minus_sign:                                                        | Configuration to override the default retry behavior of the client.       |

### Response

**[models.Scorer](../../models/scorer.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |