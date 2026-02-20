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
from mistralai.client import Mistral
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

**[models.ListSharingsResponse](../../models/listsharingsresponse.md)**

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
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.accesses.update_or_create(library_id="ae92ecb2-1ed7-4c5f-97e0-b2cbe325a206", level="Editor", share_with_uuid="add9ae1f-2854-4378-84a0-91c77efa6fd2", share_with_type="User")

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

**[models.Sharing](../../models/sharing.md)**

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
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.libraries.accesses.delete(library_id="843cc47c-e8f3-454c-9fc5-fcd7fb2865b0", share_with_uuid="0814a235-c2d0-4814-875a-4b85f93d3dc7", share_with_type="Org")

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

**[models.Sharing](../../models/sharing.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |