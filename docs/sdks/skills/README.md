# Beta.Skills

## Overview

(beta) Skills API - create and manage agent skills with versioning

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

<!-- UsageSnippet language="python" operationID="skills_list" method="get" path="/v1/skills" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.list()

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `page_size`                                                                                                                     | *Optional[int]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `page_token`                                                                                                                    | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `fields`                                                                                                                        | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | Optional, supports nested fields (e.g. "skill_id", "skill.skill", "metadata.latest_version").<br/>An empty mask returns all fields. |
| `version_alias`                                                                                                                 | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | Selects the version returned for each object and excludes objects<br/>without this current alias.                               |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[models.SkillsListResponse](../../models/skillslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_create" method="post" path="/v1/skills" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.create()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `skill`                                                                     | [Optional[models.V1Skill]](../../models/v1skill.md)                         | :heavy_minus_sign:                                                          | Per-version content package surfaced to the model.                          |
| `attributes`                                                                | [Optional[models.V1Attributes]](../../models/v1attributes.md)               | :heavy_minus_sign:                                                          | N/A                                                                         |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `name`                                                                      | *Optional[str]*                                                             | :heavy_minus_sign:                                                          | Optional human-readable name (immutable after creation, workspace-unique).  |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.SkillsCreateResponse](../../models/skillscreateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_get" method="get" path="/v1/skills/{skillId}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.get(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                       | Type                                                                                                                            | Required                                                                                                                        | Description                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                      | *str*                                                                                                                           | :heavy_check_mark:                                                                                                              | N/A                                                                                                                             |
| `version`                                                                                                                       | *Optional[int]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `alias`                                                                                                                         | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | N/A                                                                                                                             |
| `fields`                                                                                                                        | *Optional[str]*                                                                                                                 | :heavy_minus_sign:                                                                                                              | Optional, supports nested fields (e.g. "skill_id", "skill.skill", "metadata.latest_version").<br/>An empty mask returns all fields. |
| `retries`                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                | :heavy_minus_sign:                                                                                                              | Configuration to override the default retry behavior of the client.                                                             |

### Response

**[models.SkillsGetResponse](../../models/skillsgetresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_delete" method="delete" path="/v1/skills/{skillId}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.delete(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsDeleteResponse](../../models/skillsdeleteresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_attributes" method="patch" path="/v1/skills/{skillId}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `attributes`                                                        | [Optional[models.V1Attributes]](../../models/v1attributes.md)       | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsUpdateAttributesResponse](../../models/skillsupdateattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_sharing_scope

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_sharing_scope" method="patch" path="/v1/skills/{skillId}/sharing-scope" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update_sharing_scope(skill_id="<id>", sharing_scope="sharing_scope_unspecified")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `sharing_scope`                                                     | [Optional[models.V1SharingScope]](../../models/v1sharingscope.md)   | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsUpdateSharingScopeResponse](../../models/skillsupdatesharingscoperesponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_list_versions" method="get" path="/v1/skills/{skillId}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.list_versions(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsListVersionsResponse](../../models/skillslistversionsresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create_version

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_create_version" method="post" path="/v1/skills/{skillId}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.create_version(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `skill_id`                                                                  | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `skill`                                                                     | [Optional[models.V1Skill]](../../models/v1skill.md)                         | :heavy_minus_sign:                                                          | Per-version content package surfaced to the model.                          |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.SkillsCreateVersionResponse](../../models/skillscreateversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_version_attributes" method="patch" path="/v1/skills/{skillId}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update_version(skill_id="<id>", version=486174)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `skill_id`                                                                  | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `version`                                                                   | *int*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `version_attributes`                                                        | [Optional[models.V1VersionAttributes]](../../models/v1versionattributes.md) | :heavy_minus_sign:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.SkillsUpdateVersionAttributesResponse](../../models/skillsupdateversionattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |