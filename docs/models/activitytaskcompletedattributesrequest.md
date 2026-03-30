# ActivityTaskCompletedAttributesRequest

Attributes for activity task completed events.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `task_id`                                                                                      | *str*                                                                                          | :heavy_check_mark:                                                                             | Unique identifier for the activity task within the workflow.                                   |
| `activity_name`                                                                                | *str*                                                                                          | :heavy_check_mark:                                                                             | The registered name of the activity being executed.                                            |
| `result`                                                                                       | [models.JSONPayloadRequest](../models/jsonpayloadrequest.md)                                   | :heavy_check_mark:                                                                             | A payload containing arbitrary JSON data.<br/><br/>Used for complete state snapshots or final results. |