# ScalarStatisticValue

A single scalar computed run-level statistic: its canonical id and numeric value.

``value`` is ``None`` when the statistic is not evaluable (e.g. a ``sum`` or percentile over an
empty numeric sample). A declared ``count`` is always evaluable and is ``0`` on an empty sample.

The ``type`` discriminator lets future result shapes (e.g. a categorical ``categories`` or a
``distribution``) join a union without overloading this model; consumers dispatch on ``type``.


## Fields

| Field                         | Type                          | Required                      | Description                   |
| ----------------------------- | ----------------------------- | ----------------------------- | ----------------------------- |
| `type`                        | *Optional[Literal["scalar"]]* | :heavy_minus_sign:            | N/A                           |
| `id`                          | *str*                         | :heavy_check_mark:            | N/A                           |
| `value`                       | *OptionalNullable[float]*     | :heavy_minus_sign:            | N/A                           |