# TransferCallTool


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `type`                                                                     | *Literal["transfer_call"]*                                                 | :heavy_check_mark:                                                         | N/A                                                                        |
| `destinations`                                                             | List[[models.TransferTarget](../models/transfertarget.md)]                 | :heavy_check_mark:                                                         | N/A                                                                        |
| `filler`                                                                   | [OptionalNullable[models.StaticToolFiller]](../models/statictoolfiller.md) | :heavy_minus_sign:                                                         | N/A                                                                        |