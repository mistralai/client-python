# Beta.Users

## Overview

### Available Operations

* [get_identity](#get_identity) - Get Identity

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