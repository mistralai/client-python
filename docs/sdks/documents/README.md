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

<!-- UsageSnippet language="python" operationID="libraries_documents_list_v1" method="get" path="/v1/libraries/{library_id}/documents" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.list(library_id="5c3ca4cd-62bc-4c71-ad8a-1531ae80d078", page_size=100, page=0, sort_by="created_at", sort_order="desc")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_upload_v1" method="post" path="/v1/libraries/{library_id}/documents" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.upload(library_id="a02150d9-5ee0-4877-b62c-28b1fcdf3b76", file={
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

<!-- UsageSnippet language="python" operationID="libraries_documents_get_v1" method="get" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.get(library_id="03d908c8-90a1-44fd-bf3a-8490fb7c9a03", document_id="90973aec-0508-4375-8b00-91d732414745")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_update_v1" method="put" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.update(library_id="3ddd8d93-dca5-4a6d-980d-173226c35742", document_id="2a25e44c-b160-40ca-b5c2-b65fb2fcae34")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_delete_v1" method="delete" path="/v1/libraries/{library_id}/documents/{document_id}" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.libraries.documents.delete(library_id="005daae9-d42e-407d-82d7-2261c6a1496c", document_id="edc236b0-baff-49a9-884b-4ca36a258da4")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_get_text_content_v1" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/text_content" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.text_content(library_id="1d177215-3b6b-45ba-9fa9-baf773223bec", document_id="60214c91-2aba-4692-a4e6-a53365de8caf")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_get_status_v1" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/status" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.status(library_id="e6906f70-368f-4155-80da-c1718f01bc43", document_id="2c904915-d831-4e9d-a345-8ce405bcef66")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_get_signed_url_v1" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/signed-url" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.get_signed_url(library_id="23cf6904-a602-4ee8-9f5b-8efc557c336d", document_id="48598486-df71-4994-acbb-1133c72efa8c")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_get_extracted_text_signed_url_v1" method="get" path="/v1/libraries/{library_id}/documents/{document_id}/extracted-text-signed-url" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.documents.extracted_text_signed_url(library_id="a6f15de3-1e82-4f95-af82-851499042ef8", document_id="9749d4f9-24e5-4ca2-99a3-a406863f805d")

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

<!-- UsageSnippet language="python" operationID="libraries_documents_reprocess_v1" method="post" path="/v1/libraries/{library_id}/documents/{document_id}/reprocess" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.libraries.documents.reprocess(library_id="51b29371-de8f-4ba4-932b-a0bafb3a7f64", document_id="3052422c-49ca-45ac-a918-cadb35d61fd8")

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