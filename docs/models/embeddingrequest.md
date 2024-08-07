# EmbeddingRequest


## Fields

| Field                                   | Type                                    | Required                                | Description                             |
| --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| `inputs`                                | [models.Inputs](../models/inputs.md)    | :heavy_check_mark:                      | Text to embed.                          |
| `model`                                 | *str*                                   | :heavy_check_mark:                      | ID of the model to use.                 |
| `encoding_format`                       | *OptionalNullable[str]*                 | :heavy_minus_sign:                      | The format to return the embeddings in. |