# Embeddings
(*embeddings*)

## Overview

Embeddings API.

### Available Operations

* [create](#create) - Embeddings

## create

Embeddings

### Example Usage

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)


res = s.embeddings.create(inputs="<value>", model="<value>")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `inputs`                                                            | [models.Inputs](../../models/inputs.md)                             | :heavy_check_mark:                                                  | Text to embed.                                                      |
| `model`                                                             | *str*                                                               | :heavy_check_mark:                                                  | ID of the model to use.                                             |
| `encoding_format`                                                   | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The format to return the embeddings in.                             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EmbeddingResponse](../../models/embeddingresponse.md)**

### Errors

| Error Object               | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4xx-5xx                    | */*                        |
