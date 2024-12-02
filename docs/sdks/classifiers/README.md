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

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.classifiers.moderate(inputs=[
    "<value>",
])

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                                         | Type                                                                              | Required                                                                          | Description                                                                       |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `inputs`                                                                          | [models.ClassificationRequestInputs](../../models/classificationrequestinputs.md) | :heavy_check_mark:                                                                | Text to classify.                                                                 |
| `model`                                                                           | *OptionalNullable[str]*                                                           | :heavy_minus_sign:                                                                | N/A                                                                               |
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

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.classifiers.moderate_chat(inputs=[
    [
        {
            "content": [
                {
                    "text": "<value>",
                },
            ],
        },
    ],
], model="V90")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `inputs`                                                                                  | [models.ChatClassificationRequestInputs](../../models/chatclassificationrequestinputs.md) | :heavy_check_mark:                                                                        | Chat to classify                                                                          |
| `model`                                                                                   | *Nullable[str]*                                                                           | :heavy_check_mark:                                                                        | N/A                                                                                       |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |

### Response

**[models.ClassificationResponse](../../models/classificationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |