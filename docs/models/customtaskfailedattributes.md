# CustomTaskFailedAttributes

Attributes for custom task failed events.


## Fields

| Field                                                                   | Type                                                                    | Required                                                                | Description                                                             |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `custom_task_id`                                                        | *str*                                                                   | :heavy_check_mark:                                                      | Unique identifier for the custom task within the workflow.              |
| `custom_task_type`                                                      | *str*                                                                   | :heavy_check_mark:                                                      | The type/category of the custom task (e.g., 'llm_call', 'api_request'). |
| `failure`                                                               | [models.Failure](../models/failure.md)                                  | :heavy_check_mark:                                                      | Represents an error or exception that occurred during execution.        |