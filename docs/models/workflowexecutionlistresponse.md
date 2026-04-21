# WorkflowExecutionListResponse

Deprecated: use WorkflowRunListResponse instead. Will be removed in the next major version.


## Fields

| Field                                                                                                      | Type                                                                                                       | Required                                                                                                   | Description                                                                                                |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `executions`                                                                                               | List[[models.WorkflowExecutionWithoutResultResponse](../models/workflowexecutionwithoutresultresponse.md)] | :heavy_check_mark:                                                                                         | A list of workflow executions                                                                              |
| `next_page_token`                                                                                          | *OptionalNullable[str]*                                                                                    | :heavy_minus_sign:                                                                                         | Token to use for fetching the next page of results. Null if this is the last page.                         |