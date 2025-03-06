# OCRPageObject


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `index`                                                              | *int*                                                                | :heavy_check_mark:                                                   | The page index in a pdf document starting from 0                     |
| `markdown`                                                           | *str*                                                                | :heavy_check_mark:                                                   | The markdown string response of the page                             |
| `images`                                                             | List[[models.OCRImageObject](../models/ocrimageobject.md)]           | :heavy_check_mark:                                                   | List of all extracted images in the page                             |
| `dimensions`                                                         | [Nullable[models.OCRPageDimensions]](../models/ocrpagedimensions.md) | :heavy_check_mark:                                                   | The dimensions of the PDF Page's screenshot image                    |