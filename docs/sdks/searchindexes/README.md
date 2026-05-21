# Beta.Rag.SearchIndexes

## Overview

### Available Operations

* [list](#list) - Get Search Indexes
* [register](#register) - Register Search Index

## list

Get Search Indexes

### Example Usage

<!-- UsageSnippet language="python" operationID="get_search_indexes_v1_rag_search_index_get" method="get" path="/v1/rag/search_index" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.SearchIndexResponse]](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## register

Register Search Index

### Example Usage

<!-- UsageSnippet language="python" operationID="register_search_index_v1_rag_search_index_put" method="put" path="/v1/rag/search_index" -->
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
        "schemas": [],
    }, status="offline")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                 | Type                                                                                                      | Required                                                                                                  | Description                                                                                               |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                    | *str*                                                                                                     | :heavy_check_mark:                                                                                        | N/A                                                                                                       |
| `index`                                                                                                   | [models.CreateSearchIndexInfoRequestIndex](../../models/createsearchindexinforequestindex.md)             | :heavy_check_mark:                                                                                        | N/A                                                                                                       |
| `document_count`                                                                                          | *OptionalNullable[int]*                                                                                   | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `status`                                                                                                  | [Optional[models.CreateSearchIndexInfoRequestStatus]](../../models/createsearchindexinforequeststatus.md) | :heavy_minus_sign:                                                                                        | N/A                                                                                                       |
| `retries`                                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                          | :heavy_minus_sign:                                                                                        | Configuration to override the default retry behavior of the client.                                       |

### Response

**[models.SearchIndexResponse](../../models/searchindexresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |