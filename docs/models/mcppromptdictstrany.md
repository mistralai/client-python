# MCPPromptDictStrAny


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `name`                                                     | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `title`                                                    | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `description`                                              | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `arguments`                                                | List[[models.PromptArgument](../models/promptargument.md)] | :heavy_minus_sign:                                         | N/A                                                        |
| `icons`                                                    | List[[models.MCPServerIcon](../models/mcpservericon.md)]   | :heavy_minus_sign:                                         | N/A                                                        |
| `meta`                                                     | Dict[str, *Any*]                                           | :heavy_minus_sign:                                         | N/A                                                        |
| `__pydantic_extra__`                                       | Dict[str, *Any*]                                           | :heavy_minus_sign:                                         | N/A                                                        |