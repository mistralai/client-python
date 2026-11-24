# ResponseFormat

Specify the format that the model must output. By default it will use `{ "type": "text" }`. Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is in JSON. When using JSON mode you MUST also instruct the model to produce JSON yourself with a system or a user message. Setting to `{ "type": "json_schema" }` enables JSON schema mode, which guarantees the message the model generates is in JSON and follows the schema you provide. Note: on third-party models (for example GLM), the schema is still enforced, but field descriptions may not influence the output; put field-level requirements in the prompt.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `type`                                                           | [Optional[models.ResponseFormats]](../models/responseformats.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `json_schema`                                                    | [OptionalNullable[models.JSONSchema]](../models/jsonschema.md)   | :heavy_minus_sign:                                               | N/A                                                              |