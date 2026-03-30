# ConnectorCallToolV1Request


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `tool_name`                                                              | *str*                                                                    | :heavy_check_mark:                                                       | N/A                                                                      |
| `credentials_name`                                                       | *OptionalNullable[str]*                                                  | :heavy_minus_sign:                                                       | N/A                                                                      |
| `connector_id_or_name`                                                   | *str*                                                                    | :heavy_check_mark:                                                       | N/A                                                                      |
| `connector_call_tool_request`                                            | [models.ConnectorCallToolRequest](../models/connectorcalltoolrequest.md) | :heavy_check_mark:                                                       | N/A                                                                      |