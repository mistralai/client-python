# CustomTaskCompletedAttributesResponse

Attributes for custom task completed events.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `custom_task_id`                                                                               | *str*                                                                                          | :heavy_check_mark:                                                                             | Unique identifier for the custom task within the workflow.                                     |
| `custom_task_type`                                                                             | *str*                                                                                          | :heavy_check_mark:                                                                             | The type/category of the custom task (e.g., 'llm_call', 'api_request').                        |
| `payload`                                                                                      | [models.JSONPayloadResponse](../models/jsonpayloadresponse.md)                                 | :heavy_check_mark:                                                                             | A payload containing arbitrary JSON data.<br/><br/>Used for complete state snapshots or final results. |