# WorkflowBulkUnarchiveResponse


## Fields

| Field                                                                       | Type                                                                        | Required                                                                    | Description                                                                 |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `unarchived`                                                                | List[[models.Workflow](../models/workflow.md)]                              | :heavy_check_mark:                                                          | Workflows that were successfully unarchived or were already unarchived      |
| `errored`                                                                   | List[[models.WorkflowBulkError](../models/workflowbulkerror.md)]            | :heavy_minus_sign:                                                          | Workflows that could not be unarchived and the corresponding error messages |