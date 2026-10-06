# Beta.Observability.Evaluations.Optimizations

## Overview

### Available Operations

* [list](#list) - List optimizations with optional filters
* [get](#get) - Get an optimization by id (with its anchored evaluation + project)
* [list_trials](#list_trials) - List an optimization's trials with their observation runs (paginated)

## list

List optimizations with optional filters

### Example Usage

<!-- UsageSnippet language="python" operationID="list_optimizations_v1_observability_optimizations_get" method="get" path="/v1/observability/optimizations" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.optimizations.list(page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `project`                                                           | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Filter by project slug                                              |
| `evaluation`                                                        | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Filter by evaluation slug                                           |
| `status`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Filter by lifecycle status                                          |
| `algorithm`                                                         | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Filter by algorithm                                                 |
| `tags`                                                              | List[*str*]                                                         | :heavy_minus_sign:                                                  | Filter by tags                                                      |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListOptimizationsResponse](../../models/listoptimizationsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## get

Get an optimization by id (with its anchored evaluation + project)

### Example Usage

<!-- UsageSnippet language="python" operationID="get_optimization_v1_observability_optimizations__optimization_id__get" method="get" path="/v1/observability/optimizations/{optimization_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.optimizations.get(optimization_id="fd7cc96b-0c32-4b79-b7e4-63786d9dcfea")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `optimization_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.OptimizationDetail](../../models/optimizationdetail.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## list_trials

List an optimization's trials with their observation runs (paginated)

### Example Usage

<!-- UsageSnippet language="python" operationID="list_optimization_trials_v1_observability_optimizations__optimization_id__trials_get" method="get" path="/v1/observability/optimizations/{optimization_id}/trials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.evaluations.optimizations.list_trials(optimization_id="54622d5d-6e77-4a86-9908-87b1f8f16424", page_size=50, page=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `optimization_id`                                                   | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListOptimizationTrialsResponse](../../models/listoptimizationtrialsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |