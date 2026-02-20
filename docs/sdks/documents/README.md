# Beta.Libraries.Documents

## Overview

(beta) Libraries API - manage documents in a library.

### Available Operations

* [list](#list) - List documents in a given library.
* [upload](#upload) - Upload a new document.
* [get](#get) - Retrieve the metadata of a specific document.
* [update](#update) - Update the metadata of a specific document.
* [delete](#delete) - Delete a document.
* [text_content](#text_content) - Retrieve the text content of a specific document.
* [status](#status) - Retrieve the processing status of a specific document.
* [get_signed_url](#get_signed_url) - Retrieve the signed URL of a specific document.
* [extracted_text_signed_url](#extracted_text_signed_url) - Retrieve the signed URL of text extracted from a given document.
* [reprocess](#reprocess) - Reprocess a document.

## list

Given a library, lists the document that have been uploaded to that library.

### Example Usage

<!-- UsageSnippet language="python" operationID="ListDocuments" method="get" path="/v1/libraries/{library_id}/documents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.list(library_id="05e1bda5-99b1-4baf-bb03-905d8e094f74", page_size=100, page=0, sort_by="created_at", sort_order="desc")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `search`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `filters_attributes`                                                | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sort_by`                                                           | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sort_order`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListDocumentOut](../../models/listdocumentout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## upload

Given a library, upload a new document to that library. It is queued for processing, it status will change it has been processed. The processing has to be completed in order be discoverable for the library search

### Example Usage

<!-- UsageSnippet language="python" operationID="UploadDocument" method="post" path="/v1/libraries/{library_id}/documents" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.upload(library_id="f973c54e-979a-4464-9d36-8cc31beb21fe", file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `library_id`                                                                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `file`                                                                                                                                                                                                                                                                                                              | [models.File](../../models/file.md)                                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.DocumentOut](../../models/documentout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Given a library and a document in this library, you can retrieve the metadata of that document.

### Example Usage

<!-- UsageSnippet language="python" operationID="GetDocument" method="get" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.get(library_id="f9902d0a-1ea4-4953-be48-52df6edd302a", document_id="c3e12fd9-e840-46f2-8d4a-79985ed36d24")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DocumentOut](../../models/documentout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Given a library and a document in that library, update the name of that document.

### Example Usage

<!-- UsageSnippet language="python" operationID="UpdateDocument" method="put" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.update(library_id="3b900c67-d2b6-4637-93f2-3eff2c85f8dd", document_id="66f935fd-37ec-441f-bca5-b1129befcbca")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `attributes`                                                        | Dict[str, [models.Attributes](../../models/attributes.md)]          | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DocumentOut](../../models/documentout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Given a library and a document in that library, delete that document. The document will be deleted from the library and the search index.

### Example Usage

<!-- UsageSnippet language="python" operationID="DeleteDocument" method="delete" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.libraries.documents.delete(library_id="c728d742-7845-462b-84ad-2aacbaf1c7cf", document_id="ed3f5797-846a-4abe-8e30-39b2fd2323e0")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## text_content

Given a library and a document in that library, you can retrieve the text content of that document if it exists. For documents like pdf, docx and pptx the text content results from our processing using Mistral OCR.

### Example Usage

<!-- UsageSnippet language="python" operationID="GetDocumentTextContent" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/text_content" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.text_content(library_id="12689dc1-50df-4a0d-8202-2757f7a8c141", document_id="9d4057e9-d112-437c-911e-6ee031389739")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DocumentTextContent](../../models/documenttextcontent.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## status

Given a library and a document in that library, retrieve the processing status of that document.

### Example Usage

<!-- UsageSnippet language="python" operationID="GetDocumentStatus" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/status" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.status(library_id="41bb33c4-7e53-453d-bf21-398bb2862772", document_id="416b95cf-19c8-45af-84be-26aaa3ab3666")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ProcessingStatusOut](../../models/processingstatusout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_signed_url

Given a library and a document in that library, retrieve the signed URL of a specific document.The url will expire after 30 minutes and can be accessed by anyone with the link.

### Example Usage

<!-- UsageSnippet language="python" operationID="GetDocumentSignedUrl" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/signed-url" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.get_signed_url(library_id="2dbbe172-1374-41be-b03d-a088c733612e", document_id="b5d88764-47f1-4485-9df1-658775428344")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[str](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## extracted_text_signed_url

Given a library and a document in that library, retrieve the signed URL of text extracted. For documents that are sent to the OCR this returns the result of the OCR queries.

### Example Usage

<!-- UsageSnippet language="python" operationID="GetDocumentExtractedTextSignedUrl" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/extracted-text-signed-url" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.extracted_text_signed_url(library_id="46d040ce-ae2e-4891-a54c-cdab6a8f62d8", document_id="3eddbfe2-3fd7-47f5-984b-b378e6950e37")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[str](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## reprocess

Given a library and a document in that library, reprocess that document, it will be billed again.

### Example Usage

<!-- UsageSnippet language="python" operationID="ReprocessDocument" method="post" path="/v1/libraries/{library_id}/documents/{document_id}/reprocess" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.libraries.documents.reprocess(library_id="76d357e4-d891-40c6-9d1e-6d6ce5056ee0", document_id="09798d2b-8f46-46c6-9765-8054a82a4bb2")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `document_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |