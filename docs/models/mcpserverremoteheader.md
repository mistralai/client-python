# MCPServerRemoteHeader

Header definition for a remote transport (SEP-2127).


## Fields

| Field                                    | Type                                     | Required                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `name`                                   | *str*                                    | :heavy_check_mark:                       | Header name                              |
| `description`                            | *str*                                    | :heavy_check_mark:                       | Human-readable description of the header |
| `is_required`                            | *OptionalNullable[bool]*                 | :heavy_minus_sign:                       | N/A                                      |
| `is_secret`                              | *OptionalNullable[bool]*                 | :heavy_minus_sign:                       | N/A                                      |
| `default`                                | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | N/A                                      |
| `choices`                                | List[*str*]                              | :heavy_minus_sign:                       | N/A                                      |