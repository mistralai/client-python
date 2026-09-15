# EmbeddedResource

The contents of a resource, embedded into a prompt or tool call result.

It is up to the client how best to render embedded resources for the benefit
of the LLM and/or the user.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `type`                                                           | *Literal["resource"]*                                            | :heavy_check_mark:                                               | N/A                                                              |
| `resource`                                                       | [models.Resource](../models/resource.md)                         | :heavy_check_mark:                                               | N/A                                                              |
| `annotations`                                                    | [OptionalNullable[models.Annotations]](../models/annotations.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `meta`                                                           | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |
| `__pydantic_extra__`                                             | Dict[str, *Any*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |