# DeploymentWorkerListResponse


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `workers`                                                                      | List[[models.DeploymentWorkerResponse](../models/deploymentworkerresponse.md)] | :heavy_check_mark:                                                             | Workers registered for the deployment                                          |
| `next_cursor`                                                                  | *Nullable[str]*                                                                | :heavy_check_mark:                                                             | Cursor for the next page of results                                            |