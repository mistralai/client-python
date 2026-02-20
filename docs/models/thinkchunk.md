# ThinkChunk


## Fields

| Field                                                                           | Type                                                                            | Required                                                                        | Description                                                                     |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `type`                                                                          | *Optional[Literal["thinking"]]*                                                 | :heavy_minus_sign:                                                              | N/A                                                                             |
| `thinking`                                                                      | List[[models.Thinking](../models/thinking.md)]                                  | :heavy_check_mark:                                                              | N/A                                                                             |
| `closed`                                                                        | *Optional[bool]*                                                                | :heavy_minus_sign:                                                              | Whether the thinking chunk is closed or not. Currently only used for prefixing. |