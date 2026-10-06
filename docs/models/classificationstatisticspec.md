# ClassificationStatisticSpec

A classification metric (``precision``/``recall``/``f1``) over ``(expected, predicted)`` pairs.

The predicted label is the score ``value``; the expected label is read from the score ``metadata``
under ``expected_key`` (default ``"expected"``). Provide **exactly one** of ``positive_label`` (a
binary metric scored against that one class) or ``average`` (a multi-class averaging scheme).

``labels`` pins the class universe so filtered views keep a stable, comparable denominator.


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `kind`                                                                                 | [models.ClassificationStatisticSpecKind](../models/classificationstatisticspeckind.md) | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `positive_label`                                                                       | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `average`                                                                              | [OptionalNullable[models.Average]](../models/average.md)                               | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `expected_key`                                                                         | *Optional[str]*                                                                        | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `labels`                                                                               | List[*str*]                                                                            | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `goal`                                                                                 | [OptionalNullable[models.GoalSpec]](../models/goalspec.md)                             | :heavy_minus_sign:                                                                     | N/A                                                                                    |