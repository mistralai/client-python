# DeepResearchTaskStep


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `id`                                                   | *Optional[str]*                                        | :heavy_minus_sign:                                     | N/A                                                    |
| `query`                                                | *str*                                                  | :heavy_check_mark:                                     | N/A                                                    |
| `status`                                               | [Optional[models.StepStatus]](../models/stepstatus.md) | :heavy_minus_sign:                                     | The status of a step.                                  |
| `findings`                                             | List[[models.Finding](../models/finding.md)]           | :heavy_minus_sign:                                     | N/A                                                    |
| `is_report`                                            | *Optional[bool]*                                       | :heavy_minus_sign:                                     | N/A                                                    |
| `is_fallback`                                          | *OptionalNullable[bool]*                               | :heavy_minus_sign:                                     | N/A                                                    |
| `is_skip`                                              | *OptionalNullable[bool]*                               | :heavy_minus_sign:                                     | N/A                                                    |