# WorkflowBulkError


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `workflow_id`                                              | *str*                                                      | :heavy_check_mark:                                         | The requested workflow ID                                  |
| `workflow`                                                 | [OptionalNullable[models.Workflow]](../models/workflow.md) | :heavy_minus_sign:                                         | The workflow, if found                                     |
| `message`                                                  | *str*                                                      | :heavy_check_mark:                                         | Error message describing why the operation failed          |