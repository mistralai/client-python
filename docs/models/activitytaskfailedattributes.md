# ActivityTaskFailedAttributes

Attributes for activity task failed events (final failure after all retries).


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `task_id`                                                        | *str*                                                            | :heavy_check_mark:                                               | Unique identifier for the activity task within the workflow.     |
| `activity_name`                                                  | *str*                                                            | :heavy_check_mark:                                               | The registered name of the activity being executed.              |
| `attempt`                                                        | *int*                                                            | :heavy_check_mark:                                               | The final attempt number that failed (1-indexed).                |
| `failure`                                                        | [models.Failure](../models/failure.md)                           | :heavy_check_mark:                                               | Represents an error or exception that occurred during execution. |