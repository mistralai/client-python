# GetWorkflowEventsV1WorkflowsEventsListGetRequest


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `root_workflow_exec_id`                                                | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Execution ID of the root workflow that initiated this execution chain. |
| `workflow_exec_id`                                                     | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Execution ID of the workflow that emitted this event.                  |
| `workflow_run_id`                                                      | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Run ID of the workflow that emitted this event.                        |
| `limit`                                                                | *Optional[int]*                                                        | :heavy_minus_sign:                                                     | Maximum number of events to return.                                    |
| `cursor`                                                               | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Cursor for pagination.                                                 |