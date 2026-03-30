# Beta.Observability.ChatCompletionEvents.Fields

## Overview

### Available Operations

* [list](#list) - Get Chat Completion Fields
* [fetch_options](#fetch_options) - Get Chat Completion Field Options
* [fetch_option_counts](#fetch_option_counts) - Get Chat Completion Field Options Counts

## list

Get Chat Completion Fields

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_fields_v1_observability_chat_completion_fields_get" method="get" path="/v1/observability/chat-completion-fields" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.fields.list()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListChatCompletionFieldsResponse](../../models/listchatcompletionfieldsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_options

Get Chat Completion Field Options

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_field_options_v1_observability_chat_completion_fields__field_name__options_get" method="get" path="/v1/observability/chat-completion-fields/{field_name}/options" -->
```python
from mistralai.client import Mistral, models
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.fields.fetch_options(field_name="<value>", operator=models.Operator.STARTSWITH)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `field_name`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `operator`                                                          | [models.Operator](../../models/operator.md)                         | :heavy_check_mark:                                                  | The operator to use for filtering options                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.FetchChatCompletionFieldOptionsResponse](../../models/fetchchatcompletionfieldoptionsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_option_counts

Get Chat Completion Field Options Counts

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_field_options_counts_v1_observability_chat_completion_fields__field_name__options_counts_post" method="post" path="/v1/observability/chat-completion-fields/{field_name}/options-counts" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.fields.fetch_option_counts(field_name="<value>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `field_name`                                                            | *str*                                                                   | :heavy_check_mark:                                                      | N/A                                                                     |
| `filter_params`                                                         | [OptionalNullable[models.FilterPayload]](../../models/filterpayload.md) | :heavy_minus_sign:                                                      | N/A                                                                     |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |

### Response

**[models.FetchFieldOptionCountsResponse](../../models/fetchfieldoptioncountsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |