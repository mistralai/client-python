# OpenReferenceToolExecutionConfig


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `timeout`                                      | *Optional[float]*                              | :heavy_minus_sign:                             | N/A                                            |
| `max_execution_count`                          | *Optional[int]*                                | :heavy_minus_sign:                             | N/A                                            |
| `call_name_alias`                              | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | The name of the tool from the POV of the model |
| `tool_mapping`                                 | Dict[str, *str*]                               | :heavy_check_mark:                             | N/A                                            |
| `type`                                         | *Literal["open_references"]*                   | :heavy_check_mark:                             | N/A                                            |