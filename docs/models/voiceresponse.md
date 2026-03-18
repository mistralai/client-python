# VoiceResponse

Schema for voice response


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `name`                                                               | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `slug`                                                               | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `languages`                                                          | List[*str*]                                                          | :heavy_minus_sign:                                                   | N/A                                                                  |
| `gender`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `age`                                                                | *OptionalNullable[int]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `tags`                                                               | List[*str*]                                                          | :heavy_minus_sign:                                                   | N/A                                                                  |
| `color`                                                              | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `retention_notice`                                                   | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `id`                                                                 | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |
| `user_id`                                                            | *Nullable[str]*                                                      | :heavy_check_mark:                                                   | N/A                                                                  |