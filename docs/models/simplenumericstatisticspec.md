# SimpleNumericStatisticSpec

A scalar numeric reduction (``avg``/``sum``/``min``/``max``/``std``/``count``).

``weight_key`` (``avg`` only) turns the mean into a weighted mean, ``sum(w * x) / sum(w)``, where
each score's weight ``w`` is read from its ``metadata`` under that key. Scores whose weight is
missing, non-numeric or negative are left out of that statistic.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `kind`                                                                               | [models.SimpleNumericStatisticSpecKind](../models/simplenumericstatisticspeckind.md) | :heavy_check_mark:                                                                   | N/A                                                                                  |
| `weight_key`                                                                         | *OptionalNullable[str]*                                                              | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `goal`                                                                               | [OptionalNullable[models.GoalSpec]](../models/goalspec.md)                           | :heavy_minus_sign:                                                                   | N/A                                                                                  |