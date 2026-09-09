# OtelFieldDefinition


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `name`                                                                 | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `label`                                                                | *str*                                                                  | :heavy_check_mark:                                                     | N/A                                                                    |
| `type`                                                                 | [models.OtelFieldDefinitionType](../models/otelfielddefinitiontype.md) | :heavy_check_mark:                                                     | N/A                                                                    |
| `group`                                                                | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | N/A                                                                    |
| `supported_operators`                                                  | List[[models.SupportedOperator](../models/supportedoperator.md)]       | :heavy_check_mark:                                                     | N/A                                                                    |
| `supported_aggregations`                                               | List[[models.MetricAggregation](../models/metricaggregation.md)]       | :heavy_check_mark:                                                     | N/A                                                                    |