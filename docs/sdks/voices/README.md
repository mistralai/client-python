# Audio.Voices

## Overview

### Available Operations

* [list](#list) - List all voices
* [create](#create) - Create a new voice
* [delete](#delete) - Delete a custom voice
* [update](#update) - Update voice metadata
* [get](#get) - Get voice details
* [get_sample_audio](#get_sample_audio) - Get voice sample audio

## list

List all voices (excluding sample data)

### Example Usage

<!-- UsageSnippet language="python" operationID="list_voices_v1_audio_voices_get" method="get" path="/v1/audio/voices" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.list(limit=10, offset=0, type_="all")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                         | Type                                                                                              | Required                                                                                          | Description                                                                                       |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `limit`                                                                                           | *Optional[int]*                                                                                   | :heavy_minus_sign:                                                                                | Maximum number of voices to return                                                                |
| `offset`                                                                                          | *Optional[int]*                                                                                   | :heavy_minus_sign:                                                                                | Offset for pagination                                                                             |
| `type`                                                                                            | [Optional[models.ListVoicesV1AudioVoicesGetType]](../../models/listvoicesv1audiovoicesgettype.md) | :heavy_minus_sign:                                                                                | Filter the voices between customs and presets                                                     |
| `retries`                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                  | :heavy_minus_sign:                                                                                | Configuration to override the default retry behavior of the client.                               |

### Response

**[models.VoiceListResponse](../../models/voicelistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## create

Create a new voice with a base64-encoded audio sample

### Example Usage

<!-- UsageSnippet language="python" operationID="create_voice_v1_audio_voices_post" method="post" path="/v1/audio/voices" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.create(name="<value>", sample_audio="<value>", retention_notice=30)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `sample_audio`                                                      | *str*                                                               | :heavy_check_mark:                                                  | Base64-encoded audio file                                           |
| `slug`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `languages`                                                         | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `gender`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `age`                                                               | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `tags`                                                              | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `color`                                                             | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retention_notice`                                                  | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `sample_filename`                                                   | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | Original filename for extension detection                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.VoiceResponse](../../models/voiceresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## delete

Delete a custom voice

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_voice_v1_audio_voices__voice_id__delete" method="delete" path="/v1/audio/voices/{voice_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.delete(voice_id="f42bf0d7-8a10-4b98-bbfa-589a232209d2")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.VoiceResponse](../../models/voiceresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## update

Update voice metadata (name, gender, languages, age, tags).

### Example Usage

<!-- UsageSnippet language="python" operationID="update_voice_v1_audio_voices__voice_id__patch" method="patch" path="/v1/audio/voices/{voice_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.update(voice_id="030a6b20-e287-414d-9a77-6b76a4a56c9d")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `name`                                                              | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `languages`                                                         | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `gender`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `age`                                                               | *OptionalNullable[int]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `tags`                                                              | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.VoiceResponse](../../models/voiceresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Get voice details (excluding sample)

### Example Usage

<!-- UsageSnippet language="python" operationID="get_voice_v1_audio_voices__voice_id__get" method="get" path="/v1/audio/voices/{voice_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.get(voice_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.VoiceResponse](../../models/voiceresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get_sample_audio

Get the audio sample for a voice

### Example Usage

<!-- UsageSnippet language="python" operationID="get_voice_sample_audio_v1_audio_voices__voice_id__sample_get" method="get" path="/v1/audio/voices/{voice_id}/sample" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.voices.get_sample_audio(voice_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[str](../../models/responsegetvoicesampleaudiov1audiovoicesvoiceidsampleget.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |