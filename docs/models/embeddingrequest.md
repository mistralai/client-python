# EmbeddingRequest


## Fields

| Field                                              | Type                                               | Required                                           | Description                                        | Example                                            |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `inputs`                                           | [models.Inputs](../models/inputs.md)               | :heavy_check_mark:                                 | Text to embed.                                     | [<br/>"Embed this sentence.",<br/>"As well as this one."<br/>] |
| `model`                                            | *Optional[str]*                                    | :heavy_minus_sign:                                 | ID of the model to use.                            |                                                    |
| `encoding_format`                                  | *OptionalNullable[str]*                            | :heavy_minus_sign:                                 | The format to return the embeddings in.            |                                                    |