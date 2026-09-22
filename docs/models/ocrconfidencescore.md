# OCRConfidenceScore

Confidence score for a token or word in OCR output.


## Fields

| Field                                               | Type                                                | Required                                            | Description                                         |
| --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| `text`                                              | *str*                                               | :heavy_check_mark:                                  | The word or text segment                            |
| `confidence`                                        | *float*                                             | :heavy_check_mark:                                  | Confidence score (0-1)                              |
| `start_index`                                       | *int*                                               | :heavy_check_mark:                                  | Start index of the text in the page markdown string |