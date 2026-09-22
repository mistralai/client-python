# WorkflowMetrics

Complete metrics for a specific workflow.

This type combines all metric categories.


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `execution_count`                                        | [models.ScalarMetric](../models/scalarmetric.md)         | :heavy_check_mark:                                       | Scalar metric with a single value.                       |
| `success_count`                                          | [models.ScalarMetric](../models/scalarmetric.md)         | :heavy_check_mark:                                       | Scalar metric with a single value.                       |
| `error_count`                                            | [models.ScalarMetric](../models/scalarmetric.md)         | :heavy_check_mark:                                       | Scalar metric with a single value.                       |
| `average_latency_ms`                                     | [models.ScalarMetric](../models/scalarmetric.md)         | :heavy_check_mark:                                       | Scalar metric with a single value.                       |
| `latency_over_time`                                      | [models.TimeSeriesMetric](../models/timeseriesmetric.md) | :heavy_check_mark:                                       | Time-series metric with timestamp-value pairs.           |
| `retry_rate`                                             | [models.ScalarMetric](../models/scalarmetric.md)         | :heavy_check_mark:                                       | Scalar metric with a single value.                       |