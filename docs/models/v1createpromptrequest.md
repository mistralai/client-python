# V1CreatePromptRequest


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `prompt`                                                                 | [Optional[models.V1Prompt]](../models/v1prompt.md)                       | :heavy_minus_sign:                                                       | User-editable template fields (create / update body).                    |
| `attributes`                                                             | [Optional[models.V1Attributes]](../models/v1attributes.md)               | :heavy_minus_sign:                                                       | N/A                                                                      |
| `version_attributes`                                                     | [Optional[models.V1VersionAttributes]](../models/v1versionattributes.md) | :heavy_minus_sign:                                                       | N/A                                                                      |
| `name`                                                                   | *Optional[str]*                                                          | :heavy_minus_sign:                                                       | Optional human-readable name, immutable after creation.                  |