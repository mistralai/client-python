# V1CreateSkillRequest


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `skill`                                                                    | [Optional[models.V1Skill]](../models/v1skill.md)                           | :heavy_minus_sign:                                                         | Per-version content package surfaced to the model.                         |
| `attributes`                                                               | [Optional[models.V1Attributes]](../models/v1attributes.md)                 | :heavy_minus_sign:                                                         | N/A                                                                        |
| `version_attributes`                                                       | [Optional[models.V1VersionAttributes]](../models/v1versionattributes.md)   | :heavy_minus_sign:                                                         | N/A                                                                        |
| `name`                                                                     | *Optional[str]*                                                            | :heavy_minus_sign:                                                         | Optional human-readable name (immutable after creation, workspace-unique). |