# VoiceCreateRequest

Request model for creating a new voice with base64 audio.


## Fields

| Field                                     | Type                                      | Required                                  | Description                               |
| ----------------------------------------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| `name`                                    | *str*                                     | :heavy_check_mark:                        | N/A                                       |
| `slug`                                    | *OptionalNullable[str]*                   | :heavy_minus_sign:                        | N/A                                       |
| `languages`                               | List[*str*]                               | :heavy_minus_sign:                        | N/A                                       |
| `gender`                                  | *OptionalNullable[str]*                   | :heavy_minus_sign:                        | N/A                                       |
| `age`                                     | *OptionalNullable[int]*                   | :heavy_minus_sign:                        | N/A                                       |
| `tags`                                    | List[*str*]                               | :heavy_minus_sign:                        | N/A                                       |
| `color`                                   | *OptionalNullable[str]*                   | :heavy_minus_sign:                        | N/A                                       |
| `retention_notice`                        | *Optional[int]*                           | :heavy_minus_sign:                        | N/A                                       |
| `sample_audio`                            | *str*                                     | :heavy_check_mark:                        | Base64-encoded audio file                 |
| `sample_filename`                         | *OptionalNullable[str]*                   | :heavy_minus_sign:                        | Original filename for extension detection |