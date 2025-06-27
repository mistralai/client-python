# OCRResponse


## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `pages`                                                          | List[[models.OCRPageObject](../models/ocrpageobject.md)]         | :heavy_check_mark:                                               | List of OCR info for pages.                                      |
| `model`                                                          | *str*                                                            | :heavy_check_mark:                                               | The model used to generate the OCR.                              |
| `document_annotation`                                            | *OptionalNullable[str]*                                          | :heavy_minus_sign:                                               | Formatted response in the request_format if provided in json str |
| `usage_info`                                                     | [models.OCRUsageInfo](../models/ocrusageinfo.md)                 | :heavy_check_mark:                                               | N/A                                                              |