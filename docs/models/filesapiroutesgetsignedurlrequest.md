# FilesAPIRoutesGetSignedURLRequest


## Fields

| Field                                                                                         | Type                                                                                          | Required                                                                                      | Description                                                                                   |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `file_id`                                                                                     | *str*                                                                                         | :heavy_check_mark:                                                                            | N/A                                                                                           |
| `expiry`                                                                                      | *Optional[int]*                                                                               | :heavy_minus_sign:                                                                            | Number of hours before the URL becomes invalid. Defaults to 24h. Must be between 1h and 168h. |