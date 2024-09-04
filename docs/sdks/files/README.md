# Files
(*files*)

## Overview

Files API

### Available Operations

* [upload](#upload) - Upload File
* [list](#list) - List Files
* [retrieve](#retrieve) - Retrieve File
* [delete](#delete) - Delete File

## upload

Upload a file that can be used across various endpoints.

The size of individual files can be a maximum of 512 MB. The Fine-tuning API only supports .jsonl files.

Please contact us if you need to increase these storage limits.

### Example Usage

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


res = s.files.upload(file={
    "file_name": "your_file_here",
    "content": open("<file_path>", "rb"),
})

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file`                                                                                                                                                                                                                                                                                                              | [models.File](../../models/file.md)                                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.UploadFileOut](../../models/uploadfileout.md)**

### Errors

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |


## list

Returns a list of files that belong to the user's organization.

### Example Usage

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


res = s.files.list()

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListFilesOut](../../models/listfilesout.md)**

### Errors

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |


## retrieve

Returns information about a specific file.

### Example Usage

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


res = s.files.retrieve(file_id="<value>")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.RetrieveFileOut](../../models/retrievefileout.md)**

### Errors

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |


## delete

Delete a file.

### Example Usage

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


res = s.files.delete(file_id="<value>")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `file_id`                                                           | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeleteFileOut](../../models/deletefileout.md)**

### Errors

| Error Object    | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4xx-5xx         | */*             |
