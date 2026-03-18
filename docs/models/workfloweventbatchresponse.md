# WorkflowEventBatchResponse

Response model for batch workflow event reception.


## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `status`                                                                                 | [models.WorkflowEventBatchResponseStatus](../models/workfloweventbatchresponsestatus.md) | :heavy_check_mark:                                                                       | Status of the batch event reception                                                      |
| `message`                                                                                | *OptionalNullable[str]*                                                                  | :heavy_minus_sign:                                                                       | Optional message                                                                         |
| `events_received`                                                                        | *int*                                                                                    | :heavy_check_mark:                                                                       | Number of events successfully received                                                   |