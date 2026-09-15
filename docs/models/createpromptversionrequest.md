# CreatePromptVersionRequest


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `definition`                                             | [models.PromptDefinition](../models/promptdefinition.md) | :heavy_check_mark:                                       | Versioned prompt content.                                |
| `notes`                                                  | *OptionalNullable[str]*                                  | :heavy_minus_sign:                                       | Notes for this version.                                  |
| `aliases`                                                | List[*str*]                                              | :heavy_minus_sign:                                       | Aliases pointing to this version.                        |