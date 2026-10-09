# JudgeDefinitionV1

The fully materialized LLM judge behavior stored in a pipeline config.


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `model`                                                          | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `prompt`                                                         | *str*                                                            | :heavy_check_mark:                                               | N/A                                                              |
| `temperature`                                                    | *OptionalNullable[float]*                                        | :heavy_minus_sign:                                               | N/A                                                              |
| `top_p`                                                          | *OptionalNullable[float]*                                        | :heavy_minus_sign:                                               | N/A                                                              |
| `max_tokens`                                                     | *OptionalNullable[int]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `random_seed`                                                    | *OptionalNullable[int]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `result_spec`                                                    | [models.EvaluationResultSpec](../models/evaluationresultspec.md) | :heavy_check_mark:                                               | N/A                                                              |
| `mapping`                                                        | Dict[str, *str*]                                                 | :heavy_minus_sign:                                               | N/A                                                              |
| `use_cache`                                                      | *Optional[bool]*                                                 | :heavy_minus_sign:                                               | N/A                                                              |