# Beta.Prompts

## Overview

(beta) Prompts API - create and manage reusable prompt templates with versioning

### Available Operations

* [list](#list) - ListPrompts
* [create](#create) - CreatePrompt
* [get](#get) - GetPrompt
* [delete](#delete) - DeletePrompt
* [update](#update) - UpdatePromptAttributes
* [list_versions](#list_versions) - ListPromptVersions
* [create_version](#create_version) - CreatePromptVersion
* [get_version](#get_version) - GetPromptVersion
* [update_version](#update_version) - UpdatePromptVersionAttributes
* [update_sharing_scope](#update_sharing_scope) - UpdatePromptSharingScope

## list

ListPrompts

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_list" method="get" path="/v1/prompts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.list()

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                                      | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `page_size`                                                                                    | *Optional[int]*                                                                                | :heavy_minus_sign:                                                                             | N/A                                                                                            |
| `page_token`                                                                                   | *Optional[str]*                                                                                | :heavy_minus_sign:                                                                             | N/A                                                                                            |
| `fields`                                                                                       | List[*str*]                                                                                    | :heavy_minus_sign:                                                                             | The set of field mask paths.                                                                   |
| `version_alias`                                                                                | *Optional[str]*                                                                                | :heavy_minus_sign:                                                                             | Selects the version returned for each object and excludes objects<br/> without this current alias. |
| `filter_key`                                                                                   | *Optional[str]*                                                                                | :heavy_minus_sign:                                                                             | N/A                                                                                            |
| `filter_value`                                                                                 | *Optional[str]*                                                                                | :heavy_minus_sign:                                                                             | N/A                                                                                            |
| `search`                                                                                       | *Optional[str]*                                                                                | :heavy_minus_sign:                                                                             | Case-insensitive substring match against per-version content.                                  |
| `retries`                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                               | :heavy_minus_sign:                                                                             | Configuration to override the default retry behavior of the client.                            |

### Response

**[models.PromptsListResponse](../../models/promptslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

--- Existing (modified request/response) ---

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_create" method="post" path="/v1/prompts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.create()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `prompt`                                                                | [Optional[models.PromptContent]](../../models/promptcontent.md)         | :heavy_minus_sign:                                                      | User-editable template fields (create / update body).                   |
| `attributes`                                                            | [Optional[models.Attributes]](../../models/attributes.md)               | :heavy_minus_sign:                                                      | N/A                                                                     |
| `version_attributes`                                                    | [Optional[models.VersionAttributes]](../../models/versionattributes.md) | :heavy_minus_sign:                                                      | User-provided, per-version fields                                       |
| `name`                                                                  | *Optional[str]*                                                         | :heavy_minus_sign:                                                      | Optional human-readable name, immutable after creation.                 |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.PromptsCreateResponse](../../models/promptscreateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

GetPrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_get" method="get" path="/v1/prompts/{prompt_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.get(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Fetch specific version number.                                      |
| `alias`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Fetch version pointed to by alias name.                             |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | The set of field mask paths.                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsGetResponse](../../models/promptsgetresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

DeletePrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_delete" method="delete" path="/v1/prompts/{prompt_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.delete(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsDeleteResponse](../../models/promptsdeleteresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update

--- New: per-object mutations ---

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_attributes" method="patch" path="/v1/prompts/{prompt_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `attributes`                                                                                                                                                                                                                                                                                                        | [Optional[models.Attributes]](../../models/attributes.md)                                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.PromptsUpdateAttributesResponse](../../models/promptsupdateattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

ListPromptVersions

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_list_versions" method="get" path="/v1/prompts/{prompt_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.list_versions(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsListVersionsResponse](../../models/promptslistversionsresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create_version

--- New: versioning ---

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_create_version" method="post" path="/v1/prompts/{prompt_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.create_version(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `prompt`                                                                                                                                                                                                                                                                                                            | [Optional[models.PromptContent]](../../models/promptcontent.md)                                                                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | User-editable template fields (create / update body).                                                                                                                                                                                                                                                               |
| `version_attributes`                                                                                                                                                                                                                                                                                                | [Optional[models.VersionAttributes]](../../models/versionattributes.md)                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | User-provided, per-version fields                                                                                                                                                                                                                                                                                   |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.PromptsCreateVersionResponse](../../models/promptscreateversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get_version

GetPromptVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_get_version" method="get" path="/v1/prompts/{prompt_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.get_version(prompt_id="<id>", version=600480)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | The set of field mask paths.                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsGetVersionResponse](../../models/promptsgetversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version

--- New: per-version mutations ---

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_version_attributes" method="patch" path="/v1/prompts/{prompt_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update_version(prompt_id="<id>", version=242918)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `version`                                                                                                                                                                                                                                                                                                           | *int*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | Target version.                                                                                                                                                                                                                                                                                                     |
| `version_attributes`                                                                                                                                                                                                                                                                                                | [Optional[models.VersionAttributes]](../../models/versionattributes.md)                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | User-provided, per-version fields                                                                                                                                                                                                                                                                                   |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.PromptsUpdateVersionAttributesResponse](../../models/promptsupdateversionattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_sharing_scope

UpdatePromptSharingScope

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_sharing_scope" method="patch" path="/v1/prompts/{prompt_id}/sharing-scope" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update_sharing_scope(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                                                                                                                                                                                                         | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `sharing_scope`                                                                                                                                                                                                                                                                                                     | [Optional[models.SharingScope]](../../models/sharingscope.md)                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.PromptsUpdateSharingScopeResponse](../../models/promptsupdatesharingscoperesponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |