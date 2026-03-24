# WorkflowBasicDefinition


## Fields

| Field                                                              | Type                                                               | Required                                                           | Description                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `id`                                                               | *str*                                                              | :heavy_check_mark:                                                 | N/A                                                                |
| `name`                                                             | *str*                                                              | :heavy_check_mark:                                                 | The name of the workflow                                           |
| `display_name`                                                     | *str*                                                              | :heavy_check_mark:                                                 | The display name of the workflow                                   |
| `description`                                                      | *OptionalNullable[str]*                                            | :heavy_minus_sign:                                                 | A description of the workflow                                      |
| `metadata`                                                         | [Optional[models.WorkflowMetadata]](../models/workflowmetadata.md) | :heavy_minus_sign:                                                 | N/A                                                                |
| `archived`                                                         | *bool*                                                             | :heavy_check_mark:                                                 | Whether the workflow is archived                                   |