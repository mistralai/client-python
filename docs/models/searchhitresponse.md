# SearchHitResponse


## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `chunk`                                                         | [models.SearchChunkResponse](../models/searchchunkresponse.md)  | :heavy_check_mark:                                              | Wire chunk: atom fields plus any custom fields (via ``extra``). |
| `score`                                                         | *float*                                                         | :heavy_check_mark:                                              | N/A                                                             |
| `distance`                                                      | *OptionalNullable[float]*                                       | :heavy_minus_sign:                                              | N/A                                                             |
| `index_name`                                                    | *str*                                                           | :heavy_check_mark:                                              | N/A                                                             |