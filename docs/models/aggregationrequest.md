# AggregationRequest


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `metric`                                                             | [models.MetricDefinition](../models/metricdefinition.md)             | :heavy_check_mark:                                                   | N/A                                                                  |
| `dimensions`                                                         | List[*str*]                                                          | :heavy_minus_sign:                                                   | N/A                                                                  |
| `time_dimension`                                                     | [OptionalNullable[models.TimeDimension]](../models/timedimension.md) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `search_expression`                                                  | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `order_by`                                                           | List[[models.OrderByClause](../models/orderbyclause.md)]             | :heavy_minus_sign:                                                   | N/A                                                                  |
| `limit`                                                              | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |