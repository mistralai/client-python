# ThinkChunk


## Fields

| Field                                                                           | Type                                                                            | Required                                                                        | Description                                                                     |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `type`                                                                          | *Literal["thinking"]*                                                           | :heavy_check_mark:                                                              | N/A                                                                             |
| `thinking`                                                                      | List[[models.ThinkChunkThinking](../models/thinkchunkthinking.md)]              | :heavy_check_mark:                                                              | N/A                                                                             |
| `closed`                                                                        | *Optional[bool]*                                                                | :heavy_minus_sign:                                                              | Whether the thinking chunk is closed or not. Currently only used for prefixing. |