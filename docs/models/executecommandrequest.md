# ExecuteCommandRequest

Request to execute a command in a sandbox.


## Fields

| Field                                 | Type                                  | Required                              | Description                           |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |
| `command`                             | *str*                                 | :heavy_check_mark:                    | Command to execute                    |
| `timeout`                             | *OptionalNullable[int]*               | :heavy_minus_sign:                    | Optional timeout in seconds (integer) |