# WorkflowBulkArchiveResponse


## Fields

| Field                                                                     | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `archived`                                                                | List[[models.Workflow](../models/workflow.md)]                            | :heavy_check_mark:                                                        | Workflows that were successfully archived or were already archived        |
| `errored`                                                                 | List[[models.WorkflowBulkError](../models/workflowbulkerror.md)]          | :heavy_minus_sign:                                                        | Workflows that could not be archived and the corresponding error messages |