# APIResponseSandboxListData


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `success`                                                                | *bool*                                                                   | :heavy_check_mark:                                                       | Whether the request was successful                                       |
| `data`                                                                   | [OptionalNullable[models.SandboxListData]](../models/sandboxlistdata.md) | :heavy_minus_sign:                                                       | Response data                                                            |
| `error`                                                                  | *OptionalNullable[str]*                                                  | :heavy_minus_sign:                                                       | Error message if failed                                                  |