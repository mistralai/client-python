# DocumentLibraryTool


## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `tool_configuration`                                                             | [OptionalNullable[models.ToolConfiguration]](../models/toolconfiguration.md)     | :heavy_minus_sign:                                                               | N/A                                                                              |
| `type`                                                                           | [Optional[models.DocumentLibraryToolType]](../models/documentlibrarytooltype.md) | :heavy_minus_sign:                                                               | N/A                                                                              |
| `library_ids`                                                                    | List[*str*]                                                                      | :heavy_check_mark:                                                               | Ids of the library in which to search.                                           |