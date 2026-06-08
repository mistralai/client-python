# Beta.Prompts

## Overview

(beta) Prompts API - create and manage reusable prompt templates with versioning

### Available Operations

* [list](#list)
* [create](#create)
* [get](#get)
* [delete](#delete)
* [update](#update)
* [update_sharing_scope](#update_sharing_scope)
* [list_versions](#list_versions)
* [create_version](#create_version)
* [update_version](#update_version)

## list

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

| Parameter                                                                                                                          | Type                                                                                                                               | Required                                                                                                                           | Description                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `page_size`                                                                                                                        | *Optional[int]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | N/A                                                                                                                                |
| `page_token`                                                                                                                       | *Optional[str]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | N/A                                                                                                                                |
| `fields`                                                                                                                           | *Optional[str]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | Optional, supports nested fields (e.g. "prompt_id", "prompt.prompt", "metadata.latest_version").<br/>An empty mask returns all fields. |
| `version_alias`                                                                                                                    | *Optional[str]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | Selects the version returned for each object and excludes objects<br/>without this current alias.                                  |
| `retries`                                                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                   | :heavy_minus_sign:                                                                                                                 | Configuration to override the default retry behavior of the client.                                                                |

### Response

**[models.PromptsListResponse](../../models/promptslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

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

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `prompt`                                                                    | [Optional[models.V1Prompt]](../../models/v1prompt.md)                       | :heavy_minus_sign:                                                          | User-editable template fields (create / update body).                       |
| `attributes`                                                                | [Optional[models.V1Attributes]](../../models/v1attributes.md)               | :heavy_minus_sign:                                                          | N/A                                                                         |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `name`                                                                      | *Optional[str]*                                                             | :heavy_minus_sign:                                                          | Optional human-readable name, immutable after creation.                     |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.PromptsCreateResponse](../../models/promptscreateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_get" method="get" path="/v1/prompts/{promptId}" -->
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

| Parameter                                                                                                                          | Type                                                                                                                               | Required                                                                                                                           | Description                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `prompt_id`                                                                                                                        | *str*                                                                                                                              | :heavy_check_mark:                                                                                                                 | N/A                                                                                                                                |
| `version`                                                                                                                          | *Optional[int]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | Fetch specific version number.                                                                                                     |
| `alias`                                                                                                                            | *Optional[str]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | Fetch version pointed to by alias name.                                                                                            |
| `fields`                                                                                                                           | *Optional[str]*                                                                                                                    | :heavy_minus_sign:                                                                                                                 | Optional, supports nested fields (e.g. "prompt_id", "prompt.prompt", "metadata.latest_version").<br/>An empty mask returns all fields. |
| `retries`                                                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                   | :heavy_minus_sign:                                                                                                                 | Configuration to override the default retry behavior of the client.                                                                |

### Response

**[models.PromptsGetResponse](../../models/promptsgetresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_delete" method="delete" path="/v1/prompts/{promptId}" -->
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

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_attributes" method="patch" path="/v1/prompts/{promptId}" -->
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

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `attributes`                                                        | [Optional[models.V1Attributes]](../../models/v1attributes.md)       | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsUpdateAttributesResponse](../../models/promptsupdateattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_sharing_scope

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_sharing_scope" method="patch" path="/v1/prompts/{promptId}/sharing-scope" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.prompts.update_sharing_scope(prompt_id="<id>", sharing_scope="sharing_scope_unspecified")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `prompt_id`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `sharing_scope`                                                     | [Optional[models.V1SharingScope]](../../models/v1sharingscope.md)   | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.PromptsUpdateSharingScopeResponse](../../models/promptsupdatesharingscoperesponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_list_versions" method="get" path="/v1/prompts/{promptId}/versions" -->
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

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_create_version" method="post" path="/v1/prompts/{promptId}/versions" -->
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

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `prompt_id`                                                                 | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `prompt`                                                                    | [Optional[models.V1Prompt]](../../models/v1prompt.md)                       | :heavy_minus_sign:                                                          | User-editable template fields (create / update body).                       |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.PromptsCreateVersionResponse](../../models/promptscreateversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version

### Example Usage

<!-- UsageSnippet language="python" operationID="prompts_update_version_attributes" method="patch" path="/v1/prompts/{promptId}/versions/{version}" -->
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

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `prompt_id`                                                                 | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `version`                                                                   | *int*                                                                       | :heavy_check_mark:                                                          | Target version.                                                             |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.PromptsUpdateVersionAttributesResponse](../../models/promptsupdateversionattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |