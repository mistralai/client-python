# OAuth2Token


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `access_token`                                                       | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `token_type`                                                         | *Optional[Literal["Bearer"]]*                                        | :heavy_minus_sign:                                                   | N/A                                                                  |
| `expires_in`                                                         | *OptionalNullable[int]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `scope`                                                              | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `refresh_token`                                                      | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `expires_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |