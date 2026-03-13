# APIResponseExecutionData


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `success`                                                            | *bool*                                                               | :heavy_check_mark:                                                   | Whether the request was successful                                   |
| `data`                                                               | [OptionalNullable[models.ExecutionData]](../models/executiondata.md) | :heavy_minus_sign:                                                   | Response data                                                        |
| `error`                                                              | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | Error message if failed                                              |