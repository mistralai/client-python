# Beta.Rag.SearchIndexes

## Overview

### Available Operations

* [get_indexes](#get_indexes) - Get Index Summaries
* [register](#register) - Register (or re-register) a search index
* [unregister](#unregister) - Unregister Search Index
* [update_index_metrics](#update_index_metrics) - Update Index Metrics

## get_indexes

Fetch all indexes available to a user

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_summaries_v1_rag_indexes_get" method="get" path="/v1/rag/indexes" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_indexes()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSearchIndexSummaryResponse](../../models/getsearchindexsummaryresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## register

Register (or re-register) a search index

### Example Usage

<!-- UsageSnippet language="python" operationID="register_search_index_v1_rag_indexes_put" method="put" path="/v1/rag/indexes" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.register(name="<value>", index={
        "type": "vespa",
        "k8s_cluster": "<value>",
        "k8s_namespace": "<value>",
        "vespa_instance_name": "<value>",
        "vespa_version": "<value>",
        "schemas": [
            {
                "name": "<value>",
                "fields": [],
                "sd": "<value>",
            },
        ],
        "query_url": "https://shiny-range.com/",
    }, status="offline")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                       | Type                                                                                                            | Required                                                                                                        | Description                                                                                                     |
| --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                          | *str*                                                                                                           | :heavy_check_mark:                                                                                              | N/A                                                                                                             |
| `index`                                                                                                         | [models.RegisterSearchIndexRequestIndexIndex](../../models/registersearchindexrequestindexindex.md)             | :heavy_check_mark:                                                                                              | N/A                                                                                                             |
| `status`                                                                                                        | [Optional[models.RegisterSearchIndexRequestIndexStatus]](../../models/registersearchindexrequestindexstatus.md) | :heavy_minus_sign:                                                                                              | N/A                                                                                                             |
| `retries`                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                | :heavy_minus_sign:                                                                                              | Configuration to override the default retry behavior of the client.                                             |

### Response

**[models.RegisterSearchIndexResponseIndex](../../models/registersearchindexresponseindex.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unregister

Delete all information about an index

### Example Usage

<!-- UsageSnippet language="python" operationID="unregister_search_index_v1_rag_indexes__index_id__delete" method="delete" path="/v1/rag/indexes/{index_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.unregister(index_id="545b10f3-a041-4786-9d25-5a7b7ca281e2")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
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

<!-- UsageSnippet language="python" operationID="update_index_metrics_v1_rag_indexes__index_id__metrics_put" method="put" path="/v1/rag/indexes/{index_id}/metrics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.update_index_metrics(index_id="8ab7ca9a-64c2-4c00-b9ba-9a6ce4268033", request_body={
        "status": "online",
        "document_count": 951726,
        "schema_metrics": [
            {
                "name": "<value>",
                "document_count": 381376,
            },
        ],
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `request_body`                                                      | [models.MetricsData](../../models/metricsdata.md)                   | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |