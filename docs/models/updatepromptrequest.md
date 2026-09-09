# UpdatePromptRequest


## Fields

| Field                                                                      | Type                                                                       | Required                                                                   | Description                                                                |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `title`                                                                    | *OptionalNullable[str]*                                                    | :heavy_minus_sign:                                                         | Display title.                                                             |
| `description`                                                              | *OptionalNullable[str]*                                                    | :heavy_minus_sign:                                                         | Display description.                                                       |
| `sharing_scope`                                                            | [Optional[models.RegistrySharingScope]](../models/registrysharingscope.md) | :heavy_minus_sign:                                                         | N/A                                                                        |
| `workspace_relation`                                                       | [Optional[models.ShareRelation]](../models/sharerelation.md)               | :heavy_minus_sign:                                                         | Relation a subject holds on a shared registry object.                      |