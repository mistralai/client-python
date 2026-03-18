# QueryDefinition


## Fields

| Field                                   | Type                                    | Required                                | Description                             |
| --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| `name`                                  | *str*                                   | :heavy_check_mark:                      | Name of the query                       |
| `description`                           | *OptionalNullable[str]*                 | :heavy_minus_sign:                      | Description of the query                |
| `input_schema`                          | Dict[str, *Any*]                        | :heavy_check_mark:                      | Input JSON schema of the query's model  |
| `output_schema`                         | Dict[str, *Any*]                        | :heavy_minus_sign:                      | Output JSON schema of the query's model |