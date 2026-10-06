# ScoreSortInput


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `kind`                                                                 | *Literal["score"]*                                                     | :heavy_check_mark:                                                     | N/A                                                                    |
| `evaluator_name`                                                       | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `metric`                                                               | [Optional[models.NumericScoreMetric]](../models/numericscoremetric.md) | :heavy_minus_sign:                                                     | N/A                                                                    |
| `direction`                                                            | [Optional[models.SortDirection]](../models/sortdirection.md)           | :heavy_minus_sign:                                                     | N/A                                                                    |