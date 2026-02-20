# TranscriptionSegmentChunk


## Fields

| Field                                        | Type                                         | Required                                     | Description                                  |
| -------------------------------------------- | -------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| `type`                                       | *Optional[Literal["transcription_segment"]]* | :heavy_minus_sign:                           | N/A                                          |
| `text`                                       | *str*                                        | :heavy_check_mark:                           | N/A                                          |
| `start`                                      | *float*                                      | :heavy_check_mark:                           | N/A                                          |
| `end`                                        | *float*                                      | :heavy_check_mark:                           | N/A                                          |
| `score`                                      | *OptionalNullable[float]*                    | :heavy_minus_sign:                           | N/A                                          |
| `speaker_id`                                 | *OptionalNullable[str]*                      | :heavy_minus_sign:                           | N/A                                          |
| `__pydantic_extra__`                         | Dict[str, *Any*]                             | :heavy_minus_sign:                           | N/A                                          |