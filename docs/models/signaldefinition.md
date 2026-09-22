# SignalDefinition


## Fields

| Field                                   | Type                                    | Required                                | Description                             |
| --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| `name`                                  | *str*                                   | :heavy_check_mark:                      | Name of the signal                      |
| `description`                           | *OptionalNullable[str]*                 | :heavy_minus_sign:                      | Description of the signal               |
| `input_schema`                          | Dict[str, *Any*]                        | :heavy_check_mark:                      | Input JSON schema of the signal's model |