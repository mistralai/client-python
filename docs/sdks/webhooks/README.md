# Beta.Webhooks

## Overview

### Available Operations

* [list](#list) - List Webhooks
* [create](#create) - Create Webhook
* [get](#get) - Get Webhook
* [delete](#delete) - Delete Webhook
* [get_signing_secret](#get_signing_secret) - Get Webhook Signing Secret

## list

List Webhooks

### Example Usage

<!-- UsageSnippet language="python" operationID="list_webhooks_v1_webhooks_get" method="get" path="/v1/webhooks" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.webhooks.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.Webhook]](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## create

Create Webhook

### Example Usage

<!-- UsageSnippet language="python" operationID="create_webhook_v1_webhooks_post" method="post" path="/v1/webhooks" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.webhooks.create(provider="slack", name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                               | Type                                                                                                    | Required                                                                                                | Description                                                                                             |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `provider`                                                                                              | [models.WebhookProvider](../../models/webhookprovider.md)                                               | :heavy_check_mark:                                                                                      | N/A                                                                                                     |
| `name`                                                                                                  | *str*                                                                                                   | :heavy_check_mark:                                                                                      | Human-readable name for this webhook                                                                    |
| `owner_type`                                                                                            | [Optional[models.TriggersOwnerType]](../../models/triggersownertype.md)                                 | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `secret`                                                                                                | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Signing secret provided by the third-party provider                                                     |
| `encryption_key`                                                                                        | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Encryption key used to decrypt webhook payloads                                                         |
| `expires_at`                                                                                            | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                    | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `signature_hash_algorithm`                                                                              | [OptionalNullable[models.WebhookSignatureHashAlgorithm]](../../models/webhooksignaturehashalgorithm.md) | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `signature_header_name`                                                                                 | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `validity_period_second`                                                                                | *OptionalNullable[int]*                                                                                 | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `signature_extractor_regex`                                                                             | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Regex to extract signature, eg sha256=(.*)                                                              |
| `timestamp_extractor_regex`                                                                             | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `signature_payload_pattern`                                                                             | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Pattern for signature payload, eg {body} or {timestamp}.{body}                                          |
| `signature_encoding`                                                                                    | [OptionalNullable[models.WebhookSignatureEncoding]](../../models/webhooksignatureencoding.md)           | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `success_status_code`                                                                                   | *OptionalNullable[int]*                                                                                 | :heavy_minus_sign:                                                                                      | N/A                                                                                                     |
| `event_type_path`                                                                                       | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Path to extract event type, eg body.type or headers.X-GitHub-Event                                      |
| `retries`                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                        | :heavy_minus_sign:                                                                                      | Configuration to override the default retry behavior of the client.                                     |

### Response

**[models.Webhook](../../models/webhook.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get Webhook

### Example Usage

<!-- UsageSnippet language="python" operationID="get_webhook_v1_webhooks__webhook_id__get" method="get" path="/v1/webhooks/{webhook_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.webhooks.get(webhook_id="de67528b-7424-4bfa-98e4-5c117313e2ce")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `webhook_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.Webhook](../../models/webhook.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete Webhook

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_webhook_v1_webhooks__webhook_id__delete" method="delete" path="/v1/webhooks/{webhook_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.beta.webhooks.delete(webhook_id="97c2e685-f7cb-4949-a2cd-267a02c742c5")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `webhook_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_signing_secret

Get Webhook Signing Secret

### Example Usage

<!-- UsageSnippet language="python" operationID="get_webhook_signing_secret_v1_webhooks__webhook_id__signing_secret_get" method="get" path="/v1/webhooks/{webhook_id}/signing-secret" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.webhooks.get_signing_secret(webhook_id="171d0caa-bac1-4282-aeac-1fe92c67d7ff")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `webhook_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.WebhookSigningSecret](../../models/webhooksigningsecret.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |