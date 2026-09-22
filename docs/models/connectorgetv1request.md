# ConnectorGetV1Request


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `connector_id_or_name`                                                                 | *str*                                                                                  | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `fetch_user_data`                                                                      | *Optional[bool]*                                                                       | :heavy_minus_sign:                                                                     | Fetch the user-level data associated with the connector (e.g. connection credentials). |