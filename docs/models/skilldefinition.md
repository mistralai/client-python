# SkillDefinition

Versioned skill content.


## Fields

| Field                                                                 | Type                                                                  | Required                                                              | Description                                                           |
| --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `description`                                                         | *Optional[str]*                                                       | :heavy_minus_sign:                                                    | Model-facing trigger and usage description.                           |
| `body`                                                                | *str*                                                                 | :heavy_check_mark:                                                    | Skill body content.                                                   |
| `assets`                                                              | Dict[str, [models.SkillAssetContent](../models/skillassetcontent.md)] | :heavy_minus_sign:                                                    | Additional files available to the skill.                              |