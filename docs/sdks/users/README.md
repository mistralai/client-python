# Beta.Users

## Overview

### Available Operations

* [get_identity](#get_identity) - Get Identity
* [list_organizations](#list_organizations) - List Organizations
* [list_workspaces](#list_workspaces) - List Workspaces

## get_identity

Get Identity

### Example Usage

<!-- UsageSnippet language="python" operationID="users_api_get_identity" method="get" path="/v1/users/me" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral() as mistral:

    res = mistral.beta.users.get_identity(security=models.UsersAPIGetIdentitySecurity(
        dashboard_user_context_auth=os.getenv("MISTRAL_DASHBOARD_USER_CONTEXT_AUTH", ""),
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                  | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `security`                                                                 | [models.UsersAPIGetIdentitySecurity](../../usersapigetidentitysecurity.md) | :heavy_check_mark:                                                         | The security requirements to use for the request.                          |
| `retries`                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)           | :heavy_minus_sign:                                                         | Configuration to override the default retry behavior of the client.        |

### Response

**[models.UserIdentity](../../models/useridentity.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_organizations

List every organization the authenticated user is a member of.

Identity-only: the caller need not have selected an organization, so this
reads only the user and never scopes by the active org.

### Example Usage

<!-- UsageSnippet language="python" operationID="users_api_list_organizations" method="get" path="/v1/users/me/organizations" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral() as mistral:

    res = mistral.beta.users.list_organizations(security=models.UsersAPIListOrganizationsSecurity(
        dashboard_user_context_auth=os.getenv("MISTRAL_DASHBOARD_USER_CONTEXT_AUTH", ""),
    ), offset=0, limit=100)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                                     | Type                                                                                          | Required                                                                                      | Description                                                                                   | Example                                                                                       |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `security`                                                                                    | [models.UsersAPIListOrganizationsSecurity](../../models/usersapilistorganizationssecurity.md) | :heavy_check_mark:                                                                            | N/A                                                                                           |                                                                                               |
| `offset`                                                                                      | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | Number of organizations to skip before returning results.                                     | 0                                                                                             |
| `limit`                                                                                       | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | Maximum number of organizations to return.                                                    | 100                                                                                           |
| `retries`                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                              | :heavy_minus_sign:                                                                            | Configuration to override the default retry behavior of the client.                           |                                                                                               |

### Response

**[models.UsersAPIListOrganizationsResponse](../../models/usersapilistorganizationsresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## list_workspaces

List every workspace the authenticated user is a member of, across all
their organizations, each tagged with the organization it belongs to.

### Example Usage

<!-- UsageSnippet language="python" operationID="users_api_list_workspaces" method="get" path="/v1/users/me/workspaces" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral() as mistral:

    res = mistral.beta.users.list_workspaces(security=models.UsersAPIListWorkspacesSecurity(
        dashboard_user_context_auth=os.getenv("MISTRAL_DASHBOARD_USER_CONTEXT_AUTH", ""),
    ), organization_id="1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d", offset=0, limit=100)

    while res is not None:
        # Handle items

        res = res.next()

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             | Example                                                                                 |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `security`                                                                              | [models.UsersAPIListWorkspacesSecurity](../../models/usersapilistworkspacessecurity.md) | :heavy_check_mark:                                                                      | N/A                                                                                     |                                                                                         |
| `organization_id`                                                                       | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | Return only workspaces belonging to this organization.                                  | 1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d                                                    |
| `offset`                                                                                | *Optional[int]*                                                                         | :heavy_minus_sign:                                                                      | Number of workspaces to skip before returning results.                                  | 0                                                                                       |
| `limit`                                                                                 | *Optional[int]*                                                                         | :heavy_minus_sign:                                                                      | Maximum number of workspaces to return.                                                 | 100                                                                                     |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |                                                                                         |

### Response

**[models.UsersAPIListWorkspacesResponse](../../models/usersapilistworkspacesresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |