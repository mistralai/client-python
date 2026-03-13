# ToolExecutionData

All the data needed to execute tools server-side


## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `stop_after_tools_execution`                                 | *Optional[bool]*                                             | :heavy_minus_sign:                                           | N/A                                                          |
| `display_completion_available_tools`                         | *Optional[bool]*                                             | :heavy_minus_sign:                                           | N/A                                                          |
| `integrations`                                               | List[[models.IntegrationData](../models/integrationdata.md)] | :heavy_minus_sign:                                           | N/A                                                          |
| `tools`                                                      | List[[models.ToolData](../models/tooldata.md)]               | :heavy_minus_sign:                                           | N/A                                                          |