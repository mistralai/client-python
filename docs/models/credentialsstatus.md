# CredentialsStatus


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `status_type`                                                        | [models.AuthStatus](../models/authstatus.md)                         | :heavy_check_mark:                                                   | N/A                                                                  |
| `last_checked_at`                                                    | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `error_http_code`                                                    | [OptionalNullable[models.HTTPStatus]](../models/httpstatus.md)       | :heavy_minus_sign:                                                   | N/A                                                                  |
| `error_message`                                                      | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |