# FilesAPIRoutesListFilesRequest


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `page`                                                           | *Optional[int]*                                                  | :heavy_minus_sign:                                               | N/A                                                              |
| `page_size`                                                      | *Optional[int]*                                                  | :heavy_minus_sign:                                               | N/A                                                              |
| `include_total`                                                  | *Optional[bool]*                                                 | :heavy_minus_sign:                                               | N/A                                                              |
| `sample_type`                                                    | List[[models.SampleType](../models/sampletype.md)]               | :heavy_minus_sign:                                               | N/A                                                              |
| `source`                                                         | List[[models.Source](../models/source.md)]                       | :heavy_minus_sign:                                               | N/A                                                              |
| `search`                                                         | *OptionalNullable[str]*                                          | :heavy_minus_sign:                                               | N/A                                                              |
| `purpose`                                                        | [OptionalNullable[models.FilePurpose]](../models/filepurpose.md) | :heavy_minus_sign:                                               | N/A                                                              |
| `mimetypes`                                                      | List[*str*]                                                      | :heavy_minus_sign:                                               | N/A                                                              |