# VoiceAgentFunctionToolRequest


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `type`                                                                     | *Literal["function"]*                                                      | :heavy_check_mark:                                                         | N/A                                                                        |
| `function`                                                                 | [models.FunctionRequest](../models/functionrequest.md)                     | :heavy_check_mark:                                                         | N/A                                                                        |
| `filler`                                                                   | [OptionalNullable[models.StaticToolFiller]](../models/statictoolfiller.md) | :heavy_minus_sign:                                                         | N/A                                                                        |
| `timeout_ms`                                                               | *OptionalNullable[int]*                                                    | :heavy_minus_sign:                                                         | N/A                                                                        |