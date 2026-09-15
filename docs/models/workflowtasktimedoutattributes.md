# WorkflowTaskTimedOutAttributes

Attributes for workflow task timed out events.


## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `task_id`                                                                        | *str*                                                                            | :heavy_check_mark:                                                               | Unique identifier for the task within the workflow execution.                    |
| `timeout_type`                                                                   | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | The type of timeout that occurred (e.g., 'START_TO_CLOSE', 'SCHEDULE_TO_START'). |