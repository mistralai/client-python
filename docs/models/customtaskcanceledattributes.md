# CustomTaskCanceledAttributes

Attributes for custom task canceled events.


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `custom_task_id`                                                        | *str*                                                                   | :heavy_check_mark:                                                      | Unique identifier for the custom task within the workflow.              |
| `custom_task_type`                                                      | *str*                                                                   | :heavy_check_mark:                                                      | The type/category of the custom task (e.g., 'llm_call', 'api_request'). |
| `reason`                                                                | *OptionalNullable[str]*                                                 | :heavy_minus_sign:                                                      | Optional reason provided for the cancellation.                          |