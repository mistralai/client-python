# Beta.Prompts

## Overview

### Available Operations

* [list](#list) - ListPrompts
* [create](#create) - CreatePrompt
* [get](#get) - GetPrompt
* [delete](#delete) - DeletePrompt
* [update_metadata](#update_metadata) - UpdatePrompt
* [list_versions](#list_versions) - ListPromptVersions
* [create_version](#create_version) - CreatePromptVersion
* [get_version](#get_version) - GetPromptVersion
* [update_version_metadata](#update_version_metadata) - UpdatePromptVersionMetadata

## list

ListPrompts

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_list" method="get" path="/v2/prompts" -->
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

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page_token`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `alias`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsListResponse](../../models/promptslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

CreatePrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_create" method="post" path="/v2/prompts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.create(name="<value>", definition={
        "content": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `name`                                                                        | *str*                                                                         | :heavy_check_mark:                                                            | Stable object name.                                                           |
| `definition`                                                                  | [models.PromptDefinition](../../models/promptdefinition.md)                   | :heavy_check_mark:                                                            | Versioned prompt content.                                                     |
| `title`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Display title.                                                                |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Display description.                                                          |
| `notes`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Notes for this version.                                                       |
| `sharing_scope`                                                               | [Optional[models.RegistrySharingScope]](../../models/registrysharingscope.md) | :heavy_minus_sign:                                                            | N/A                                                                           |
| `aliases`                                                                     | List[*str*]                                                                   | :heavy_minus_sign:                                                            | Aliases pointing to this version.                                             |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.Prompt](../../models/prompt.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

GetPrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_get" method="get" path="/v2/prompts/{prompt_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.get(prompt_id="<id>", version=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `version`                                                           | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 | 1                                                                   |
| `alias`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.Prompt](../../models/prompt.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

DeletePrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_delete" method="delete" path="/v2/prompts/{prompt_id}" -->
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

**[models.DeletePromptResponse](../../models/deletepromptresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_metadata

UpdatePrompt

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update" method="patch" path="/v2/prompts/{prompt_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update_metadata(prompt_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `prompt_id`                                                                   | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `title`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Display title.                                                                |
| `description`                                                                 | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Display description.                                                          |
| `sharing_scope`                                                               | [Optional[models.RegistrySharingScope]](../../models/registrysharingscope.md) | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.Prompt](../../models/prompt.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

ListPromptVersions

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_list_versions" method="get" path="/v2/prompts/{prompt_id}/versions" -->
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

**[models.ListPromptVersionsResponse](../../models/listpromptversionsresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create_version

CreatePromptVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_create_version" method="post" path="/v2/prompts/{prompt_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.create_version(prompt_id="<id>", definition={
        "content": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `definition`                                                        | [models.PromptDefinition](../../models/promptdefinition.md)         | :heavy_check_mark:                                                  | Versioned prompt content.                                           |
| `notes`                                                             | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Notes for this version.                                             |
| `aliases`                                                           | List[*str*]                                                         | :heavy_minus_sign:                                                  | Aliases pointing to this version.                                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreatePromptVersionResponse](../../models/createpromptversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get_version

GetPromptVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_get_version" method="get" path="/v2/prompts/{prompt_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.get_version(prompt_id="<id>", version=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `version`                                                           | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | 1                                                                   |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.Prompt](../../models/prompt.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version_metadata

UpdatePromptVersionMetadata

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_version_metadata" method="patch" path="/v2/prompts/{prompt_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update_version_metadata(prompt_id="<id>", version=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                       | Type                                                                                                                                                                                                                            | Required                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                     | Example                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                                                                                                                     | *str*                                                                                                                                                                                                                           | :heavy_check_mark:                                                                                                                                                                                                              | N/A                                                                                                                                                                                                                             |                                                                                                                                                                                                                                 |
| `version`                                                                                                                                                                                                                       | *int*                                                                                                                                                                                                                           | :heavy_check_mark:                                                                                                                                                                                                              | N/A                                                                                                                                                                                                                             | 1                                                                                                                                                                                                                               |
| `notes`                                                                                                                                                                                                                         | *OptionalNullable[str]*                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                              | Notes for this version.                                                                                                                                                                                                         |                                                                                                                                                                                                                                 |
| `aliases`                                                                                                                                                                                                                       | [Optional[models.AliasList]](../../models/aliaslist.md)                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                              | Presence wrapper for a set of alias labels on update RPCs. As a message field it carries presence, so callers can distinguish "leave aliases unchanged" (field omitted) from "clear all aliases" (field set, empty ``values``). |                                                                                                                                                                                                                                 |
| `retries`                                                                                                                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                              | Configuration to override the default retry behavior of the client.                                                                                                                                                             |                                                                                                                                                                                                                                 |

### Response

**[models.Prompt](../../models/prompt.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |