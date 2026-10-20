# ListAgentsV1AudioAgentsGetRequest


## Fields

| Field                                                   | Type                                                    | Required                                                | Description                                             |
| ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| `page_size`                                             | *Optional[int]*                                         | :heavy_minus_sign:                                      | Maximum number of agents to return                      |
| `page_token`                                            | *OptionalNullable[str]*                                 | :heavy_minus_sign:                                      | Cursor returned as next_page_token by the previous page |
| `search`                                                | *OptionalNullable[str]*                                 | :heavy_minus_sign:                                      | Substring match on the agent name                       |