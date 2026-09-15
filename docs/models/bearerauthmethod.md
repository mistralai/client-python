# BearerAuthMethod


## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `method_type`                                                                            | *Literal["bearer"]*                                                                      | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `headers`                                                                                | List[[models.ConnectorAuthenticationHeader](../models/connectorauthenticationheader.md)] | :heavy_minus_sign:                                                                       | Optional additional headers sent with requests.                                          |