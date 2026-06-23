# Beta.Rag.SearchIndexes

## Overview

### Available Operations

* [register](#register) - Register (or re-register) a search index
* [get_index_summaries](#get_index_summaries) - Get Index Summaries
* [unregister](#unregister) - Unregister Search Index
* [update_index_metrics](#update_index_metrics) - Update Index Metrics
* [get_index_detail](#get_index_detail) - Get Index Details
* [set_index_summary](#set_index_summary) - Set Index Summary
* [get_index_schema_detail](#get_index_schema_detail) - Get Index Schema Detail
* [set_schema_summary](#set_schema_summary) - Set Schema Summary
* [get_index_schema_file](#get_index_schema_file) - Get Index Schema File

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

## get_index_summaries

Fetch summary view of all indexes available to a user

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_summaries_v1_rag_indexes_summary_get" method="get" path="/v1/rag/indexes/summary" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_index_summaries()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.GetSearchIndexSummaryResponseIndex]](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## unregister

Delete all information about an index

### Example Usage

<!-- UsageSnippet language="python" operationID="unregister_search_index_v1_rag_indexes_index__index_id__delete" method="delete" path="/v1/rag/indexes/index/{index_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.unregister(index_id="0e59f390-f2e4-428e-a81c-c9c2f2ced09e")

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

<!-- UsageSnippet language="python" operationID="update_index_metrics_v1_rag_indexes_index__index_id__metrics_put" method="put" path="/v1/rag/indexes/index/{index_id}/metrics" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.update_index_metrics(index_id="cb562a81-38ce-49a7-86ec-592676de32a8", request_body={
        "status": "online",
        "document_count": 864436,
        "schema_metrics": [
            {
                "name": "<value>",
                "document_count": 109412,
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

## get_index_detail

Get a detailed view of the stored data for a single index

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_details_v1_rag_indexes_index__index_id__detail_get" method="get" path="/v1/rag/indexes/index/{index_id}/detail" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_index_detail(index_id="f6ffec01-1f00-47ec-bf94-a08bdc049edc")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSearchIndexDetailResponseIndex](../../models/getsearchindexdetailresponseindex.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## set_index_summary

Update the summary field for an index

### Example Usage

<!-- UsageSnippet language="python" operationID="set_index_summary_v1_rag_indexes_index__index_id__summary_field_put" method="put" path="/v1/rag/indexes/index/{index_id}/summary_field" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.set_index_summary(index_id="e77375ab-1284-42f3-9224-d42f3c120e57", summary="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `summary`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_index_schema_detail

Get a detailed view of the stored information for a schema

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_schema_detail_v1_rag_indexes_index__index_id__schemas_schema__schema_id__detail_get" method="get" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/detail" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_index_schema_detail(index_id="af850b81-3290-4f41-83af-f0d2ac1b070d", schema_id="fc2825a7-a8ef-4bec-9729-f7486e8327cb")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSearchIndexSchemaDetailResponseSchemaModel](../../models/getsearchindexschemadetailresponseschemamodel.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## set_schema_summary

Update the summary field for an index

### Example Usage

<!-- UsageSnippet language="python" operationID="set_schema_summary_v1_rag_indexes_index__index_id__schemas_schema__schema_id__summary_field_put" method="put" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/summary_field" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.set_schema_summary(index_id="1a7d0662-5542-453a-8120-6e22a4fa6187", schema_id="bb5f0528-b652-4c47-81eb-574cb5c442a5", summary="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `summary`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_index_schema_file

Get Index Schema File

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_schema_file_v1_rag_indexes_index__index_id__schemas_schema__schema_id__file_get" method="get" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/file" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_index_schema_file(index_id="252c6de5-4c9b-43b5-8c30-54524a59cb57", schema_id="93166e46-2e3c-4b20-b9a5-8607304372d2")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSearchIndexSchemaSDFileResponseSDFile](../../models/getsearchindexschemasdfileresponsesdfile.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |