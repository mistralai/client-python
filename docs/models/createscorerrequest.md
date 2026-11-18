# CreateScorerRequest


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `name`                                               | *str*                                                | :heavy_check_mark:                                   | N/A                                                  |
| `description`                                        | *OptionalNullable[str]*                              | :heavy_minus_sign:                                   | N/A                                                  |
| `kind`                                               | [models.ScorerKind](../models/scorerkind.md)         | :heavy_check_mark:                                   | N/A                                                  |
| `config`                                             | [models.LlmJudgeConfig](../models/llmjudgeconfig.md) | :heavy_check_mark:                                   | N/A                                                  |