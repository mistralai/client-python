# Beta.Observability.Evaluations.Records

## Overview

### Available Operations

* [get](#get) - Get a specific record from an evaluation run
* [search](#search) - Search records for an evaluation run with content filters

## get

Get a specific record from an evaluation run

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_run_record_v2_v1_observability_evaluation_runs_v2__run_id__records__record_id__get" method="get" path="/v1/observability/evaluation-runs_v2/{run_id}/records/{record_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.records.get(run_id="4561f251-c638-4a33-8739-db876b032f73", record_id="24b40e66-4e0d-4788-bb5a-df09239c7ba9")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `run_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `record_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRunRecordV2Response](../../models/evaluationrunrecordv2response.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## search

Search records for an evaluation run with content filters

### Example Usage

<!-- UsageSnippet language="python" operationID="search_evaluation_run_records_v2_v1_observability_evaluation_runs_v2__run_id__records_search_post" method="post" path="/v1/observability/evaluation-runs_v2/{run_id}/records/search" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.records.search(run_id="3ec2a158-4bb7-4020-8a52-0f64a2745094", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `run_id`                                                                                      | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `page_size`                                                                                   | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `page`                                                                                        | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `input_filters`                                                                               | [OptionalNullable[models.ContentSearchFilterGroup]](../../models/contentsearchfiltergroup.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `output_filters`                                                                              | [OptionalNullable[models.ContentSearchFilterGroup]](../../models/contentsearchfiltergroup.md) | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `score_filters`                                                                               | [OptionalNullable[models.ScoreFilterGroup]](../../models/scorefiltergroup.md)                 | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `goal_filters`                                                                                | [OptionalNullable[models.GoalStatusFilterGroup]](../../models/goalstatusfiltergroup.md)       | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `sort`                                                                                        | [OptionalNullable[models.Sort]](../../models/sort.md)                                         | :heavy_minus_sign:                                                                            | N/A                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |

### Response

**[models.ListEvaluationRunRecordsResponse](../../models/listevaluationrunrecordsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |