# ImageContent

Image content for a message.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `type`                                                           | *Literal["image"]*                                               | :heavy_check_mark:                                               | N/A                                                              |
| `data`                                                           | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `mime_type`                                                      | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `annotations`                                                    | [OptionalNullable[models.Annotations]](../models/annotations.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `meta`                                                           | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |
| `__pydantic_extra__`                                             | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |