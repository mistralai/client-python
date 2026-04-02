# CustomConnector


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `type`                                                                       | *Literal["connector"]*                                                       | :heavy_check_mark:                                                           | N/A                                                                          |
| `connector_id`                                                               | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          |
| `authorization`                                                              | [OptionalNullable[models.Authorization]](../models/authorization.md)         | :heavy_minus_sign:                                                           | N/A                                                                          |
| `tool_configuration`                                                         | [OptionalNullable[models.ToolConfiguration]](../models/toolconfiguration.md) | :heavy_minus_sign:                                                           | N/A                                                                          |