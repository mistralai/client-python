# Audio.Sessions

## Overview

### Available Operations

* [create](#create) - Create an agent session
* [get](#get) - Get session status
* [close](#close) - Stop an agent session

## create

Create a real-time audio agent session.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_session_v1_audio_sessions_post" method="post" path="/v1/audio/sessions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.sessions.create()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                   | Type                                                                                        | Required                                                                                    | Description                                                                                 |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `llm`                                                                                       | [Optional[models.AudioLLMConfig]](../../models/audiollmconfig.md)                           | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `tts`                                                                                       | [Optional[models.AudioTTSConfig]](../../models/audiottsconfig.md)                           | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `stt`                                                                                       | [Optional[models.AudioSTTConfig]](../../models/audiosttconfig.md)                           | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `turn`                                                                                      | [Optional[models.AudioTurnConfig]](../../models/audioturnconfig.md)                         | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `instructions`                                                                              | *OptionalNullable[str]*                                                                     | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `tools`                                                                                     | List[[models.AudioSessionCreateRequestTool](../../models/audiosessioncreaterequesttool.md)] | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `welcome_message`                                                                           | *OptionalNullable[str]*                                                                     | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `agent_id`                                                                                  | *OptionalNullable[str]*                                                                     | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `agent_version`                                                                             | *OptionalNullable[int]*                                                                     | :heavy_minus_sign:                                                                          | N/A                                                                                         |
| `retries`                                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                            | :heavy_minus_sign:                                                                          | Configuration to override the default retry behavior of the client.                         |

### Response

**[models.AudioSessionCreateResponse](../../models/audiosessioncreateresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## get

Retrieve an audio agent session with the transcript of its conversation.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_session_v1_audio_sessions__session_id__get" method="get" path="/v1/audio/sessions/{session_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.sessions.get(session_id="4f4cc199-091a-4c84-bbe2-7e1c1dfeb849")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `session_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.AudioSessionResponse](../../models/audiosessionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |

## close

Stop an audio agent session and release its resources.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_session_v1_audio_sessions__session_id__delete" method="delete" path="/v1/audio/sessions/{session_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    mistral.audio.sessions.close(session_id="ce48313c-2e04-4918-9c23-e227a406a9e0")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `session_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |