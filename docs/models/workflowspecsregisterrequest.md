# WorkflowSpecsRegisterRequest


## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `definitions`                                                                    | List[[models.WorkflowSpecWithTaskQueue](../models/workflowspecwithtaskqueue.md)] | :heavy_check_mark:                                                               | List of workflow specs to register                                               |
| `deployment_name`                                                                | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Name of the deployment this worker belongs to                                    |
| `worker_id`                                                                      | *OptionalNullable[str]*                                                          | :heavy_minus_sign:                                                               | Stable identity of this worker instance                                          |