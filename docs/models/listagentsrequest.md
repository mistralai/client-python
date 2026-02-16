# ListAgentsRequest


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `page`                                                   | *Optional[int]*                                          | :heavy_minus_sign:                                       | Page number (0-indexed)                                  |
| `page_size`                                              | *Optional[int]*                                          | :heavy_minus_sign:                                       | Number of agents per page                                |
| `deployment_chat`                                        | *OptionalNullable[bool]*                                 | :heavy_minus_sign:                                       | N/A                                                      |
| `sources`                                                | List[[models.RequestSource](../models/requestsource.md)] | :heavy_minus_sign:                                       | N/A                                                      |
| `name`                                                   | *OptionalNullable[str]*                                  | :heavy_minus_sign:                                       | Filter by agent name                                     |
| `search`                                                 | *OptionalNullable[str]*                                  | :heavy_minus_sign:                                       | Search agents by name or ID                              |
| `id`                                                     | *OptionalNullable[str]*                                  | :heavy_minus_sign:                                       | N/A                                                      |
| `metadata`                                               | Dict[str, *Any*]                                         | :heavy_minus_sign:                                       | N/A                                                      |