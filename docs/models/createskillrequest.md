# CreateSkillRequest


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `skill`                                                                    | [Optional[models.SkillContent]](../models/skillcontent.md)                 | :heavy_minus_sign:                                                         | Per-version content package surfaced to the model.                         |
| `attributes`                                                               | [Optional[models.Attributes]](../models/attributes.md)                     | :heavy_minus_sign:                                                         | N/A                                                                        |
| `version_attributes`                                                       | [Optional[models.VersionAttributes]](../models/versionattributes.md)       | :heavy_minus_sign:                                                         | User-provided, per-version fields                                          |
| `name`                                                                     | *Optional[str]*                                                            | :heavy_minus_sign:                                                         | Optional human-readable name (immutable after creation, workspace-unique). |