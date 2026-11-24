# ScoreMetric

One named number of a run evaluator score. Stored and sent as an ordered list (JSONB keeps no key order).


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `name`                                                   | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      |
| `value`                                                  | [models.ScoreMetricValue](../models/scoremetricvalue.md) | :heavy_check_mark:                                       | N/A                                                      |