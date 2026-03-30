# CustomTaskStartedAttributesRequest

Attributes for custom task started events.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `custom_task_id`                                                                               | *str*                                                                                          | :heavy_check_mark:                                                                             | Unique identifier for the custom task within the workflow.                                     |
| `custom_task_type`                                                                             | *str*                                                                                          | :heavy_check_mark:                                                                             | The type/category of the custom task (e.g., 'llm_call', 'api_request').                        |
| `payload`                                                                                      | [Optional[models.JSONPayloadRequest]](../models/jsonpayloadrequest.md)                         | :heavy_minus_sign:                                                                             | A payload containing arbitrary JSON data.<br/><br/>Used for complete state snapshots or final results. |