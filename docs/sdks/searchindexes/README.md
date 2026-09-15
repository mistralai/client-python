# Beta.Rag.SearchIndexes

## Overview

### Available Operations

* [get_deployment_summaries](#get_deployment_summaries) - Get Deployment Summaries
* [register_deployment](#register_deployment) - Register (or re-register) a search index
* [unregister_deployment](#unregister_deployment) - Unregister Deployment
* [update_index_metrics](#update_index_metrics) - Update Index Metrics

## get_deployment_summaries

Fetch all indexes available to a user

### Example Usage

<!-- UsageSnippet language="python" operationID="get_deployment_summaries_v1_rag_deployments_get" method="get" path="/v1/rag/deployments" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_deployment_summaries()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetDeploymentSummariesResponse](../../models/getdeploymentsummariesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## register_deployment

Register (or re-register) a search index

### Example Usage

<!-- UsageSnippet language="python" operationID="register_deployment_v1_rag_deployments_put" method="put" path="/v1/rag/deployments" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.register_deployment(name="<value>", deployment={
        "type": "vespa",
        "vespa_version": "<value>",
        "indexes": [],
        "query_url": "https://joyful-granny.info",
    }, status="offline")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                               | Type                                                                                                                    | Required                                                                                                                | Description                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                                  | *str*                                                                                                                   | :heavy_check_mark:                                                                                                      | N/A                                                                                                                     |
| `deployment`                                                                                                            | [models.RegisterDeploymentRequestDeploymentDeployment](../../models/registerdeploymentrequestdeploymentdeployment.md)   | :heavy_check_mark:                                                                                                      | N/A                                                                                                                     |
| `status`                                                                                                                | [Optional[models.RegisterDeploymentRequestDeploymentStatus]](../../models/registerdeploymentrequestdeploymentstatus.md) | :heavy_minus_sign:                                                                                                      | N/A                                                                                                                     |
| `retries`                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                        | :heavy_minus_sign:                                                                                                      | Configuration to override the default retry behavior of the client.                                                     |

### Response

**[models.RegisterSearchIndexResponseIndex](../../models/registersearchindexresponseindex.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unregister_deployment

Delete all information about a deployment

### Example Usage

<!-- UsageSnippet language="python" operationID="unregister_deployment_v1_rag_deployments__deployment_id__delete" method="delete" path="/v1/rag/deployments/{deployment_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.unregister_deployment(deployment_id="240a5e63-fd68-4806-8290-04cce22b4c37")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `deployment_id`                                                     | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_index_metrics

Update the metrics for a given index

### Example Usage

<!-- UsageSnippet language="python" operationID="update_index_metrics_v1_rag_deployments__deployment_id__metrics_put" method="put" path="/v1/rag/deployments/{deployment_id}/metrics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.update_index_metrics(deployment_id="b0c2f463-8aef-437d-83ac-d4bfae874584", request_body={
        "status": "offline",
        "clear_metrics": False,
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `deployment_id`                                                     | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `request_body`                                                      | [models.MetricsData](../../models/metricsdata.md)                   | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |