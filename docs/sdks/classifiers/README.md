# Classifiers
(*classifiers*)

## Overview

Classifiers API.

### Available Operations

* [moderate](#moderate) - Moderations
* [moderate_chat](#moderate_chat) - Moderations Chat

## moderate

Moderations

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.moderate(model="V90", inputs=[
        "<value>",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | ID of the model to use.                                                           |
| `inputs`                                                                          | [models.ClassificationRequestInputs](../../models/classificationrequestinputs.md) | :heavy_check_mark:                                                                | Text to classify.                                                                 |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.ClassificationResponse](../../models/classificationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

## moderate_chat

Moderations Chat

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.classifiers.moderate_chat(model="Roadster", inputs=[
        [
            {
                "content": "<value>",
                "role": "tool",
            },
            {
                "content": "<value>",
                "role": "tool",
            },
            {
                "content": "<value>",
                "role": "tool",
            },
        ],
        [
            {
                "prefix": False,
                "role": "assistant",
            },
            {
                "content": "<value>",
                "role": "user",
            },
            {
                "prefix": False,
                "role": "assistant",
            },
        ],
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `model`                                                                           | *str*                                                                             | :heavy_check_mark:                                                                | N/A                                                                               |
| `inputs`                                                                          | [models.ChatModerationRequestInputs](../../models/chatmoderationrequestinputs.md) | :heavy_check_mark:                                                                | Chat to classify                                                                  |
| `truncate_for_context_length`                                                     | *Optional[bool]*                                                                  | :heavy_minus_sign:                                                                | N/A                                                                               |
| `retries`                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                  | :heavy_minus_sign:                                                                | Configuration to override the default retry behavior of the client.               |

### Response

**[models.ClassificationResponse](../../models/classificationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |