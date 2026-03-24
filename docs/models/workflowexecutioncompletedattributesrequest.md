# WorkflowExecutionCompletedAttributesRequest

Attributes for workflow execution completed events.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `task_id`                                                                                      | *str*                                                                                          | :heavy_check_mark:                                                                             | Unique identifier for the task within the workflow execution.                                  |
| `result`                                                                                       | [models.JSONPayloadRequest](../models/jsonpayloadrequest.md)                                   | :heavy_check_mark:                                                                             | A payload containing arbitrary JSON data.<br/><br/>Used for complete state snapshots or final results. |