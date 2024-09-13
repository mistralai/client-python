# ToolChoice

ToolChoice is either a ToolChoiceEnum or a ToolChoice


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `function`                                                                   | [models.FunctionName](../models/functionname.md)                             | :heavy_check_mark:                                                           | this restriction of `Function` is used to select a specific function to call |
| `type`                                                                       | [Optional[models.ToolTypes]](../models/tooltypes.md)                         | :heavy_minus_sign:                                                           | N/A                                                                          |