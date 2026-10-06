# RunStatisticsResponse


## Fields

| Field                                                                     | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `run_id`                                                                  | *str*                                                                     | :heavy_check_mark:                                                        | N/A                                                                       |
| `statistics`                                                              | Dict[str, [models.EvaluatorStatistics](../models/evaluatorstatistics.md)] | :heavy_check_mark:                                                        | N/A                                                                       |
| `goal_results`                                                            | Dict[str, [models.GoalResult](../models/goalresult.md)]                   | :heavy_minus_sign:                                                        | N/A                                                                       |
| `passed`                                                                  | *OptionalNullable[bool]*                                                  | :heavy_minus_sign:                                                        | N/A                                                                       |