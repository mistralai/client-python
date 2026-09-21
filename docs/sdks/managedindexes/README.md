# Beta.Rag.ManagedIndexes

## Overview

### Available Operations

* [create](#create) - Create a managed index
* [list](#list) - List managed indexes
* [get](#get) - Get a managed index
* [update](#update) - Update a managed index schema
* [delete](#delete) - Delete a managed index
* [ingest_documents](#ingest_documents) - Ingest documents into a managed index
* [delete_documents](#delete_documents) - Delete documents from a managed index
* [search](#search) - Search a managed index
* [navigate](#navigate) - Navigate to adjacent chunks
* [read](#read) - Read chunks within a span
* [grep](#grep) - Grep for a pattern within a source
* [get_chunk](#get_chunk) - Get a single chunk by id

## create

Reserves a managed search index and starts asynchronous backing-table provisioning. Poll the returned Location until status is ready or failed.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_index_v1_rag_managed_indexes_post" method="post" path="/v1/rag/managed_indexes" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.create(name="<value>", config=models.ManagedIndexConfig(
        embedding=models.CustomEmbeddingModel(
            name="<value>",
            dimensions=543021,
        ),
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                 | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `name`                                                                    | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `config`                                                                  | [models.ManagedIndexConfig](../../models/managedindexconfig.md)           | :heavy_check_mark:                                                        | N/A                                                                       |
| `schema_`                                                                 | [Optional[models.ManagedIndexFields]](../../models/managedindexfields.md) | :heavy_minus_sign:                                                        | N/A                                                                       |
| `retries`                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)          | :heavy_minus_sign:                                                        | Configuration to override the default retry behavior of the client.       |

### Response

**[models.CreateIndexV1RagManagedIndexesPostResponse](../../models/createindexv1ragmanagedindexespostresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

Lists all managed search indexes for the current workspace.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_indexes_v1_rag_managed_indexes_get" method="get" path="/v1/rag/managed_indexes" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.list(page_size=20)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `page_size`                                                                       | *Optional[int]*                                                                   | :heavy_minus_sign:                                                                | Maximum number of indexes to return                                               |
| `page_token`                                                                      | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | Cursor returned as next_page_token by the previous page                           |
| `name`                                                                            | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | Case-insensitive substring to match against index names                           |
| `status`                                                                          | [OptionalNullable[models.ManagedIndexStatus]](../../models/managedindexstatus.md) | :heavy_minus_sign:                                                                | Status to match                                                                   |
| `creator_id`                                                                      | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | Creator ID to match                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.ListIndexesV1RagManagedIndexesGetResponse](../../models/listindexesv1ragmanagedindexesgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Returns the managed search index with the given name.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_index_v1_rag_managed_indexes__index_name__get" method="get" path="/v1/rag/managed_indexes/{index_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.get(index_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedIndexResponse](../../models/managedindexresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Records a new schema for the managed search index and applies it asynchronously. The index keeps serving its current schema until the new one is on disk; poll it until status is ready. Additive only: the new schema must keep every field the current one has.

### Example Usage

<!-- UsageSnippet language="python" operationID="update_index_v1_rag_managed_indexes__index_name__put" method="put" path="/v1/rag/managed_indexes/{index_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.update(index_name="<value>", schema={})

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `schema_`                                                           | [models.ManagedIndexFields](../../models/managedindexfields.md)     | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ManagedIndexResponse](../../models/managedindexresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

Marks the managed search index for deletion and returns it with status deleting. The backing table is dropped asynchronously; poll the index until it returns 404.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_index_v1_rag_managed_indexes__index_name__delete" method="delete" path="/v1/rag/managed_indexes/{index_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.delete(index_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeleteManagedIndexResponse](../../models/deletemanagedindexresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## ingest_documents

Validates and persists documents. Always returns 200; each document is reported as accepted or rejected in the response body.

### Example Usage

<!-- UsageSnippet language="python" operationID="ingest_documents_v1_rag_managed_indexes__index_name__documents_post" method="post" path="/v1/rag/managed_indexes/{index_name}/documents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.ingest_documents(index_name="<value>", documents=[
        {
            "key": "<value>",
        },
        {
            "key": "<value>",
            "key1": "<value>",
            "key2": "<value>",
        },
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `documents`                                                         | List[Dict[str, *Any*]]                                              | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.IngestDocumentsResponse](../../models/ingestdocumentsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_documents

Deletes the given documents by id. Returns the ids actually removed and, in `missing`, any requested ids that were not present.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_documents_v1_rag_managed_indexes__index_name__documents_delete" method="delete" path="/v1/rag/managed_indexes/{index_name}/documents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.delete_documents(index_name="<value>", document_ids=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_ids`                                                      | List[*str*]                                                         | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeleteDocumentsResponse](../../models/deletedocumentsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## search

Runs an approximate-nearest-neighbor vector search over the index and returns matching chunks, closest-first.

### Example Usage

<!-- UsageSnippet language="python" operationID="search_index_v1_rag_managed_indexes__index_name__search_post" method="post" path="/v1/rag/managed_indexes/{index_name}/search" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.search(index_name="<value>", retriever=models.NearestNeighbourRetriever(
        top_k=20,
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `index_name`                                                            | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `retriever`                                                             | [models.SearchRequestRetriever](../../models/searchrequestretriever.md) | :heavy_check_mark:                                                      | N/A                                                                     |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.SearchResponse](../../models/searchresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## navigate

Returns the chunks adjacent to a position within a source, in reading order. NEXT fetches chunks at or after the end offset; PREVIOUS fetches chunks before the start offset. A 200 with an empty list means the source exists but no chunk falls in the requested direction; a 404 means the source has no chunks at all.

### Example Usage

<!-- UsageSnippet language="python" operationID="navigate_index_v1_rag_managed_indexes__index_name__navigate_post" method="post" path="/v1/rag/managed_indexes/{index_name}/navigate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.navigate(index_name="<value>", source_id="<id>", start_offset=506558, end_offset=410700, direction="previous", top_k=1, content_type="content")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `source_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `start_offset`                                                      | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `end_offset`                                                        | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `direction`                                                         | [models.NavigationDirection](../../models/navigationdirection.md)   | :heavy_check_mark:                                                  | N/A                                                                 |
| `top_k`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `content_type`                                                      | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.NavigationResponse](../../models/navigationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## read

Returns the chunks of a source whose span falls within [start_offset, end_offset). Either bound may be omitted to leave that side open. A 200 with an empty list means the source exists but no chunk falls in the range; a 404 means the source has no chunks at all.

### Example Usage

<!-- UsageSnippet language="python" operationID="read_index_v1_rag_managed_indexes__index_name__read_post" method="post" path="/v1/rag/managed_indexes/{index_name}/read" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.read(index_name="<value>", source_id="<id>", top_k=20, content_type="content")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `source_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `start_offset`                                                      | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `end_offset`                                                        | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `top_k`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `content_type`                                                      | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.NavigationResponse](../../models/navigationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## grep

Lexical substring match within a single source, in reading order. PHRASE mode matches the pattern literally (whitespace-sensitive, case-insensitive); TERM mode requires every whitespace-split token present in any order. A 200 with an empty list means the source exists but no chunk matched; a 404 means the source has no chunks at all.

### Example Usage

<!-- UsageSnippet language="python" operationID="grep_index_v1_rag_managed_indexes__index_name__grep_post" method="post" path="/v1/rag/managed_indexes/{index_name}/grep" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.grep(index_name="<value>", source_id="<id>", pattern="<value>", top_k=5, content_type="content")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `source_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `pattern`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `mode`                                                              | [Optional[models.GrepMode]](../../models/grepmode.md)               | :heavy_minus_sign:                                                  | N/A                                                                 |
| `top_k`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `content_type`                                                      | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.NavigationResponse](../../models/navigationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_chunk

Returns a single chunk by its canonical id. A 404 means no chunk with that id exists in the index.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chunk_index_v1_rag_managed_indexes__index_name__chunks__chunk_id__get" method="get" path="/v1/rag/managed_indexes/{index_name}/chunks/{chunk_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.rag.managed_indexes.get_chunk(index_name="<value>", chunk_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `index_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `chunk_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.NavigationResponse](../../models/navigationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |