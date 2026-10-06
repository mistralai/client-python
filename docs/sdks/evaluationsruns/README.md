# Beta.Observability.Evaluations.Runs

## Overview

### Available Operations

* [search](#search) - Search evaluation runs with filters
* [search_all](#search_all) - Search evaluation runs across all evaluations
* [get](#get) - Get a specific evaluation run by ID
* [get_statistics](#get_statistics) - Get statistics for a specific evaluation run
* [compute_statistics](#compute_statistics) - Compute statistics for a specific evaluation run with optional filters

## search

Search evaluation runs with filters

### Example Usage

<!-- UsageSnippet language="python" operationID="search_evaluation_runs_v2_v1_observability_evaluations_v2__evaluation_slug__runs_search_post" method="post" path="/v1/observability/evaluations_v2/{evaluation_slug}/runs/search" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.search(evaluation_slug="<value>", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `evaluation_slug`                                                                       | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `page_size`                                                                             | *Optional[int]*                                                                         | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `page`                                                                                  | *Optional[int]*                                                                         | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `run_ids`                                                                               | List[*str*]                                                                             | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `evaluation_ids`                                                                        | List[*str*]                                                                             | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `creator_ids`                                                                           | List[*str*]                                                                             | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `project_ids`                                                                           | List[*str*]                                                                             | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `ownership`                                                                             | [OptionalNullable[models.RunOwnershipFilter]](../../models/runownershipfilter.md)       | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `tags`                                                                                  | [OptionalNullable[models.TagFilter]](../../models/tagfilter.md)                         | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `score_filters`                                                                         | [OptionalNullable[models.ScoreFilterGroup]](../../models/scorefiltergroup.md)           | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `goal_filters`                                                                          | [OptionalNullable[models.GoalStatusFilterGroup]](../../models/goalstatusfiltergroup.md) | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `system`                                                                                | [OptionalNullable[models.SystemFilter]](../../models/systemfilter.md)                   | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `metadata`                                                                              | [OptionalNullable[models.MetadataFilterGroup]](../../models/metadatafiltergroup.md)     | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

### Response

**[models.ListEvaluationRunsResponse](../../models/listevaluationrunsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## search_all

Search evaluation runs across all evaluations

### Example Usage

<!-- UsageSnippet language="python" operationID="search_all_evaluation_runs_v2_v1_observability_evaluation_runs_v2_search_post" method="post" path="/v1/observability/evaluation-runs_v2/search" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.search_all(page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `page_size`                                                                                   | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `page`                                                                                        | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `evaluation_run_filter_input`                                                                 | [OptionalNullable[models.EvaluationRunFilterInput]](../../models/evaluationrunfilterinput.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.SearchAllEvaluationRunsResponse](../../models/searchallevaluationrunsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get

Get a specific evaluation run by ID

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_run_v2_v1_observability_evaluation_runs_v2__run_id__get" method="get" path="/v1/observability/evaluation-runs_v2/{run_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.get(run_id="c120b634-146a-4ae3-bd38-b7a168c4c8ce")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRunV2Response](../../models/evaluationrunv2response.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get_statistics

Get statistics for a specific evaluation run

### Example Usage

<!-- UsageSnippet language="python" operationID="get_single_evaluation_run_statistics_v2_v1_observability_evaluation_runs_v2__run_id__statistics_get" method="get" path="/v1/observability/evaluation-runs_v2/{run_id}/statistics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.get_statistics(run_id="a38473a2-532a-4cb8-9320-a7f617d16595")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RunStatisticsResponse](../../models/runstatisticsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## compute_statistics

Compute statistics for a specific evaluation run with optional filters

### Example Usage

<!-- UsageSnippet language="python" operationID="compute_filtered_run_statistics_v2_v1_observability_evaluation_runs_v2__run_id__statistics_compute_post" method="post" path="/v1/observability/evaluation-runs_v2/{run_id}/statistics/compute" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.runs.compute_statistics(run_id="c5e1142f-de29-45b2-b29c-fe37e6509c8a")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `run_id`                                                                                      | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `input_filters`                                                                               | [OptionalNullable[models.ContentSearchFilterGroup]](../../models/contentsearchfiltergroup.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `output_filters`                                                                              | [OptionalNullable[models.ContentSearchFilterGroup]](../../models/contentsearchfiltergroup.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `score_filters`                                                                               | [OptionalNullable[models.ScoreFilterGroup]](../../models/scorefiltergroup.md)                 | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `goal_filters`                                                                                | [OptionalNullable[models.GoalStatusFilterGroup]](../../models/goalstatusfiltergroup.md)       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `sort`                                                                                        | [OptionalNullable[models.Sort]](../../models/sort.md)                                         | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.RunStatisticsResponse](../../models/runstatisticsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |