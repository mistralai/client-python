# WorkflowExecutionSyncResponse

Response model for synchronous workflow execution


## Fields

| Field                                  | Type                                   | Required                               | Description                            |
| -------------------------------------- | -------------------------------------- | -------------------------------------- | -------------------------------------- |
| `workflow_name`                        | *str*                                  | :heavy_check_mark:                     | Name of the workflow that was executed |
| `execution_id`                         | *str*                                  | :heavy_check_mark:                     | ID of the workflow execution           |
| `result`                               | *Any*                                  | :heavy_check_mark:                     | The result of the workflow execution   |