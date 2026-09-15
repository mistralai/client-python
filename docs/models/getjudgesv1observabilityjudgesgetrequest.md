# GetJudgesV1ObservabilityJudgesGetRequest


## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `type_filter`                                                | List[[models.JudgeOutputType](../models/judgeoutputtype.md)] | :heavy_minus_sign:                                           | Filter by judge output types                                 |
| `model_filter`                                               | List[*str*]                                                  | :heavy_minus_sign:                                           | Filter by model names                                        |
| `page_size`                                                  | *Optional[int]*                                              | :heavy_minus_sign:                                           | N/A                                                          |
| `page`                                                       | *Optional[int]*                                              | :heavy_minus_sign:                                           | N/A                                                          |
| `q`                                                          | *OptionalNullable[str]*                                      | :heavy_minus_sign:                                           | N/A                                                          |