# AggregationRow


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `time_bucket`                                                        | [date](https://docs.python.org/3/library/datetime.html#date-objects) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `dimensions`                                                         | Dict[str, *Any*]                                                     | :heavy_minus_sign:                                                   | N/A                                                                  |
| `metric_name`                                                        | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `metric_value`                                                       | [OptionalNullable[models.MetricValue]](../models/metricvalue.md)     | :heavy_minus_sign:                                                   | N/A                                                                  |