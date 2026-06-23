# ToolChoice

ToolChoice is either a ToolChoiceEnum or a ToolChoice


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `type`                                                                       | [Optional[models.ToolTypes]](../models/tooltypes.md)                         | :heavy_minus_sign:                                                           | N/A                                                                          |
| `function`                                                                   | [models.FunctionName](../models/functionname.md)                             | :heavy_check_mark:                                                           | this restriction of `Function` is used to select a specific function to call |