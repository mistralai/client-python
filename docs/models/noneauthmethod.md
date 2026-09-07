# NoneAuthMethod


## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `method_type`                                                                            | *Literal["none"]*                                                                        | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `headers`                                                                                | List[[models.ConnectorAuthenticationHeader](../models/connectorauthenticationheader.md)] | :heavy_minus_sign:                                                                       | Headers whose values must be provided as credentials.                                    |