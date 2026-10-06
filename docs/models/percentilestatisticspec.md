# PercentileStatisticSpec

The ``p``-th percentile (``0 <= p <= 100``), computed with the type-7 algorithm.


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `kind`                                                     | *Literal["percentile"]*                                    | :heavy_check_mark:                                         | N/A                                                        |
| `percentile`                                               | [models.Percentile](../models/percentile.md)               | :heavy_check_mark:                                         | N/A                                                        |
| `goal`                                                     | [OptionalNullable[models.GoalSpec]](../models/goalspec.md) | :heavy_minus_sign:                                         | N/A                                                        |