# WorkflowExecutionCanceledAttributes

Attributes for workflow execution canceled events.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `task_id`                                                                            | *str*                                                                                | :heavy_check_mark:                                                                   | Unique identifier for the task within the workflow execution.                        |
| `reason`                                                                             | *OptionalNullable[str]*                                                              | :heavy_minus_sign:                                                                   | Optional reason provided for the cancellation.                                       |
| `attempt`                                                                            | *Optional[int]*                                                                      | :heavy_minus_sign:                                                                   | Workflow retry attempt number. 1 on first run and CAN; >1 on workflow-level retries. |