# ResourceLink

A resource that the server is capable of reading, included in a prompt or tool call result.

Note: resource links returned by tools are not guaranteed to appear in the results of `resources/list` requests.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `name`                                                           | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `title`                                                          | *OptionalNullable[str]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `uri`                                                            | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `description`                                                    | *OptionalNullable[str]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `mime_type`                                                      | *OptionalNullable[str]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `size`                                                           | *OptionalNullable[int]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `icons`                                                          | List[[models.MCPServerIcon](../models/mcpservericon.md)]         | :heavy_minus_sign:                                               | N/A                                                              |
| `annotations`                                                    | [OptionalNullable[models.Annotations]](../models/annotations.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `meta`                                                           | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |
| `type`                                                           | *Literal["resource_link"]*                                       | :heavy_check_mark:                                               | N/A                                                              |
| `__pydantic_extra__`                                             | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |