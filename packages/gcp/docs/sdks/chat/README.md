# Chat
(*chat*)

## Overview

Chat Completion API.

### Available Operations

* [stream](#stream) - Stream chat completion
* [complete](#complete) - Chat Completion

## stream

Mistral AI provides the ability to stream responses back to a client in order to allow partial results for certain requests. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

### Example Usage

```python
import os
from mistralai.gcp.client import MistralGCP

# The SDK auto-detects credentials and builds the Vertex AI URL
s = MistralGCP(
    project_id=os.environ.get("GCP_PROJECT_ID"),  # Optional: auto-detected from credentials
    region=os.environ.get("GCP_REGION", "us-central1"),
)

res = s.chat.stream(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model="mistral-small-2503")

if res is not None:
    for event in res:
        # handle event
        print(event)

```

### Parameters

| Parameter         | Type                                                              | Required           | Description                                                                                                                                                                                                                                                   | Example                                                                                                    |
| ----------------- | ----------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `messages`        | List[models.Messages]                 | :heavy_check_mark: | The prompt(s) to generate completions for, encoded as a list of dict with role and content.                                                                                                                                                                   | {<br/>"role": "user",<br/>"content": "Who is the best French painter? Answer in one short sentence."<br/>} |
| `model`           | *OptionalNullable[str]*                                           | :heavy_minus_sign: | ID of the model to use. You can use the [List Available Models](https://docs.mistral.ai/api#operation/listModels) API to see all of your available models, or see our [Model overview](https://docs.mistral.ai/models) for model descriptions.                                                              | mistral-small-latest                                                                                       |
| `temperature`     | *Optional[float]*                                                 | :heavy_minus_sign: | What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.        |                                                                                                            |
| `top_p`           | *Optional[float]*                                                 | :heavy_minus_sign: | Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both. |                                                                                                            |
| `max_tokens`      | *OptionalNullable[int]*                                           | :heavy_minus_sign: | The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.                                                                                                        |                                                                                                            |
| `min_tokens`      | *OptionalNullable[int]*                                           | :heavy_minus_sign: | The minimum number of tokens to generate in the completion.                                                                                                                                                                                                   |                                                                                                            |
| `stream`          | *Optional[bool]*                                                  | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                           |                                                                                                            |
| `stop`            | [Optional[models.Stop]](../../models/stop.md)                     | :heavy_minus_sign: | Stop generation if this token is detected. Or if one of these tokens is detected when providing an array                                                                                                                                                      |                                                                                                            |
| `random_seed`     | *OptionalNullable[int]*                                           | :heavy_minus_sign: | The seed to use for random sampling. If set, different calls will generate deterministic results.                                                                                                                                                             |                                                                                                            |
| `response_format` | [Optional[models.ResponseFormat]](../../models/responseformat.md) | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                           |                                                                                                            |
| `tools`           | List[[models.Tool](../../models/tool.md)]                         | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                           |                                                                                                            |
| `tool_choice`     | [Optional[models.ToolChoice]](../../models/toolchoice.md)         | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                           |                                                                                                            |
| `retries`         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)  | :heavy_minus_sign: | Configuration to override the default retry behavior of the client.                                                                                                                                                                                           |                                                                                                            |


### Response

**Union[Generator[models.CompletionEvent, None, None], AsyncGenerator[models.CompletionEvent, None]]**
### Errors

| Error Object    | Status Code | Content Type |
| --------------- | ----------- | ------------ |
| models.SDKError | 4xx-5xx     | */*          |

## complete

Chat Completion

### Example Usage

```python
import os
from mistralai.gcp.client import MistralGCP

# The SDK auto-detects credentials and builds the Vertex AI URL
s = MistralGCP(
    project_id=os.environ.get("GCP_PROJECT_ID"),  # Optional: auto-detected from credentials
    region=os.environ.get("GCP_REGION", "us-central1"),
)

res = s.chat.complete(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model="mistral-small-2503")

if res is not None:
    # handle response
    print(res.choices[0].message.content)

```

### Parameters

| Parameter         | Type                                                                                                | Required           | Description                                                                                                                                                                                                                                                                                                                        | Example                                                                                                    |
| ----------------- | --------------------------------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `messages`        | List[models.ChatCompletionRequestMessages]         | :heavy_check_mark: | The prompt(s) to generate completions for, encoded as a list of dict with role and content.                                                                                                                                                                                                                                        | {<br/>"role": "user",<br/>"content": "Who is the best French painter? Answer in one short sentence."<br/>} |
| `model`           | *OptionalNullable[str]*                                                                             | :heavy_minus_sign: | ID of the model to use. You can use the [List Available Models](https://docs.mistral.ai/api#operation/listModels) API to see all of your available models, or see our [Model overview](https://docs.mistral.ai/models) for model descriptions.                                                                                                                                   | mistral-small-latest                                                                                       |
| `temperature`     | *Optional[float]*                                                                                   | :heavy_minus_sign: | What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.                                                                             |                                                                                                            |
| `top_p`           | *Optional[float]*                                                                                   | :heavy_minus_sign: | Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.                                                                      |                                                                                                            |
| `max_tokens`      | *OptionalNullable[int]*                                                                             | :heavy_minus_sign: | The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.                                                                                                                                                                             |                                                                                                            |
| `min_tokens`      | *OptionalNullable[int]*                                                                             | :heavy_minus_sign: | The minimum number of tokens to generate in the completion.                                                                                                                                                                                                                                                                        |                                                                                                            |
| `stream`          | *Optional[bool]*                                                                                    | :heavy_minus_sign: | Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON. |                                                                                                            |
| `stop`            | [Optional[models.ChatCompletionRequestStop]](../../models/chatcompletionrequeststop.md)             | :heavy_minus_sign: | Stop generation if this token is detected. Or if one of these tokens is detected when providing an array                                                                                                                                                                                                                           |                                                                                                            |
| `random_seed`     | *OptionalNullable[int]*                                                                             | :heavy_minus_sign: | The seed to use for random sampling. If set, different calls will generate deterministic results.                                                                                                                                                                                                                                  |                                                                                                            |
| `response_format` | [Optional[models.ResponseFormat]](../../models/responseformat.md)                                   | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                                                                                                |                                                                                                            |
| `tools`           | List[[models.Tool](../../models/tool.md)]                                                           | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                                                                                                |                                                                                                            |
| `tool_choice`     | [Optional[models.ChatCompletionRequestToolChoice]](../../models/chatcompletionrequesttoolchoice.md) | :heavy_minus_sign: | N/A                                                                                                                                                                                                                                                                                                                                |                                                                                                            |
| `retries`         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign: | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                |                                                                                                            |


### Response

**[models.ChatCompletionResponse](../../models/chatcompletionresponse.md)**
### Errors

| Error Object               | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| models.HTTPValidationError | 422         | application/json |
| models.SDKError            | 4xx-5xx     | */*              |
