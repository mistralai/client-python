# Beta.Rag.SearchIndexes

## Overview

### Available Operations

* [register](#register) - Register (or re-register) a search index
* [get_index_summaries](#get_index_summaries) - Get Index Summaries
* [unregister](#unregister) - Unregister Search Index
* [update_index_metrics](#update_index_metrics) - Update Index Metrics
* [get_index_detail](#get_index_detail) - Get Index Details
* [get_index_summary](#get_index_summary) - Get Index Summary
* [generate_index_summary](#generate_index_summary) - Generate a summary field for an index
* [set_index_summary](#set_index_summary) - Set Index Summary
* [get_schema_summary](#get_schema_summary) - Get Schema Summary
* [generate_schema_summary](#generate_schema_summary) - Generate a summary field for a schema
* [set_schema_summary](#set_schema_summary) - Set Schema Summary
* [get_index_schema_detail](#get_index_schema_detail) - Get Index Schema Detail
* [get_index_schema_file](#get_index_schema_file) - Get Index Schema File
* [document_lookup](#document_lookup) - Document Lookup
* [documents_fetch](#documents_fetch) - Document Fetch

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

## get_index_summary

Retrieve the summary field for an index if it exists

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_summary_v1_rag_indexes_index__index_id__summary_field__language__get" method="get" path="/v1/rag/indexes/index/{index_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_index_summary(index_id="d83e93f2-1d03-4133-90d2-fae51463c71e", language="pt_br")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                               | Type                                                                                                                                                                    | Required                                                                                                                                                                | Description                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                              | *str*                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `language`                                                                                                                                                              | [models.GetIndexSummaryV1RagIndexesIndexIndexIDSummaryFieldLanguageGetLanguage](../../models/getindexsummaryv1ragindexesindexindexidsummaryfieldlanguagegetlanguage.md) | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `retries`                                                                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                        | :heavy_minus_sign:                                                                                                                                                      | Configuration to override the default retry behavior of the client.                                                                                                     |

### Response

**[models.GetSummaryResponseSummary](../../models/getsummaryresponsesummary.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## generate_index_summary

Streams a summary for the index in chunks of json.

The first chunk contains metadata for the summary, the following contain
chunks of 'content' that should be joined together to form a full summary.

### Example Usage

<!-- UsageSnippet language="python" operationID="generate_index_summary_v1_rag_indexes_index__index_id__summary_field__language__post" method="post" path="/v1/rag/indexes/index/{index_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.generate_index_summary(index_id="b0cfd77c-9cc3-46b6-ad70-1024386259b9", language="pl")

    with res as jsonl_stream:
        for event in jsonl_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                                                                           | Type                                                                                                                                                                                | Required                                                                                                                                                                            | Description                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                                          | *str*                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                  | N/A                                                                                                                                                                                 |
| `language`                                                                                                                                                                          | [models.GenerateIndexSummaryV1RagIndexesIndexIndexIDSummaryFieldLanguagePostLanguage](../../models/generateindexsummaryv1ragindexesindexindexidsummaryfieldlanguagepostlanguage.md) | :heavy_check_mark:                                                                                                                                                                  | N/A                                                                                                                                                                                 |
| `retries`                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                 |

### Response

**[Union[jsonl.JsonLStream[models.GenerateIndexSummaryV1RagIndexesIndexIndexIDSummaryFieldLanguagePostSummaryStreamTypes], jsonl.JsonLStreamAsync[models.GenerateIndexSummaryV1RagIndexesIndexIndexIDSummaryFieldLanguagePostSummaryStreamTypes]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## set_index_summary

Update the summary field for an index

### Example Usage

<!-- UsageSnippet language="python" operationID="set_index_summary_v1_rag_indexes_index__index_id__summary_field__language__put" method="put" path="/v1/rag/indexes/index/{index_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.set_index_summary(index_id="e199a723-75b3-43fe-98fb-5d576435c591", language="pt_br", content="<value>", status="handwritten", translated=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                               | Type                                                                                                                                                                    | Required                                                                                                                                                                | Description                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                              | *str*                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `language`                                                                                                                                                              | [models.SetIndexSummaryV1RagIndexesIndexIndexIDSummaryFieldLanguagePutLanguage](../../models/setindexsummaryv1ragindexesindexindexidsummaryfieldlanguageputlanguage.md) | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `content`                                                                                                                                                               | *str*                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `status`                                                                                                                                                                | [models.UpdateSummaryRequestSummaryStatus](../../models/updatesummaryrequestsummarystatus.md)                                                                           | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `translated`                                                                                                                                                            | *bool*                                                                                                                                                                  | :heavy_check_mark:                                                                                                                                                      | N/A                                                                                                                                                                     |
| `retries`                                                                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                        | :heavy_minus_sign:                                                                                                                                                      | Configuration to override the default retry behavior of the client.                                                                                                     |

### Response

**[Any](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_schema_summary

Retrieve the summary field for a schema if it exists

### Example Usage

<!-- UsageSnippet language="python" operationID="get_schema_summary_v1_rag_indexes_index__index_id__schemas_schema__schema_id__summary_field__language__get" method="get" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.get_schema_summary(index_id="077fb72c-10cd-442d-832e-51fd35136195", schema_id="39f80401-7fc3-4ade-8b1c-b2cd613bab20", language="en")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                           | Type                                                                                                                                                                                                                | Required                                                                                                                                                                                                            | Description                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                                                                          | *str*                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `schema_id`                                                                                                                                                                                                         | *str*                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `language`                                                                                                                                                                                                          | [models.GetSchemaSummaryV1RagIndexesIndexIndexIDSchemasSchemaSchemaIDSummaryFieldLanguageGetLanguage](../../models/getschemasummaryv1ragindexesindexindexidschemasschemaschemaidsummaryfieldlanguagegetlanguage.md) | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `retries`                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                 |

### Response

**[models.GetSummaryResponseSummary](../../models/getsummaryresponsesummary.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## generate_schema_summary

Streams a summary for the schema in chunks of json.

The first chunk contains metadata for the summary, the following contain
chunks of 'content' that should be joined together to form a full summary.

### Example Usage

<!-- UsageSnippet language="python" operationID="generate_schema_summary_post_v1_rag_indexes_index__index_id__schemas_schema__schema_id__summary_field__language__post" method="post" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.generate_schema_summary(index_id="582076c8-276e-4a50-b7a6-2f266925a448", schema_id="5c471724-f36e-41cc-a302-af4f92ea7413", language="it")

    with res as jsonl_stream:
        for event in jsonl_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                                                                                                                               | Type                                                                                                                                                                                                                                    | Required                                                                                                                                                                                                                                | Description                                                                                                                                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                                                                                              | *str*                                                                                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                                                                                      | N/A                                                                                                                                                                                                                                     |
| `schema_id`                                                                                                                                                                                                                             | *str*                                                                                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                                                                                      | N/A                                                                                                                                                                                                                                     |
| `language`                                                                                                                                                                                                                              | [models.GenerateSchemaSummaryPostV1RagIndexesIndexIndexIDSchemasSchemaSchemaIDSummaryFieldLanguagePostLanguage](../../models/generateschemasummarypostv1ragindexesindexindexidschemasschemaschemaidsummaryfieldlanguagepostlanguage.md) | :heavy_check_mark:                                                                                                                                                                                                                      | N/A                                                                                                                                                                                                                                     |
| `retries`                                                                                                                                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                        | :heavy_minus_sign:                                                                                                                                                                                                                      | Configuration to override the default retry behavior of the client.                                                                                                                                                                     |

### Response

**[Union[jsonl.JsonLStream[models.GenerateSchemaSummaryPostV1RagIndexesIndexIndexIDSchemasSchemaSchemaIDSummaryFieldLanguagePostSummaryStreamTypes], jsonl.JsonLStreamAsync[models.GenerateSchemaSummaryPostV1RagIndexesIndexIndexIDSchemasSchemaSchemaIDSummaryFieldLanguagePostSummaryStreamTypes]]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## set_schema_summary

Update the summary field for an index

### Example Usage

<!-- UsageSnippet language="python" operationID="set_schema_summary_v1_rag_indexes_index__index_id__schemas_schema__schema_id__summary_field__language__put" method="put" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/summary_field/{language}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.set_schema_summary(index_id="d22ebdfa-6465-4f25-9a27-3e59d85ee544", schema_id="cc29f795-986b-483d-a658-acb000a16f70", language="nl", content="<value>", status="generated_confirmed", translated=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                           | Type                                                                                                                                                                                                                | Required                                                                                                                                                                                                            | Description                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index_id`                                                                                                                                                                                                          | *str*                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `schema_id`                                                                                                                                                                                                         | *str*                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `language`                                                                                                                                                                                                          | [models.SetSchemaSummaryV1RagIndexesIndexIndexIDSchemasSchemaSchemaIDSummaryFieldLanguagePutLanguage](../../models/setschemasummaryv1ragindexesindexindexidschemasschemaschemaidsummaryfieldlanguageputlanguage.md) | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `content`                                                                                                                                                                                                           | *str*                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `status`                                                                                                                                                                                                            | [models.UpdateSummaryRequestSummaryStatus](../../models/updatesummaryrequestsummarystatus.md)                                                                                                                       | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `translated`                                                                                                                                                                                                        | *bool*                                                                                                                                                                                                              | :heavy_check_mark:                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                 |
| `retries`                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                 |

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

## document_lookup

Fetch stored information about a retrievable element stored in an index

### Example Usage

<!-- UsageSnippet language="python" operationID="document_lookup_v1_rag_indexes_index__index_id__schemas_schema__schema_id__retrievables_retrievable__document_id__get" method="get" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/retrievables/retrievable/{document_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.document_lookup(index_id="77308a24-2d8e-4392-9ab4-38770b2bb993", schema_id="1fe735e7-4ec0-4264-b715-12a944fe2b87", document_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | the native ID in the underlying index                               |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.VespaGetRetrievableResponseRetrievable](../../models/vespagetretrievableresponseretrievable.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## documents_fetch

Fetch a few stored retrievable elements from the index/schema

### Example Usage

<!-- UsageSnippet language="python" operationID="document_fetch_v1_rag_indexes_index__index_id__schemas_schema__schema_id__retrievables_get" method="get" path="/v1/rag/indexes/index/{index_id}/schemas/schema/{schema_id}/retrievables" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.search_indexes.documents_fetch(index_id="7c9f7007-1a54-48fd-b6da-93e91f31f6aa", schema_id="7eb7703c-1b80-4ecc-8a8b-288b43e1f30e")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `group_id`                                                          | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Only retrieve from this group                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.VespaGetRetrievableResponseRetrievable]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |