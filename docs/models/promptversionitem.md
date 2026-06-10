# PromptVersionItem


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `version`                                                            | *Optional[int]*                                                      | :heavy_minus_sign:                                                   | N/A                                                                  |
| `prompt`                                                             | [Optional[models.PromptContent]](../models/promptcontent.md)         | :heavy_minus_sign:                                                   | User-editable template fields (create / update body).                |
| `version_attributes`                                                 | [Optional[models.VersionAttributes]](../models/versionattributes.md) | :heavy_minus_sign:                                                   | User-provided, per-version fields                                    |
| `version_metadata`                                                   | [Optional[models.VersionMetadata]](../models/versionmetadata.md)     | :heavy_minus_sign:                                                   | System-provided, per-version fields                                  |