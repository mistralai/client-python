# APIResponseSandboxData


## Fields

| Field                                          | Type                                           | Required                                       | Description                                    |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------- |
| `success`                                      | *bool*                                         | :heavy_check_mark:                             | Whether the request was successful             |
| `data`                                         | [models.SandboxData](../models/sandboxdata.md) | :heavy_check_mark:                             | Sandbox data for API responses.                |
| `error`                                        | *OptionalNullable[str]*                        | :heavy_minus_sign:                             | Error message if failed                        |