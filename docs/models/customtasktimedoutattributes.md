# CustomTaskTimedOutAttributes

Attributes for custom task timed out events.


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `custom_task_id`                                                        | *str*                                                                   | :heavy_check_mark:                                                      | Unique identifier for the custom task within the workflow.              |
| `custom_task_type`                                                      | *str*                                                                   | :heavy_check_mark:                                                      | The type/category of the custom task (e.g., 'llm_call', 'api_request'). |
| `timeout_type`                                                          | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | The type of timeout that occurred.                                      |