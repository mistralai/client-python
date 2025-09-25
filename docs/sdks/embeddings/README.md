# Embeddings
(*embeddings*)

## Overview

Embeddings API.

### Available Operations

* [create](#create) - Embeddings

## create

Embeddings

### Example Usage

<!-- UsageSnippet language="python" operationID="embeddings_v1_embeddings_post" method="post" path="/v1/embeddings" -->
```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.embeddings.create(model="mistral-embed", inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                               | Type                                                                    | Required                                                                | Description                                                             | Example                                                                 |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `model`                                                                 | *str*                                                                   | :heavy_check_mark:                                                      | ID of the model to use.                                                 | mistral-embed                                                           |
| `inputs`                                                                | [models.EmbeddingRequestInputs](../../models/embeddingrequestinputs.md) | :heavy_check_mark:                                                      | Text to embed.                                                          | [<br/>"Embed this sentence.",<br/>"As well as this one."<br/>]          |
| `output_dimension`                                                      | *OptionalNullable[int]*                                                 | :heavy_minus_sign:                                                      | The dimension of the output embeddings.                                 |                                                                         |
| `output_dtype`                                                          | [Optional[models.EmbeddingDtype]](../../models/embeddingdtype.md)       | :heavy_minus_sign:                                                      | N/A                                                                     |                                                                         |
| `encoding_format`                                                       | [Optional[models.EncodingFormat]](../../models/encodingformat.md)       | :heavy_minus_sign:                                                      | N/A                                                                     |                                                                         |
| `retries`                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)        | :heavy_minus_sign:                                                      | Configuration to override the default retry behavior of the client.     |                                                                         |

### Response

**[models.EmbeddingResponse](../../models/embeddingresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |