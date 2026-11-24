# MissingGoalItem

A run evaluator goal on a metric the scorer did not return: it fails, with no number to show.

Kept out of ``results`` so ``GoalResultItem.actual`` stays a number for clients that require one.


## Fields

| Field                     | Type                      | Required                  | Description               |
| ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| `metric`                  | *str*                     | :heavy_check_mark:        | N/A                       |
| `operator`                | *str*                     | :heavy_check_mark:        | N/A                       |
| `target`                  | *OptionalNullable[float]* | :heavy_minus_sign:        | N/A                       |
| `target_min`              | *OptionalNullable[float]* | :heavy_minus_sign:        | N/A                       |
| `target_max`              | *OptionalNullable[float]* | :heavy_minus_sign:        | N/A                       |
| `message`                 | *str*                     | :heavy_check_mark:        | N/A                       |