# Beta.ServiceAccounts

## Overview

### Available Operations

* [create](#create) - Create Service Account
* [list](#list) - List Service Accounts
* [list_assignable_roles](#list_assignable_roles) - List Assignable Service Account Roles
* [get](#get) - Get Service Account
* [update](#update) - Update Service Account
* [delete](#delete) - Delete Service Account
* [set_roles](#set_roles) - Set Service Account Roles
* [list_roles](#list_roles) - List Service Account Roles

## create

Create a service account in a workspace. Requires the `create_service_account` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_service_account_v1_service_accounts_post" method="post" path="/v1/service-accounts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.create(name="<value>", workspace_id="cf2146d0-158c-4b19-b8b1-ca0c68f41143")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `workspace_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ServiceAccount](../../models/serviceaccount.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

List the service accounts in a workspace.

Requires the `see_all_workspace_service_accounts` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_service_accounts_v1_service_accounts_get" method="get" path="/v1/service-accounts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.list(workspace_id="96e67917-4b94-4dc0-b61a-bd713aa8a4e6", offset=251948, limit=234499, include_deleted=False)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workspace_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `offset`                                                            | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `limit`                                                             | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `include_deleted`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListServiceAccountsV1ServiceAccountsGetResponse](../../models/listserviceaccountsv1serviceaccountsgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_assignable_roles

List the workspace roles that can be assigned to a service account.

Requires the `see_all_workspace_service_accounts` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_assignable_service_account_roles_v1_service_accounts_assignable_roles_get" method="get" path="/v1/service-accounts/assignable-roles" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.list_assignable_roles(workspace_id="e9326c4d-7aff-483b-9353-303bf1802e99")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `workspace_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListAssignableServiceAccountRolesResponse](../../models/listassignableserviceaccountrolesresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Retrieve a service account.

Requires the `see_all_workspace_service_accounts` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_service_account_v1_service_accounts__service_account_id__get" method="get" path="/v1/service-accounts/{service_account_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.get(service_account_id="68d1ecd2-32cb-473b-ae76-6d87e59f4cd1")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `service_account_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ServiceAccount](../../models/serviceaccount.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update a service account.

Requires the `manage_any_workspace_service_account` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="update_service_account_v1_service_accounts__service_account_id__patch" method="patch" path="/v1/service-accounts/{service_account_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.update(service_account_id="2f4d1ce1-d8ad-4a87-b31b-308088fc2a76")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `service_account_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `description`                                                       | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ServiceAccount](../../models/serviceaccount.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete a service account.

Requires the `manage_any_workspace_service_account` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_service_account_v1_service_accounts__service_account_id__delete" method="delete" path="/v1/service-accounts/{service_account_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.service_accounts.delete(service_account_id="10f960e0-abaa-4060-9000-249255e07c45")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `service_account_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## set_roles

Replace the workspace roles assigned to a service account.

Requires the `manage_any_workspace_service_account` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="set_service_account_roles_v1_service_accounts__service_account_id__roles_put" method="put" path="/v1/service-accounts/{service_account_id}/roles" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.set_roles(service_account_id="d4686916-124a-42f1-966f-9248b120b13c")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `service_account_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `role_ids`                                                          | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListServiceAccountRolesResponse](../../models/listserviceaccountrolesresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_roles

List the workspace roles assigned to a service account.

Requires the `see_all_workspace_service_accounts` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_service_account_roles_v1_service_accounts__service_account_id__roles_get" method="get" path="/v1/service-accounts/{service_account_id}/roles" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.service_accounts.list_roles(service_account_id="0c629f5d-1a74-4b83-a740-14410ecdea21")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `service_account_id`                                                | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListServiceAccountRolesResponse](../../models/listserviceaccountrolesresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |