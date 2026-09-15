# UpdateDefinition


## Fields

| Field                                    | Type                                     | Required                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| `name`                                   | *str*                                    | :heavy_check_mark:                       | Name of the update                       |
| `description`                            | *OptionalNullable[str]*                  | :heavy_minus_sign:                       | Description of the update                |
| `input_schema`                           | Dict[str, *Any*]                         | :heavy_check_mark:                       | Input JSON schema of the update's model  |
| `output_schema`                          | Dict[str, *Any*]                         | :heavy_minus_sign:                       | Output JSON schema of the update's model |