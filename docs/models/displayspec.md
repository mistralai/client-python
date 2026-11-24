# DisplaySpec

How the UI renders an evaluator's numeric values (scores, score-scale statistics, goal thresholds).

Display only: stored values and computed statistics never change. ``percent`` reads the value as a
fraction (0.63 renders as 63%), ``integer`` rounds it, ``number`` renders ``decimals`` decimals.
``unit`` is a free suffix ("s", "ms", "chars"), not allowed with ``percent`` (its ``%`` is the unit).
All fields unset = the default rendering.

``metric`` (run evaluators only) names the run evaluator metric this format applies to. Without it, the
spec formats the main value and is the default format of every metric.


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `format_`                                                            | [OptionalNullable[models.DisplayFormat]](../models/displayformat.md) | :heavy_minus_sign:                                                   | N/A                                                                  |
| `unit`                                                               | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `decimals`                                                           | *OptionalNullable[int]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |
| `metric`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |