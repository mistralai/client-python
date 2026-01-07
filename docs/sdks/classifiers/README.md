# Classifiers

## Overview

Classifiers API.

### Available Operations

* [moderate](#moderate) - Moderations
* [moderate_chat](#moderate_chat) - Chat Moderations
* [classify](#classify) - Classifications
* [classify_chat](#classify_chat) - Chat Classifications

## moderate

Moderations

### Example Usage

<!-- UsageSnippet language="python" operationID="moderations_v1_moderations_post" method="post" path="/v1/moderations" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.moderate(model="Durango", inputs=[
        "<value 1>",
        "<value 2>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       | Example                                                                           |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | ID of the model to use.                                                           | mistral-moderation-latest                                                         |
| `inputs`                                                                          | [models.ClassificationRequestInputs](../../models/classificationrequestinputs.md) | :heavy_check_mark:                                                                | Text to classify.                                                                 |                                                                                   |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |                                                                                   |

### Response

**[models.ModerationResponse](../../models/moderationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## moderate_chat

Chat Moderations

### Example Usage

<!-- UsageSnippet language="python" operationID="chat_moderations_v1_chat_moderations_post" method="post" path="/v1/chat/moderations" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.moderate_chat(inputs=[
        {
            "content": "<value>",
            "role": "tool",
        },
    ], model="LeBaron")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `inputs`                                                                          | [models.ChatModerationRequestInputs](../../models/chatmoderationrequestinputs.md) | :heavy_check_mark:                                                                | Chat to classify                                                                  |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | N/A                                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.ModerationResponse](../../models/moderationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## classify

Classifications

### Example Usage

<!-- UsageSnippet language="python" operationID="classifications_v1_classifications_post" method="post" path="/v1/classifications" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.classify(model="mistral-moderation-latest", inputs=[
        "<value 1>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       | Example                                                                           |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | ID of the model to use.                                                           | mistral-moderation-latest                                                         |
| `inputs`                                                                          | [models.ClassificationRequestInputs](../../models/classificationrequestinputs.md) | :heavy_check_mark:                                                                | Text to classify.                                                                 |                                                                                   |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |                                                                                   |

### Response

**[models.ClassificationResponse](../../models/classificationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## classify_chat

Chat Classifications

### Example Usage

<!-- UsageSnippet language="python" operationID="chat_classifications_v1_chat_classifications_post" method="post" path="/v1/chat/classifications" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.classify_chat(model="Camry", inputs=[
        {
            "messages": [
                {
                    "content": "<value>",
                    "role": "system",
                },
            ],
        },
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `model`                                                             | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `inputs`                                                            | [models.Inputs](../../models/inputs.md)                             | :heavy_check_mark:                                                  | Chat to classify                                                    |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ClassificationResponse](../../models/classificationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |