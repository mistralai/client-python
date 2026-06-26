# Beta.Skills

## Overview

### Available Operations

* [list](#list) - ListSkills
* [create](#create) - CreateSkill
* [get](#get) - GetSkill
* [delete](#delete) - DeleteSkill
* [update_metadata](#update_metadata) - UpdateSkill
* [list_versions](#list_versions) - ListSkillVersions
* [create_version](#create_version) - CreateSkillVersion
* [get_version](#get_version) - GetSkillVersion
* [update_version_metadata](#update_version_metadata) - UpdateSkillVersionMetadata

## list

ListSkills

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_list" method="get" path="/v2/skills" -->
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

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `page_token`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `alias`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsListResponse](../../models/skillslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

CreateSkill

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_create" method="post" path="/v2/skills" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.create(name="<value>", definition={
        "body": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `name`                                                                        | *str*                                                                         | :heavy_check_mark:                                                            | Stable object name.                                                           |
| `definition`                                                                  | [models.SkillDefinition](../../models/skilldefinition.md)                     | :heavy_check_mark:                                                            | Versioned skill content.                                                      |
| `notes`                                                                       | *OptionalNullable[str]*                                                       | :heavy_minus_sign:                                                            | Notes for this version.                                                       |
| `sharing_scope`                                                               | [Optional[models.RegistrySharingScope]](../../models/registrysharingscope.md) | :heavy_minus_sign:                                                            | N/A                                                                           |
| `aliases`                                                                     | List[*str*]                                                                   | :heavy_minus_sign:                                                            | Aliases pointing to this version.                                             |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.SkillsCreateResponse](../../models/skillscreateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

GetSkill

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_get" method="get" path="/v2/skills/{skill_id}" -->
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

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `alias`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsGetResponse](../../models/skillsgetresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## delete

DeleteSkill

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_delete" method="delete" path="/v2/skills/{skill_id}" -->
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

## update_metadata

UpdateSkill

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update" method="patch" path="/v2/skills/{skill_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update_metadata(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                     | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `skill_id`                                                                    | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `sharing_scope`                                                               | [Optional[models.RegistrySharingScope]](../../models/registrysharingscope.md) | :heavy_minus_sign:                                                            | N/A                                                                           |
| `retries`                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)              | :heavy_minus_sign:                                                            | Configuration to override the default retry behavior of the client.           |

### Response

**[models.SkillsUpdateResponse](../../models/skillsupdateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

ListSkillVersions

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_list_versions" method="get" path="/v2/skills/{skill_id}/versions" -->
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

CreateSkillVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_create_version" method="post" path="/v2/skills/{skill_id}/versions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.create_version(skill_id="<id>", definition={
        "body": "<value>",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `definition`                                                        | [models.SkillDefinition](../../models/skilldefinition.md)           | :heavy_check_mark:                                                  | Versioned skill content.                                            |
| `notes`                                                             | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Notes for this version.                                             |
| `aliases`                                                           | List[*str*]                                                         | :heavy_minus_sign:                                                  | Aliases pointing to this version.                                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsCreateVersionResponse](../../models/skillscreateversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get_version

GetSkillVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_get_version" method="get" path="/v2/skills/{skill_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.get_version(skill_id="<id>", version=808285)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `skill_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `version`                                                           | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsGetVersionResponse](../../models/skillsgetversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version_metadata

UpdateSkillVersionMetadata

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_version_metadata" method="patch" path="/v2/skills/{skill_id}/versions/{version}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update_version_metadata(skill_id="<id>", version=521507)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                       | Type                                                                                                                                                                                                                            | Required                                                                                                                                                                                                                        | Description                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                                                                                                                      | *str*                                                                                                                                                                                                                           | :heavy_check_mark:                                                                                                                                                                                                              | N/A                                                                                                                                                                                                                             |
| `version`                                                                                                                                                                                                                       | *int*                                                                                                                                                                                                                           | :heavy_check_mark:                                                                                                                                                                                                              | N/A                                                                                                                                                                                                                             |
| `notes`                                                                                                                                                                                                                         | *OptionalNullable[str]*                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                              | Notes for this version.                                                                                                                                                                                                         |
| `aliases`                                                                                                                                                                                                                       | [Optional[models.AliasList]](../../models/aliaslist.md)                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                              | Presence wrapper for a set of alias labels on update RPCs. As a message field it carries presence, so callers can distinguish "leave aliases unchanged" (field omitted) from "clear all aliases" (field set, empty ``values``). |
| `retries`                                                                                                                                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                              | Configuration to override the default retry behavior of the client.                                                                                                                                                             |

### Response

**[models.SkillsUpdateVersionMetadataResponse](../../models/skillsupdateversionmetadataresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |