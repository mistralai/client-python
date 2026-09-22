# WorkflowScheduleListResponse


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `schedules`                                                                    | List[[models.ScheduleDefinitionOutput](../models/scheduledefinitionoutput.md)] | :heavy_check_mark:                                                             | A list of workflow schedules                                                   |
| `next_page_token`                                                              | *OptionalNullable[str]*                                                        | :heavy_minus_sign:                                                             | Token for the next page of results                                             |