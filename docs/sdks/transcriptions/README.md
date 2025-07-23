# Transcriptions
(*audio.transcriptions*)

## Overview

API for audio transcription.

### Available Operations

* [complete](#complete) - Create Transcription
* [stream](#stream) - Create streaming transcription (SSE)

## complete

Create Transcription

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.transcriptions.complete(model="Model X")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                    | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `model`                                                                      | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          |
| `file`                                                                       | [Optional[models.File]](../../models/file.md)                                | :heavy_minus_sign:                                                           | N/A                                                                          |
| `file_url`                                                                   | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Url of a file to be transcribed                                              |
| `file_id`                                                                    | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | ID of a file uploaded to /v1/files                                           |
| `language`                                                                   | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Language of the audio, e.g. 'en'. Providing the language can boost accuracy. |
| `temperature`                                                                | *OptionalNullable[float]*                                                    | :heavy_minus_sign:                                                           | N/A                                                                          |
| `timestamp_granularities`                                                    | List[[models.TimestampGranularity](../../models/timestampgranularity.md)]    | :heavy_minus_sign:                                                           | Granularities of timestamps to include in the response.                      |
| `retries`                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)             | :heavy_minus_sign:                                                           | Configuration to override the default retry behavior of the client.          |

### Response

**[models.TranscriptionResponse](../../models/transcriptionresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |

## stream

Create streaming transcription (SSE)

### Example Usage

```python
from mistralai import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.transcriptions.stream(model="Camry")

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                    | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `model`                                                                      | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          |
| `file`                                                                       | [Optional[models.File]](../../models/file.md)                                | :heavy_minus_sign:                                                           | N/A                                                                          |
| `file_url`                                                                   | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Url of a file to be transcribed                                              |
| `file_id`                                                                    | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | ID of a file uploaded to /v1/files                                           |
| `language`                                                                   | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | Language of the audio, e.g. 'en'. Providing the language can boost accuracy. |
| `temperature`                                                                | *OptionalNullable[float]*                                                    | :heavy_minus_sign:                                                           | N/A                                                                          |
| `timestamp_granularities`                                                    | List[[models.TimestampGranularity](../../models/timestampgranularity.md)]    | :heavy_minus_sign:                                                           | Granularities of timestamps to include in the response.                      |
| `retries`                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)             | :heavy_minus_sign:                                                           | Configuration to override the default retry behavior of the client.          |

### Response

**[Union[eventstreaming.EventStream[models.TranscriptionStreamEvents], eventstreaming.EventStreamAsync[models.TranscriptionStreamEvents]]](../../models/.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| models.SDKError | 4XX, 5XX        | \*/\*           |