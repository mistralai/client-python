# CreatePromptRequest


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `prompt`                                                             | [Optional[models.PromptContent]](../models/promptcontent.md)         | :heavy_minus_sign:                                                   | User-editable template fields (create / update body).                |
| `attributes`                                                         | [Optional[models.Attributes]](../models/attributes.md)               | :heavy_minus_sign:                                                   | N/A                                                                  |
| `version_attributes`                                                 | [Optional[models.VersionAttributes]](../models/versionattributes.md) | :heavy_minus_sign:                                                   | User-provided, per-version fields                                    |
| `name`                                                               | *Optional[str]*                                                      | :heavy_minus_sign:                                                   | Optional human-readable name, immutable after creation.              |