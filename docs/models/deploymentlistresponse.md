# DeploymentListResponse


## Fields

| Field                                                              | Type                                                               | Required                                                           | Description                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `deployments`                                                      | List[[models.DeploymentResponse](../models/deploymentresponse.md)] | :heavy_check_mark:                                                 | List of deployments                                                |
| `next_cursor`                                                      | *Nullable[str]*                                                    | :heavy_check_mark:                                                 | Cursor for the next page of results                                |
| `workspace_id`                                                     | *str*                                                              | :heavy_check_mark:                                                 | Workspace ID the results are scoped to                             |