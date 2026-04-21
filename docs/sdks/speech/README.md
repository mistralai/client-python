# Audio.Speech

## Overview

### Available Operations

* [complete](#complete) - Speech

## complete

Speech

### Example Usage

<!-- UsageSnippet language="python" operationID="speech_v1_audio_speech_post" method="post" path="/v1/audio/speech" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                 | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `input`                                                                   | *str*                                                                     | :heavy_check_mark:                                                        | Text to generate a speech from                                            |
| `model`                                                                   | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | N/A                                                                       |
| `metadata`                                                                | Dict[str, *Any*]                                                          | :heavy_minus_sign:                                                        | N/A                                                                       |
| `stream`                                                                  | *Optional[bool]*                                                          | :heavy_minus_sign:                                                        | N/A                                                                       |
| `voice_id`                                                                | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | The preset or custom voice to use for generating the speech.              |
| `ref_audio`                                                               | *OptionalNullable[str]*                                                   | :heavy_minus_sign:                                                        | The audio reference for generating the speech.                            |
| `response_format`                                                         | [Optional[models.SpeechOutputFormat]](../../models/speechoutputformat.md) | :heavy_minus_sign:                                                        | N/A                                                                       |
| `additional_properties`                                                   | Dict[str, *Any*]                                                          | :heavy_minus_sign:                                                        | N/A                                                                       |
| `retries`                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)          | :heavy_minus_sign:                                                        | Configuration to override the default retry behavior of the client.       |

### Response

**[models.SpeechV1AudioSpeechPostResponse](../../models/speechv1audiospeechpostresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |