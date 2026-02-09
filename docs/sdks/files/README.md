# Files

## Overview

Files API

### Available Operations

* [upload](#upload) - Upload File
* [list](#list) - List Files
* [retrieve](#retrieve) - Retrieve File
* [delete](#delete) - Delete File
* [download](#download) - Download File
* [get_signed_url](#get_signed_url) - Get Signed Url

## upload

Upload a file that can be used across various endpoints.

The size of individual files can be a maximum of 512 MB. The Fine-tuning API only supports .jsonl files.

Please contact us if you need to increase these storage limits.

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_upload_file" method="post" path="/v1/files" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.upload(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file`                                                                                                                                                                                                                                                                                                              | [models.File](../../models/file.md)                                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `purpose`                                                                                                                                                                                                                                                                                                           | [Optional[models.FilePurpose]](../../models/filepurpose.md)                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.UploadFileOut](../../models/uploadfileout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## list

Returns a list of files that belong to the user's organization.

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_list_files" method="get" path="/v1/files" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.list(page=0, page_size=100, include_total=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page`                                                              | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `include_total`                                                     | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sample_type`                                                       | List[[models.SampleType](../../models/sampletype.md)]               | :heavy_minus_sign:                                                  | N/A                                                                 |
| `source`                                                            | List[[models.Source](../../models/source.md)]                       | :heavy_minus_sign:                                                  | N/A                                                                 |
| `search`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `purpose`                                                           | [OptionalNullable[models.FilePurpose]](../../models/filepurpose.md) | :heavy_minus_sign:                                                  | N/A                                                                 |
| `mimetypes`                                                         | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListFilesOut](../../models/listfilesout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## retrieve

Returns information about a specific file.

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_retrieve_file" method="get" path="/v1/files/{file_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.retrieve(file_id="f2a27685-ca4e-4dc2-9f2b-88c422c3e0f6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RetrieveFileOut](../../models/retrievefileout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## delete

Delete a file.

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_delete_file" method="delete" path="/v1/files/{file_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.delete(file_id="3b6d45eb-e30b-416f-8019-f47e2e93d930")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeleteFileOut](../../models/deletefileout.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## download

Download a file

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_download_file" method="get" path="/v1/files/{file_id}/content" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.download(file_id="f8919994-a4a1-46b2-8b5b-06335a4300ce")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[httpx.Response](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## get_signed_url

Get Signed Url

### Example Usage

<!-- UsageSnippet language="python" operationID="files_api_routes_get_signed_url" method="get" path="/v1/files/{file_id}/url" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.get_signed_url(file_id="06a020ab-355c-49a6-b19d-304b7c01699f", expiry=24)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `expiry`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Number of hours before the url becomes invalid. Defaults to 24h     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.FileSignedURL](../../models/filesignedurl.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |