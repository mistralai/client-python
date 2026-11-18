# ScorerVersion


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `version`                                                            | *int*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `config`                                                             | [models.LlmJudgeConfig](../models/llmjudgeconfig.md)                 | :heavy_check_mark:                                                   | N/A                                                                  |
| `variables`                                                          | List[*str*]                                                          | :heavy_check_mark:                                                   | N/A                                                                  |
| `creator_id`                                                         | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `creator_type`                                                       | [Optional[models.PrincipalType]](../models/principaltype.md)         | :heavy_minus_sign:                                                   | N/A                                                                  |
| `created_at`                                                         | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_check_mark:                                                   | N/A                                                                  |