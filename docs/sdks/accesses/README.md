# Beta.Libraries.Accesses

## Overview

(beta) Libraries API - manage access to a library.

### Available Operations

* [list](#list) - List all of the access to this library.
* [update_or_create](#update_or_create) - Create or update an access level.
* [delete](#delete) - Delete an access level.

## list

Given a library, list all of the Entity that have access and to what level.

### Example Usage

<!-- UsageSnippet language="python" operationID="libraries_share_list_v1" method="get" path="/v1/libraries/{library_id}/share" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.accesses.list(library_id="d2169833-d8e2-416e-a372-76518d3d99c2")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `library_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListSharingOut](../../models/listsharingout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_or_create

Given a library id, you can create or update the access level of an entity. You have to be owner of the library to share a library. An owner cannot change their own role. A library cannot be shared outside of the organization.

### Example Usage

<!-- UsageSnippet language="python" operationID="libraries_share_create_v1" method="put" path="/v1/libraries/{library_id}/share" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.accesses.update_or_create(library_id="36de3a24-5b1c-4c8f-9d84-d5642205a976", level="Viewer", share_with_uuid="0ae92ecb-21ed-47c5-9f7e-0b2cbe325a20", share_with_type="User")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `library_id`                                                         | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `level`                                                              | [models.ShareEnum](../../models/shareenum.md)                        | :heavy_check_mark:                                                   | N/A                                                                  |
| `share_with_uuid`                                                    | *str*                                                                | :heavy_check_mark:                                                   | The id of the entity (user, workspace or organization) to share with |
| `share_with_type`                                                    | [models.EntityType](../../models/entitytype.md)                      | :heavy_check_mark:                                                   | The type of entity, used to share a library.                         |
| `org_id`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.SharingOut](../../models/sharingout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Given a library id, you can delete the access level of an entity. An owner cannot delete it's own access. You have to be the owner of the library to delete an acces other than yours.

### Example Usage

<!-- UsageSnippet language="python" operationID="libraries_share_delete_v1" method="delete" path="/v1/libraries/{library_id}/share" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.accesses.delete(library_id="709e3cad-9fb2-4f4e-bf88-143cf1808107", share_with_uuid="b843cc47-ce8f-4354-8cfc-5fcd7fb2865b", share_with_type="User")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `library_id`                                                         | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `share_with_uuid`                                                    | *str*                                                                | :heavy_check_mark:                                                   | The id of the entity (user, workspace or organization) to share with |
| `share_with_type`                                                    | [models.EntityType](../../models/entitytype.md)                      | :heavy_check_mark:                                                   | The type of entity, used to share a library.                         |
| `org_id`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |

### Response

**[models.SharingOut](../../models/sharingout.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |