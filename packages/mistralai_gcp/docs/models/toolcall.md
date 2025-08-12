# ToolCall


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `id`                                                       | *Optional[str]*                                            | :heavy_minus_sign:                                         | N/A                                                        |
| `type`                                                     | [Optional[models.ToolTypes]](../models/tooltypes.md)       | :heavy_minus_sign:                                         | N/A                                                        |
| `function`                                                 | [models.FunctionCall](../models/functioncall.md)           | :heavy_check_mark:                                         | N/A                                                        |
| `index`                                                    | *Optional[int]*                                            | :heavy_minus_sign:                                         | N/A                                                        |
| `metadata`                                                 | [OptionalNullable[models.Metadata]](../models/metadata.md) | :heavy_minus_sign:                                         | N/A                                                        |