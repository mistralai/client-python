# GetWorkflowsV1WorkflowsGetRequest


## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `active_only`                                                   | *Optional[bool]*                                                | :heavy_minus_sign:                                              | Whether to only return active workflows                         |
| `include_shared`                                                | *Optional[bool]*                                                | :heavy_minus_sign:                                              | Whether to include shared workflows                             |
| `available_in_chat_assistant`                                   | *OptionalNullable[bool]*                                        | :heavy_minus_sign:                                              | Whether to only return workflows compatible with chat assistant |
| `include_archived`                                              | *Optional[bool]*                                                | :heavy_minus_sign:                                              | Whether to include archived workflows                           |
| `cursor`                                                        | *OptionalNullable[str]*                                         | :heavy_minus_sign:                                              | The cursor for pagination                                       |
| `limit`                                                         | *OptionalNullable[int]*                                         | :heavy_minus_sign:                                              | The maximum number of workflows to return                       |