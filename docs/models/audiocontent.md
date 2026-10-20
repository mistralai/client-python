# AudioContent

Audio provided to or from an LLM.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `type`                                                           | *Literal["audio"]*                                               | :heavy_check_mark:                                               | N/A                                                              |
| `data`                                                           | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `mime_type`                                                      | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `annotations`                                                    | [OptionalNullable[models.Annotations]](../models/annotations.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `meta`                                                           | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |