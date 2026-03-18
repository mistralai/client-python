# WorkflowEventResponse

Response model for workflow event reception.


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `status`                                                                       | [models.WorkflowEventResponseStatus](../models/workfloweventresponsestatus.md) | :heavy_check_mark:                                                             | Status of the event reception                                                  |
| `message`                                                                      | *OptionalNullable[str]*                                                        | :heavy_minus_sign:                                                             | Optional message                                                               |