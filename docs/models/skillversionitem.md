# SkillVersionItem


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `version`                                                            | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `skill`                                                              | [Optional[models.SkillContent]](../models/skillcontent.md)           | :heavy_minus_sign:                                                   | Per-version content package surfaced to the model.                   |
| `version_attributes`                                                 | [Optional[models.VersionAttributes]](../models/versionattributes.md) | :heavy_minus_sign:                                                   | User-provided, per-version fields                                    |
| `version_metadata`                                                   | [Optional[models.VersionMetadata]](../models/versionmetadata.md)     | :heavy_minus_sign:                                                   | System-provided, per-version fields                                  |