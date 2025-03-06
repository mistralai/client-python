# OCRResponse


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `pages`                                                  | List[[models.OCRPageObject](../models/ocrpageobject.md)] | :heavy_check_mark:                                       | List of OCR info for pages.                              |
| `model`                                                  | *str*                                                    | :heavy_check_mark:                                       | The model used to generate the OCR.                      |
| `usage_info`                                             | [models.OCRUsageInfo](../models/ocrusageinfo.md)         | :heavy_check_mark:                                       | N/A                                                      |