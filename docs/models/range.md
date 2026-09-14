# Range

Check that the given field falls in a range.

Requires at least one operator.


## Fields

| Field                                            | Type                                             | Required                                         | Description                                      |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| `type`                                           | *Literal["range"]*                               | :heavy_check_mark:                               | N/A                                              |
| `field`                                          | *str*                                            | :heavy_check_mark:                               | N/A                                              |
| `gt`                                             | [OptionalNullable[models.Gt]](../models/gt.md)   | :heavy_minus_sign:                               | N/A                                              |
| `gte`                                            | [OptionalNullable[models.Gte]](../models/gte.md) | :heavy_minus_sign:                               | N/A                                              |
| `lt`                                             | [OptionalNullable[models.Lt]](../models/lt.md)   | :heavy_minus_sign:                               | N/A                                              |
| `lte`                                            | [OptionalNullable[models.Lte]](../models/lte.md) | :heavy_minus_sign:                               | N/A                                              |