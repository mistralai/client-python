# UsersAPIListWorkspacesRequest


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            | Example                                                |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `organization_id`                                      | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | Return only workspaces belonging to this organization. | 1a2b3c4d-5e6f-4a8b-9c0d-1e2f3a4b5c6d                   |
| `offset`                                               | *Optional[int]*                                        | :heavy_minus_sign:                                     | Number of workspaces to skip before returning results. | 0                                                      |
| `limit`                                                | *Optional[int]*                                        | :heavy_minus_sign:                                     | Maximum number of workspaces to return.                | 100                                                    |