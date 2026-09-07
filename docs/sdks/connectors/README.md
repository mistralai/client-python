# Beta.Connectors

## Overview

(beta) Connectors API - manage your connectors

### Available Operations

* [create](#create) - Create a new connector.
* [list](#list) - List all connectors.
* [get_auth_url](#get_auth_url) - Get the auth URL for a connector.
* [share](#share) - Share a private connector to the current workspace.
* [unshare](#unshare) - Unshare a connector from the current workspace.
* [share_to_organization](#share_to_organization) - Share a connector to the current organization.
* [unshare_from_organization](#unshare_from_organization) - Unshare a connector from the current organization.
* [activate_for_consumer](#activate_for_consumer) - Activate a connector for the given consumer (organization, workspace, user).
* [deactivate_for_consumer](#deactivate_for_consumer) - Deactivate a connector for the current consumer (at organization, workspace or user level).
* [call_tool](#call_tool) - Call Connector Tool
* [list_tools](#list_tools) - List tools for a connector.
* [get_authentication_methods](#get_authentication_methods) - Get authentication methods for a connector.
* [list_organization_credentials](#list_organization_credentials) - List organization credentials for a connector.
* [list_workspace_credentials](#list_workspace_credentials) - List workspace credentials for a connector.
* [list_user_credentials](#list_user_credentials) - List user credentials for a connector.
* [delete_all_user_credentials](#delete_all_user_credentials) - Delete all user credentials for a connector.
* [create_credentials](#create_credentials) - Create consumer credentials for a connector.
* [update_credentials](#update_credentials) - Create or update consumer credentials for a connector.
* [delete_organization_credentials](#delete_organization_credentials) - Delete organization credentials for a connector.
* [delete_workspace_credentials](#delete_workspace_credentials) - Delete workspace credentials for a connector.
* [delete_user_credentials](#delete_user_credentials) - Delete user credentials for a connector.
* [get](#get) - Get a connector.
* [update](#update) - Update a connector.
* [delete](#delete) - Delete a connector.

## create

Create a new MCP or HTTP connector. You can customize its visibility, URL, and auth type.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_create_v1" method="post" path="/v1/connectors" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.create(request={
        "name": "<value>",
        "description": "unibody usually despite slushy wherever reward stingy from",
        "server": "https://royal-majority.net/",
        "protocol": "mcp",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `request`                                                                   | [models.ConnectorCreateV1Payload](../../models/connectorcreatev1payload.md) | :heavy_check_mark:                                                          | The request object to use for the request.                                  |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.Connector](../../models/connector.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list

List all your custom connectors with keyset pagination and filters.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_list_v1" method="get" path="/v1/connectors" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list(page_size=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `query_filters`                                                                   | [Optional[models.ConnectorsQueryFilters]](../../models/connectorsqueryfilters.md) | :heavy_minus_sign:                                                                | N/A                                                                               |
| `cursor`                                                                          | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | N/A                                                                               |
| `page_size`                                                                       | *Optional[int]*                                                                   | :heavy_minus_sign:                                                                | N/A                                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.PaginatedConnectors](../../models/paginatedconnectors.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_auth_url

Get the OAuth2 authorization URL for a connector to initiate user authentication.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_get_auth_url_v1" method="get" path="/v1/connectors/{connector_id_or_name}/auth_url" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.get_auth_url(connector_id_or_name="<value>", github_installation_link=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                    | Type                                                                                                                                                                                                                                                                                                                         | Required                                                                                                                                                                                                                                                                                                                     | Description                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                                                                                                                                                                                                                                                       | *str*                                                                                                                                                                                                                                                                                                                        | :heavy_check_mark:                                                                                                                                                                                                                                                                                                           | N/A                                                                                                                                                                                                                                                                                                                          |
| `app_return_url`                                                                                                                                                                                                                                                                                                             | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | N/A                                                                                                                                                                                                                                                                                                                          |
| `method_type`                                                                                                                                                                                                                                                                                                                | [Optional[models.OutboundAuthenticationType]](../../models/outboundauthenticationtype.md)                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | Auth method type to use for the authorization URL. Required when the connector supports multiple interactive auth methods; otherwise the sole method is selected automatically. Use this to pick a specific method (e.g. 'oauth2' vs 'github_app').                                                                          |
| `credentials_name`                                                                                                                                                                                                                                                                                                           | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | N/A                                                                                                                                                                                                                                                                                                                          |
| `credentials_title`                                                                                                                                                                                                                                                                                                          | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | N/A                                                                                                                                                                                                                                                                                                                          |
| `github_installation_link`                                                                                                                                                                                                                                                                                                   | *Optional[bool]*                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | Only valid with method_type=oauth2. When true, returns a GitHub App installation URL (https://github.com/apps/<slug>/installations/new) if the connector has the proper configuration The Github application needs to have 'Request user authorization (OAuth) during installation' enabled to perform the proper auth loop. |
| `retries`                                                                                                                                                                                                                                                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                           | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                          |

### Response

**[models.AuthURLResponse](../../models/authurlresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## share

Transfers ownership of a private user-owned connector to the current workspace, making it available to all workspace members. The creator can later revert this via the unshare endpoint. Any authentication flows that rely on the original owner's identity (e.g. OAuth on-behalf-of) will be affected and must be reconfigured after sharing. Only the connector's creator can call this endpoint. Requires the ShareConnectorToWorkspace workspace permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_share_v1" method="put" path="/v1/connectors/{connector_id}/share" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.share(connector_id="cf748b50-632b-46d6-98c3-b015086cb194")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unshare

Reverts a workspace-shared connector back to a private, creator-owned connector. Workspace-scoped connections and other members' connections are removed; the creator's own connection is preserved. Only the connector's creator can call this endpoint. Requires the ShareConnectorToWorkspace workspace permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_unshare_v1" method="delete" path="/v1/connectors/{connector_id}/share" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.unshare(connector_id="d5bd99ac-c46d-43bb-835c-cb4833bf101d")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## share_to_organization

Transfers ownership of a private user-owned connector to the current organization, making it available to all organization members. The creator can later revert this via the unshare endpoint. Any authentication flows that rely on the original owner's identity (e.g. OAuth on-behalf-of) will be affected and must be reconfigured after sharing. Requires the ShareConnectorToOrg organization permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_share_to_organization_v1" method="put" path="/v1/connectors/{connector_id}/organization/share" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.share_to_organization(connector_id="9dc7017e-ae2f-451c-9b03-623aab4aecde")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## unshare_from_organization

Reverts an organization-shared connector back to a private, creator-owned connector. Organization-scoped connections and other members' connections are removed; the creator's own connection is preserved. Requires the ShareConnectorToOrg organization permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_unshare_from_organization_v1" method="delete" path="/v1/connectors/{connector_id}/organization/share" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.unshare_from_organization(connector_id="def26f6b-c03a-4deb-9726-3771c1dd3388")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## activate_for_consumer

Enable a connector for the consumer.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_activate_for_consumer_v1" method="post" path="/v1/connectors/{connector_id}/{consumer_scope}/activate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.activate_for_consumer(connector_id="1637d954-8ef0-4080-9228-89d4c05c915f", consumer_scope="workspace")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `connector_id`                                                                                                    | *str*                                                                                                             | :heavy_check_mark:                                                                                                | N/A                                                                                                               |
| `consumer_scope`                                                                                                  | [models.ConnectorActivateForConsumerV1ConsumerScope](../../models/connectoractivateforconsumerv1consumerscope.md) | :heavy_check_mark:                                                                                                | N/A                                                                                                               |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## deactivate_for_consumer

Disable a connector for the calling consumer only.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_deactivate_for_consumer_v1" method="post" path="/v1/connectors/{connector_id}/{consumer_scope}/deactivate" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.deactivate_for_consumer(connector_id="1266a170-0379-4b3f-9305-d10fd2a83d29", consumer_scope="workspace")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                             | Type                                                                                                                  | Required                                                                                                              | Description                                                                                                           |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `connector_id`                                                                                                        | *str*                                                                                                                 | :heavy_check_mark:                                                                                                    | N/A                                                                                                                   |
| `consumer_scope`                                                                                                      | [models.ConnectorDeactivateForConsumerV1ConsumerScope](../../models/connectordeactivateforconsumerv1consumerscope.md) | :heavy_check_mark:                                                                                                    | N/A                                                                                                                   |
| `retries`                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                      | :heavy_minus_sign:                                                                                                    | Configuration to override the default retry behavior of the client.                                                   |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## call_tool

Call a tool on an MCP connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_call_tool_v1" method="post" path="/v1/connectors/{connector_id_or_name}/tools/{tool_name}/call" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.call_tool(tool_name="<value>", connector_id_or_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `tool_name`                                                         | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `credentials_name`                                                  | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `arguments`                                                         | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ConnectorToolCallResponse](../../models/connectortoolcallresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_tools

List all tools available for an MCP connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_list_tools_v1" method="get" path="/v1/connectors/{connector_id_or_name}/tools" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list_tools(connector_id_or_name="<value>", page=1, page_size=100, refresh=False, pretty=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                        | Type                                                                                             | Required                                                                                         | Description                                                                                      |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `connector_id_or_name`                                                                           | *str*                                                                                            | :heavy_check_mark:                                                                               | N/A                                                                                              |
| `page`                                                                                           | *Optional[int]*                                                                                  | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `page_size`                                                                                      | *Optional[int]*                                                                                  | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `refresh`                                                                                        | *Optional[bool]*                                                                                 | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `pretty`                                                                                         | *Optional[bool]*                                                                                 | :heavy_minus_sign:                                                                               | Return a simplified payload with only name, description, annotations, and a compact inputSchema. |
| `credentials_name`                                                                               | *OptionalNullable[str]*                                                                          | :heavy_minus_sign:                                                                               | N/A                                                                                              |
| `retries`                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                 | :heavy_minus_sign:                                                                               | Configuration to override the default retry behavior of the client.                              |

### Response

**[models.ResponseConnectorListToolsV1](../../models/responseconnectorlisttoolsv1.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_authentication_methods

Get the authentication schema for a connector. Returns the list of supported authentication methods and their required headers.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_get_authentication_methods_v1" method="get" path="/v1/connectors/{connector_id_or_name}/authentication_methods" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.get_authentication_methods(connector_id_or_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.PublicAuthenticationMethod]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_organization_credentials

List all credentials configured at the organization level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_list_organization_credentials_v1" method="get" path="/v1/connectors/{connector_id_or_name}/organization/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list_organization_credentials(connector_id_or_name="<value>", fetch_default=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                            | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `auth_type`                                                                                       | [OptionalNullable[models.OutboundAuthenticationType]](../../models/outboundauthenticationtype.md) | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `fetch_default`                                                                                   | *Optional[bool]*                                                                                  | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.CredentialsResponse](../../models/credentialsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_workspace_credentials

List all credentials configured at the workspace level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_list_workspace_credentials_v1" method="get" path="/v1/connectors/{connector_id_or_name}/workspace/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list_workspace_credentials(connector_id_or_name="<value>", fetch_default=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                            | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `auth_type`                                                                                       | [OptionalNullable[models.OutboundAuthenticationType]](../../models/outboundauthenticationtype.md) | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `fetch_default`                                                                                   | *Optional[bool]*                                                                                  | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.CredentialsResponse](../../models/credentialsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_user_credentials

List all credentials configured at the user level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_list_user_credentials_v1" method="get" path="/v1/connectors/{connector_id_or_name}/user/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list_user_credentials(connector_id_or_name="<value>", fetch_default=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                            | *str*                                                                                             | :heavy_check_mark:                                                                                | N/A                                                                                               |
| `auth_type`                                                                                       | [OptionalNullable[models.OutboundAuthenticationType]](../../models/outboundauthenticationtype.md) | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `fetch_default`                                                                                   | *Optional[bool]*                                                                                  | :heavy_minus_sign:                                                                                | N/A                                                                                               |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.CredentialsResponse](../../models/credentialsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_all_user_credentials

Delete all credentials configured at the user level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_delete_all_user_credentials_v1" method="delete" path="/v1/connectors/{connector_id_or_name}/user/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.delete_all_user_credentials(connector_id_or_name="5d332e4a-b496-4634-bfa5-8233e837b143")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create_credentials

Create consumer credentials for a given connector and consumer scope (organization, workspace, user)

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_create_credentials_v1" method="post" path="/v1/connectors/{connector_id_or_name}/{consumer_scope}/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.create_credentials(connector_id_or_name="b7170011-bca4-40c2-8f3d-4f646a544062", consumer_scope="organization", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Required                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `consumer_scope`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | [models.ConnectorCreateCredentialsV1ConsumerScope](../../models/connectorcreatecredentialsv1consumerscope.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `name`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Name of the credentials. Use this name to access or modify your credentials.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `title`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Human-readable title for the credentials.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `is_default`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | *OptionalNullable[bool]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Controls whether this credential is the default for its auth method. On creation: if no credential exists yet for this auth method, the credential is automatically set as default when is_default is true or omitted; setting is_default to false is rejected because a default must exist. If other credentials already exist, setting is_default to true promotes this credential (demoting the previous default); false or omitted creates it as non-default. On update: true promotes this credential, false is rejected if it is currently the default (promote another credential first), omitted leaves the default status unchanged. |
| `credentials`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | [OptionalNullable[models.ConnectionCredentialsInput]](../../models/connectioncredentialsinput.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | The credential data (headers, bearer_token, or OAuth2 client credentials).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update_credentials

Create or update consumer credentials for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_update_credentials" method="patch" path="/v1/connectors/{connector_id_or_name}/{consumer_scope}/credentials" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.update_credentials(connector_id_or_name="7b7eceb1-b6c5-44e4-8382-f2bba1886c77", consumer_scope="workspace", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Required                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `consumer_scope`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | [models.ConnectorUpdateCredentialsConsumerScope](../../models/connectorupdatecredentialsconsumerscope.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `name`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Name of the credentials. Use this name to access or modify your credentials.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `title`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | *OptionalNullable[str]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Human-readable title for the credentials.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `is_default`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | *OptionalNullable[bool]*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Controls whether this credential is the default for its auth method. On creation: if no credential exists yet for this auth method, the credential is automatically set as default when is_default is true or omitted; setting is_default to false is rejected because a default must exist. If other credentials already exist, setting is_default to true promotes this credential (demoting the previous default); false or omitted creates it as non-default. On update: true promotes this credential, false is rejected if it is currently the default (promote another credential first), omitted leaves the default status unchanged. |
| `credentials`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | [OptionalNullable[models.ConnectionCredentialsInput]](../../models/connectioncredentialsinput.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | The credential data (headers, bearer_token, or OAuth2 client credentials).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_organization_credentials

Delete credentials at the organization level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_delete_organization_credentials_v1" method="delete" path="/v1/connectors/{connector_id_or_name}/organization/credentials/{credentials_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.delete_organization_credentials(credentials_name="<value>", connector_id_or_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `credentials_name`                                                  | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_workspace_credentials

Delete credentials at the workspace level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_delete_workspace_credentials_v1" method="delete" path="/v1/connectors/{connector_id_or_name}/workspace/credentials/{credentials_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.delete_workspace_credentials(credentials_name="<value>", connector_id_or_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `credentials_name`                                                  | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete_user_credentials

Delete credentials at the user level for a given connector.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_delete_user_credentials_v1" method="delete" path="/v1/connectors/{connector_id_or_name}/user/credentials/{credentials_name}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.delete_user_credentials(credentials_name="<value>", connector_id_or_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `credentials_name`                                                  | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get a connector by its ID or name.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_get_v1" method="get" path="/v1/connectors/{connector_id_or_name}#idOrName" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.get(connector_id_or_name="<value>", fetch_user_data=False, fetch_customer_data=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                  | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `fetch_user_data`                                                                       | *Optional[bool]*                                                                        | :heavy_minus_sign:                                                                      | Fetch the user-level data associated with the connector (e.g. connection credentials).  |
| `fetch_customer_data`                                                                   | *Optional[bool]*                                                                        | :heavy_minus_sign:                                                                      | Fetch the customer data associated with the connector (e.g. customer secrets / config). |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

### Response

**[models.Connector](../../models/connector.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update a connector by its ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_update_v1" method="patch" path="/v1/connectors/{connector_id}#id" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.update(connector_id="81d30634-113f-4dce-a89e-7786be2d8693", request_body={
        "protocol": "mcp",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                   | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `connector_id`                                                              | *str*                                                                       | :heavy_check_mark:                                                          | N/A                                                                         |
| `request_body`                                                              | [models.ConnectorUpdateV1Payload](../../models/connectorupdatev1payload.md) | :heavy_check_mark:                                                          | N/A                                                                         |
| `retries`                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)            | :heavy_minus_sign:                                                          | Configuration to override the default retry behavior of the client.         |

### Response

**[models.Connector](../../models/connector.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete a connector by its ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_delete_v1" method="delete" path="/v1/connectors/{connector_id}#id" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.delete(connector_id="5c3269fe-6a18-4216-b1fb-b093005874cd")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id`                                                      | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MessageResponse](../../models/messageresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |