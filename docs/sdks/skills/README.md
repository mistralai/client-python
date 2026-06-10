# Beta.Skills

## Overview

(beta) Skills API - create and manage agent skills with versioning

### Available Operations

* [list](#list) - ListSkills
* [create](#create) - CreateSkill
* [get](#get) - GetSkill
* [delete](#delete) - DeleteSkill
* [update](#update) - UpdateSkillAttributes
* [list_versions](#list_versions) - ListSkillVersions
* [create_version](#create_version) - CreateSkillVersion
* [get_version](#get_version) - GetSkillVersion
* [update_version](#update_version) - UpdateSkillVersionAttributes
* [update_sharing_scope](#update_sharing_scope) - UpdateSkillSharingScope

## list

ListSkills

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

**[models.SkillsListResponse](../../models/skillslistresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

CreateSkill

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

| Parameter                                                                  | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `skill`                                                                    | [Optional[models.SkillContent]](../../models/skillcontent.md)              | :heavy_minus_sign:                                                         | Per-version content package surfaced to the model.                         |
| `attributes`                                                               | [Optional[models.Attributes]](../../models/attributes.md)                  | :heavy_minus_sign:                                                         | N/A                                                                        |
| `version_attributes`                                                       | [Optional[models.VersionAttributes]](../../models/versionattributes.md)    | :heavy_minus_sign:                                                         | User-provided, per-version fields                                          |
| `name`                                                                     | *Optional[str]*                                                            | :heavy_minus_sign:                                                         | Optional human-readable name (immutable after creation, workspace-unique). |
| `retries`                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)           | :heavy_minus_sign:                                                         | Configuration to override the default retry behavior of the client.        |

### Response

**[models.SkillsCreateResponse](../../models/skillscreateresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get

GetSkill

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_get" method="get" path="/v1/skills/{skill_id}" -->
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
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | The set of field mask paths.                                        |
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

<!-- UsageSnippet language="python" operationID="skills_delete" method="delete" path="/v1/skills/{skill_id}" -->
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

UpdateSkillAttributes

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_attributes" method="patch" path="/v1/skills/{skill_id}" -->
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

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                                                                                                                                                                                                          | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `attributes`                                                                                                                                                                                                                                                                                                        | [Optional[models.Attributes]](../../models/attributes.md)                                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.SkillsUpdateAttributesResponse](../../models/skillsupdateattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_versions

ListSkillVersions

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_list_versions" method="get" path="/v1/skills/{skill_id}/versions" -->
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

<!-- UsageSnippet language="python" operationID="skills_create_version" method="post" path="/v1/skills/{skill_id}/versions" -->
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

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                                                                                                                                                                                                          | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `skill`                                                                                                                                                                                                                                                                                                             | [Optional[models.SkillContent]](../../models/skillcontent.md)                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Per-version content package surfaced to the model.                                                                                                                                                                                                                                                                  |
| `version_attributes`                                                                                                                                                                                                                                                                                                | [Optional[models.VersionAttributes]](../../models/versionattributes.md)                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | User-provided, per-version fields                                                                                                                                                                                                                                                                                   |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.SkillsCreateVersionResponse](../../models/skillscreateversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## get_version

GetSkillVersion

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_get_version" method="get" path="/v1/skills/{skill_id}/versions/{version}" -->
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
| `fields`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | The set of field mask paths.                                        |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SkillsGetVersionResponse](../../models/skillsgetversionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_version

UpdateSkillVersionAttributes

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_version_attributes" method="patch" path="/v1/skills/{skill_id}/versions/{version}" -->
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

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                                                                                                                                                                                                          | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `version`                                                                                                                                                                                                                                                                                                           | *int*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `version_attributes`                                                                                                                                                                                                                                                                                                | [Optional[models.VersionAttributes]](../../models/versionattributes.md)                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | User-provided, per-version fields                                                                                                                                                                                                                                                                                   |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.SkillsUpdateVersionAttributesResponse](../../models/skillsupdateversionattributesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## update_sharing_scope

UpdateSkillSharingScope

### Example Usage

<!-- UsageSnippet language="python" operationID="skills_update_sharing_scope" method="patch" path="/v1/skills/{skill_id}/sharing-scope" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.skills.update_sharing_scope(skill_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skill_id`                                                                                                                                                                                                                                                                                                          | *str*                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `sharing_scope`                                                                                                                                                                                                                                                                                                     | [Optional[models.SharingScope]](../../models/sharingscope.md)                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | N/A                                                                                                                                                                                                                                                                                                                 |
| `file`                                                                                                                                                                                                                                                                                                              | *Optional[bytes]*                                                                                                                                                                                                                                                                                                   | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | The File object (not file name) to be uploaded.<br/> To upload a file and specify a custom file name you should format your request as such:<br/> ```bash<br/> file=@path/to/your/file.jsonl;filename=custom_name.jsonl<br/> ```<br/> Otherwise, you can just keep the original file name:<br/> ```bash<br/> file=@path/to/your/file.jsonl<br/> ``` |
| `retries`                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                 |

### Response

**[models.SkillsUpdateSharingScopeResponse](../../models/skillsupdatesharingscoperesponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |