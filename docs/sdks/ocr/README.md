# Ocr

## Overview

OCR API

### Available Operations

* [process](#process) - OCR

## process

OCR

### Example Usage

<!-- UsageSnippet language="python" operationID="ocr_v1_ocr_post" method="post" path="/v1/ocr" -->
```python
from mistralai.sdk import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.ocr.process(model="CX-9", document={
        "image_url": {
            "url": "https://measly-scrap.com",
        },
        "type": "image_url",
    }, bbox_annotation_format={
        "type": "text",
    }, document_annotation_format={
        "type": "text",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                  | Type                                                                                                                                                       | Required                                                                                                                                                   | Description                                                                                                                                                | Example                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                                                                                                                                                    | *Nullable[str]*                                                                                                                                            | :heavy_check_mark:                                                                                                                                         | N/A                                                                                                                                                        |                                                                                                                                                            |
| `document`                                                                                                                                                 | [models.Document](../../models/document.md)                                                                                                                | :heavy_check_mark:                                                                                                                                         | Document to run OCR on                                                                                                                                     |                                                                                                                                                            |
| `id`                                                                                                                                                       | *Optional[str]*                                                                                                                                            | :heavy_minus_sign:                                                                                                                                         | N/A                                                                                                                                                        |                                                                                                                                                            |
| `pages`                                                                                                                                                    | List[*int*]                                                                                                                                                | :heavy_minus_sign:                                                                                                                                         | Specific pages user wants to process in various formats: single number, range, or list of both. Starts from 0                                              |                                                                                                                                                            |
| `include_image_base64`                                                                                                                                     | *OptionalNullable[bool]*                                                                                                                                   | :heavy_minus_sign:                                                                                                                                         | Include image URLs in response                                                                                                                             |                                                                                                                                                            |
| `image_limit`                                                                                                                                              | *OptionalNullable[int]*                                                                                                                                    | :heavy_minus_sign:                                                                                                                                         | Max images to extract                                                                                                                                      |                                                                                                                                                            |
| `image_min_size`                                                                                                                                           | *OptionalNullable[int]*                                                                                                                                    | :heavy_minus_sign:                                                                                                                                         | Minimum height and width of image to extract                                                                                                               |                                                                                                                                                            |
| `bbox_annotation_format`                                                                                                                                   | [OptionalNullable[models.ResponseFormat]](../../models/responseformat.md)                                                                                  | :heavy_minus_sign:                                                                                                                                         | Structured output class for extracting useful information from each extracted bounding box / image from document. Only json_schema is valid for this field | {<br/>"type": "text"<br/>}                                                                                                                                 |
| `document_annotation_format`                                                                                                                               | [OptionalNullable[models.ResponseFormat]](../../models/responseformat.md)                                                                                  | :heavy_minus_sign:                                                                                                                                         | Structured output class for extracting useful information from the entire document. Only json_schema is valid for this field                               | {<br/>"type": "text"<br/>}                                                                                                                                 |
| `table_format`                                                                                                                                             | [OptionalNullable[models.TableFormat]](../../models/tableformat.md)                                                                                        | :heavy_minus_sign:                                                                                                                                         | N/A                                                                                                                                                        |                                                                                                                                                            |
| `extract_header`                                                                                                                                           | *Optional[bool]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                         | N/A                                                                                                                                                        |                                                                                                                                                            |
| `extract_footer`                                                                                                                                           | *Optional[bool]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                         | N/A                                                                                                                                                        |                                                                                                                                                            |
| `retries`                                                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                           | :heavy_minus_sign:                                                                                                                                         | Configuration to override the default retry behavior of the client.                                                                                        |                                                                                                                                                            |

### Response

**[models.OCRResponse](../../models/ocrresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |