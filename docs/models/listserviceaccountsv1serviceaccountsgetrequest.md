# ListServiceAccountsV1ServiceAccountsGetRequest


## Fields

| Field                                                         | Type                                                          | Required                                                      | Description                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| `workspace_id`                                                | *OptionalNullable[str]*                                       | :heavy_minus_sign:                                            | N/A                                                           |
| `include_deleted`                                             | *Optional[bool]*                                              | :heavy_minus_sign:                                            | N/A                                                           |
| `q`                                                           | *OptionalNullable[str]*                                       | :heavy_minus_sign:                                            | N/A                                                           |
| `order`                                                       | [Optional[models.SortOrder]](../models/sortorder.md)          | :heavy_minus_sign:                                            | Direction to sort a service-account listing by creation time. |
| `offset`                                                      | *int*                                                         | :heavy_check_mark:                                            | N/A                                                           |
| `limit`                                                       | *int*                                                         | :heavy_check_mark:                                            | N/A                                                           |