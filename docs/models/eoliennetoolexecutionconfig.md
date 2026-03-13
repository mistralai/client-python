# EolienneToolExecutionConfig


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `timeout`                                      | *Optional[float]*                              | :heavy_minus_sign:                             | N/A                                            |
| `max_execution_count`                          | *Optional[int]*                                | :heavy_minus_sign:                             | N/A                                            |
| `call_name_alias`                              | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | The name of the tool from the POV of the model |
| `path`                                         | *str*                                          | :heavy_check_mark:                             | N/A                                            |
| `rag`                                          | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `rag_single_result`                            | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `open_rag`                                     | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `image`                                        | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `code_interpreter`                             | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `open_search_single_result`                    | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `open_references`                              | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `send_user_id`                                 | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `send_customer_id`                             | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `image_domain_whitelist`                       | List[*str*]                                    | :heavy_minus_sign:                             | N/A                                            |
| `edit_image_recovery_threshold`                | *Optional[float]*                              | :heavy_minus_sign:                             | N/A                                            |
| `key`                                          | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | N/A                                            |
| `relative_positions_key`                       | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | N/A                                            |
| `tool_mapping`                                 | Dict[str, *str*]                               | :heavy_minus_sign:                             | N/A                                            |
| `read_only`                                    | *Optional[bool]*                               | :heavy_minus_sign:                             | N/A                                            |
| `type`                                         | *Literal["eolienne"]*                          | :heavy_check_mark:                             | N/A                                            |