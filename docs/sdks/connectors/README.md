# Beta.Connectors

## Overview

(beta) Connectors API - manage your connectors

### Available Operations

* [create](#create) - Create a new connector.
* [list](#list) - List all connectors.
* [call_tool](#call_tool) - Call Connector Tool
* [list_internal](#list_internal) - Get All Internal
* [verify_mcp_connector_internal](#verify_mcp_connector_internal) - Verify Mcp Connector
* [get](#get) - Get a connector.
* [update](#update) - Update a connector.
* [delete](#delete) - Delete a connector.
* [get_internal](#get_internal) - Get Internal

## create

Create a new MCP connector. You can customize its visibility, url and auth type.

### Example Usage

<!-- UsageSnippet language="python" operationID="connector_create_v1" method="post" path="/v1/connectors" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.create(name="<value>", description="unibody usually despite slushy wherever reward stingy from", server="https://royal-majority.net/", mistral_integration=False, private_tool_execution=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `name`                                                                                              | *str*                                                                                               | :heavy_check_mark:                                                                                  | The name of the connector. Should be 64 char length maximum, alphanumeric, only underscores/dashes. |
| `description`                                                                                       | *str*                                                                                               | :heavy_check_mark:                                                                                  | The description of the connector.                                                                   |
| `server`                                                                                            | *str*                                                                                               | :heavy_check_mark:                                                                                  | The url of the MCP server.                                                                          |
| `icon_url`                                                                                          | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | The optional url of the icon you want to associate to the connector.                                |
| `visibility`                                                                                        | [Optional[models.ResourceVisibility]](../../models/resourcevisibility.md)                           | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `mistral_integration`                                                                               | *Optional[bool]*                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `private_tool_execution`                                                                            | *Optional[bool]*                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `customer_configuration_schema`                                                                     | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `customer_secrets_schema`                                                                           | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `user_configuration_schema`                                                                         | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `user_secrets_schema`                                                                               | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `connection_config`                                                                                 | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `connection_secrets`                                                                                | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `headers`                                                                                           | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | Optional organization-level headers to be sent with the request to the mcp server.                  |
| `auth_scheme`                                                                                       | [OptionalNullable[models.TurbineSecurityScheme]](../../models/turbinesecurityscheme.md)             | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `locale`                                                                                            | [OptionalNullable[models.ConnectorLocale]](../../models/connectorlocale.md)                         | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `auth_data`                                                                                         | [OptionalNullable[models.AuthData]](../../models/authdata.md)                                       | :heavy_minus_sign:                                                                                  | Optional additional authentication data for the connector.                                          |
| `system_prompt`                                                                                     | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | Optional system prompt for the connector.                                                           |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |

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
| `arguments`                                                         | Dict[str, *Any*]                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.MCPToolCallResponse](../../models/mcptoolcallresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## list_internal

Get All Internal

### Example Usage

<!-- UsageSnippet language="python" operationID="get_all_internal_v1_internal_connectors_get" method="get" path="/v1/internal/connectors" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.list_internal(page=0, page_size=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `query_filters`                                                                   | [Optional[models.ConnectorsQueryFilters]](../../models/connectorsqueryfilters.md) | :heavy_minus_sign:                                                                | N/A                                                                               |
| `cursor`                                                                          | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | N/A                                                                               |
| `page`                                                                            | *Optional[int]*                                                                   | :heavy_minus_sign:                                                                | N/A                                                                               |
| `page_size`                                                                       | *Optional[int]*                                                                   | :heavy_minus_sign:                                                                | N/A                                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.ResponseGetAllInternalV1InternalConnectorsGet](../../models/responsegetallinternalv1internalconnectorsget.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## verify_mcp_connector_internal

Verify Mcp Connector

### Example Usage

<!-- UsageSnippet language="python" operationID="verify_mcp_connector_v1_internal_connectors_verify_post" method="post" path="/v1/internal/connectors/verify" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.verify_mcp_connector_internal(name="<value>", description="confused bar crowded pish overstay loyally sure-footed bliss taxicab", server="https://unimportant-overcoat.org/", mistral_integration=False, private_tool_execution=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `name`                                                                                              | *str*                                                                                               | :heavy_check_mark:                                                                                  | The name of the connector. Should be 64 char length maximum, alphanumeric, only underscores/dashes. |
| `description`                                                                                       | *str*                                                                                               | :heavy_check_mark:                                                                                  | The description of the connector.                                                                   |
| `server`                                                                                            | *str*                                                                                               | :heavy_check_mark:                                                                                  | The url of the MCP server.                                                                          |
| `icon_url`                                                                                          | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | The optional url of the icon you want to associate to the connector.                                |
| `visibility`                                                                                        | [Optional[models.ResourceVisibility]](../../models/resourcevisibility.md)                           | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `mistral_integration`                                                                               | *Optional[bool]*                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `private_tool_execution`                                                                            | *Optional[bool]*                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `customer_configuration_schema`                                                                     | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `customer_secrets_schema`                                                                           | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `user_configuration_schema`                                                                         | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `user_secrets_schema`                                                                               | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `connection_config`                                                                                 | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `connection_secrets`                                                                                | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `headers`                                                                                           | Dict[str, *Any*]                                                                                    | :heavy_minus_sign:                                                                                  | Optional organization-level headers to be sent with the request to the mcp server.                  |
| `auth_scheme`                                                                                       | [OptionalNullable[models.TurbineSecurityScheme]](../../models/turbinesecurityscheme.md)             | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `locale`                                                                                            | [OptionalNullable[models.ConnectorLocale]](../../models/connectorlocale.md)                         | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |
| `auth_data`                                                                                         | [OptionalNullable[models.AuthData]](../../models/authdata.md)                                       | :heavy_minus_sign:                                                                                  | Optional additional authentication data for the connector.                                          |
| `system_prompt`                                                                                     | *OptionalNullable[str]*                                                                             | :heavy_minus_sign:                                                                                  | Optional system prompt for the connector.                                                           |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |

### Response

**[models.MCPVerificationResponse](../../models/mcpverificationresponse.md)**

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

    res = mistral.beta.connectors.get(connector_id_or_name="<value>", fetch_customer_data=False, fetch_connection_secrets=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                  | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `fetch_customer_data`                                                                   | *Optional[bool]*                                                                        | :heavy_minus_sign:                                                                      | Fetch the customer data associated with the connector (e.g. customer secrets / config). |
| `fetch_connection_secrets`                                                              | *Optional[bool]*                                                                        | :heavy_minus_sign:                                                                      | Fetch the general connection secrets associated with the connector.                     |
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

    res = mistral.beta.connectors.update(connector_id="81d30634-113f-4dce-a89e-7786be2d8693")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                               | Type                                                                                    | Required                                                                                | Description                                                                             |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `connector_id`                                                                          | *str*                                                                                   | :heavy_check_mark:                                                                      | N/A                                                                                     |
| `name`                                                                                  | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | The name of the connector.                                                              |
| `description`                                                                           | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | The description of the connector.                                                       |
| `icon_url`                                                                              | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | The optional url of the icon you want to associate to the connector.                    |
| `locale`                                                                                | [OptionalNullable[models.ConnectorLocale]](../../models/connectorlocale.md)             | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `system_prompt`                                                                         | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | Optional system prompt for the connector.                                               |
| `private_tool_execution`                                                                | *OptionalNullable[bool]*                                                                | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `connection_config`                                                                     | Dict[str, *Any*]                                                                        | :heavy_minus_sign:                                                                      | Optional new connection config.                                                         |
| `connection_secrets`                                                                    | Dict[str, *Any*]                                                                        | :heavy_minus_sign:                                                                      | Optional new connection secrets                                                         |
| `server`                                                                                | *OptionalNullable[str]*                                                                 | :heavy_minus_sign:                                                                      | New server url for your mcp connector.                                                  |
| `headers`                                                                               | Dict[str, *Any*]                                                                        | :heavy_minus_sign:                                                                      | New headers for your mcp connector.                                                     |
| `auth_data`                                                                             | [OptionalNullable[models.AuthData]](../../models/authdata.md)                           | :heavy_minus_sign:                                                                      | New authentication data for your mcp connector.                                         |
| `auth_scheme`                                                                           | [OptionalNullable[models.TurbineSecurityScheme]](../../models/turbinesecurityscheme.md) | :heavy_minus_sign:                                                                      | N/A                                                                                     |
| `retries`                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                        | :heavy_minus_sign:                                                                      | Configuration to override the default retry behavior of the client.                     |

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

## get_internal

Get Internal

### Example Usage

<!-- UsageSnippet language="python" operationID="get_internal_v1_internal_connectors__connector_id_or_name__get" method="get" path="/v1/internal/connectors/{connector_id_or_name}#idOrName" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.connectors.get_internal(connector_id_or_name="<value>", fetch_user_data=False, fetch_customer_data=False, fetch_connection_secrets=False, fetch_execution_data=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `connector_id_or_name`                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `fetch_user_data`                                                   | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fetch_customer_data`                                               | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fetch_connection_secrets`                                          | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `fetch_execution_data`                                              | *Optional[bool]*                                                    | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Connector](../../models/connector.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |