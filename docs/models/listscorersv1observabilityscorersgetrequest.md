# ListScorersV1ObservabilityScorersGetRequest


## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `created_by_me`                                              | *Optional[bool]*                                             | :heavy_minus_sign:                                           | Only return scorers created by the current user              |
| `ootb`                                                       | *Optional[bool]*                                             | :heavy_minus_sign:                                           | Only return out-of-the-box scorers                           |
| `q`                                                          | *OptionalNullable[str]*                                      | :heavy_minus_sign:                                           | Case-insensitive filter on scorer slug, name, or description |
| `page_size`                                                  | *Optional[int]*                                              | :heavy_minus_sign:                                           | N/A                                                          |
| `page`                                                       | *Optional[int]*                                              | :heavy_minus_sign:                                           | N/A                                                          |