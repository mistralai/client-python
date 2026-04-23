# PublicAuthenticationMethod

Public view of an authentication method, without secrets.


## Fields

| Field                                                                                    | Type                                                                                     | Required                                                                                 | Description                                                                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `method_type`                                                                            | [models.OutboundAuthenticationType](../models/outboundauthenticationtype.md)             | :heavy_check_mark:                                                                       | N/A                                                                                      |
| `headers`                                                                                | List[[models.ConnectorAuthenticationHeader](../models/connectorauthenticationheader.md)] | :heavy_minus_sign:                                                                       | N/A                                                                                      |