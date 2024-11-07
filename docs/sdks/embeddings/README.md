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

res = s.embeddings.create(inputs=[
    "Embed this sentence.",
    "As well as this one.",
], model="Wrangler")

if res is not None:
    # handle response
    pass

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `inputs`                                                            | [models.Inputs](../../models/inputs.md)                             | :heavy_check_mark:                                                  | Text to embed.                                                      | [<br/>"Embed this sentence.",<br/>"As well as this one."<br/>]      |
| `model`                                                             | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | ID of the model to use.                                             |                                                                     |
| `encoding_format`                                                   | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | The format to return the embeddings in.                             |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.EmbeddingResponse](../../models/embeddingresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |