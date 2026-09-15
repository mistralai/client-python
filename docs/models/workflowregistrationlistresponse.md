# WorkflowRegistrationListResponse


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `workflow_registrations`                                               | List[[models.WorkflowRegistration](../models/workflowregistration.md)] | :heavy_check_mark:                                                     | A list of workflow registrations                                       |
| `next_cursor`                                                          | *Nullable[str]*                                                        | :heavy_check_mark:                                                     | N/A                                                                    |
| `workflow_versions`                                                    | List[[models.WorkflowRegistration](../models/workflowregistration.md)] | :heavy_check_mark:                                                     | Deprecated: use workflow_registrations                                 |