# MCPServerAuthenticationRequirement

Authentication requirements for a remote transport (SEP-2127).


## Fields

| Field                                         | Type                                          | Required                                      | Description                                   |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| `required`                                    | *bool*                                        | :heavy_check_mark:                            | Whether authentication is mandatory           |
| `schemes`                                     | List[*str*]                                   | :heavy_minus_sign:                            | Supported schemes (e.g. ['bearer', 'oauth2']) |