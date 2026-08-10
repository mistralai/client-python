# WorkflowExecutionFailedAttributes

Attributes for workflow execution failed events.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `task_id`                                                                            | *str*                                                                                | :heavy_check_mark:                                                                   | Unique identifier for the task within the workflow execution.                        |
| `failure`                                                                            | [models.Failure](../models/failure.md)                                               | :heavy_check_mark:                                                                   | Represents an error or exception that occurred during execution.                     |
| `attempt`                                                                            | *Optional[int]*                                                                      | :heavy_minus_sign:                                                                   | Workflow retry attempt number. 1 on first run and CAN; >1 on workflow-level retries. |