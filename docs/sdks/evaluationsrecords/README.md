# Beta.Observability.Evaluations.Records

## Overview

(beta) Manage records of a given evaluation

### Available Operations

* [fetch](#fetch) - Get an evaluation record
* [delete](#delete) - Delete an evaluation record

## fetch

Get an evaluation record

### Example Usage

<!-- UsageSnippet language="python" operationID="get_evaluation_record_by_id_v1_observability_evaluation_records__evaluation_record_id__get" method="get" path="/v1/observability/evaluation-records/{evaluation_record_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.records.fetch(evaluation_record_id="d616b941-2140-4247-bf1f-3786e481597a")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_record_id`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EvaluationRecord](../../models/evaluationrecord.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## delete

Delete an evaluation record

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_evaluation_record_v1_observability_evaluation_records__evaluation_record_id__delete" method="delete" path="/v1/observability/evaluation-records/{evaluation_record_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.observability.evaluations.records.delete(evaluation_record_id="fff268ed-e4d8-4d50-b83b-b349d9565fa3")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `evaluation_record_id`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |