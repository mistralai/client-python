# WebPublicToolExecutionConfig


## Fields

| Field                                              | Type                                               | Required                                           | Description                                        |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `timeout`                                          | *Optional[float]*                                  | :heavy_minus_sign:                                 | N/A                                                |
| `max_execution_count`                              | *Optional[int]*                                    | :heavy_minus_sign:                                 | N/A                                                |
| `call_name_alias`                                  | *OptionalNullable[str]*                            | :heavy_minus_sign:                                 | The name of the tool from the POV of the model     |
| `path`                                             | *str*                                              | :heavy_check_mark:                                 | N/A                                                |
| `operation_type`                                   | [models.OperationType](../models/operationtype.md) | :heavy_check_mark:                                 | N/A                                                |
| `operation`                                        | Dict[str, *Any*]                                   | :heavy_check_mark:                                 | N/A                                                |
| `type`                                             | *Literal["web_public"]*                            | :heavy_check_mark:                                 | N/A                                                |