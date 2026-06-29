# CreateSkillVersionRequest


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `definition`                                           | [models.SkillDefinition](../models/skilldefinition.md) | :heavy_check_mark:                                     | Versioned skill content.                               |
| `notes`                                                | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | Notes for this version.                                |
| `aliases`                                              | List[*str*]                                            | :heavy_minus_sign:                                     | Aliases pointing to this version.                      |