# ActivityTaskStartedAttributesResponse

Attributes for activity task started events.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `task_id`                                                                                      | *str*                                                                                          | :heavy_check_mark:                                                                             | Unique identifier for the activity task within the workflow.                                   |
| `activity_name`                                                                                | *str*                                                                                          | :heavy_check_mark:                                                                             | The registered name of the activity being executed.                                            |
| `input`                                                                                        | [models.JSONPayloadResponse](../models/jsonpayloadresponse.md)                                 | :heavy_check_mark:                                                                             | A payload containing arbitrary JSON data.<br/><br/>Used for complete state snapshots or final results. |