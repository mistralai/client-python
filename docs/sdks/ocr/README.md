# Ocr
(*ocr*)

## Overview

OCR API

### Available Operations

* [process](#process) - OCR

## process

OCR

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.ocr.process(model="Focus", document={
        "document_url": "https://dutiful-horst.org",
        "type": "document_url",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                     | Type                                                                                                          | Required                                                                                                      | Description                                                                                                   |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `model`                                                                                                       | *Nullable[str]*                                                                                               | :heavy_check_mark:                                                                                            | N/A                                                                                                           |
| `document`                                                                                                    | [models.Document](../../models/document.md)                                                                   | :heavy_check_mark:                                                                                            | Document to run OCR on                                                                                        |
| `id`                                                                                                          | *Optional[str]*                                                                                               | :heavy_minus_sign:                                                                                            | N/A                                                                                                           |
| `pages`                                                                                                       | List[*int*]                                                                                                   | :heavy_minus_sign:                                                                                            | Specific pages user wants to process in various formats: single number, range, or list of both. Starts from 0 |
| `include_image_base64`                                                                                        | *OptionalNullable[bool]*                                                                                      | :heavy_minus_sign:                                                                                            | Include image URLs in response                                                                                |
| `image_limit`                                                                                                 | *OptionalNullable[int]*                                                                                       | :heavy_minus_sign:                                                                                            | Max images to extract                                                                                         |
| `image_min_size`                                                                                              | *OptionalNullable[int]*                                                                                       | :heavy_minus_sign:                                                                                            | Minimum height and width of image to extract                                                                  |
| `retries`                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                              | :heavy_minus_sign:                                                                                            | Configuration to override the default retry behavior of the client.                                           |

### Response

**[models.OCRResponse](../../models/ocrresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |