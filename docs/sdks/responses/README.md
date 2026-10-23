# Responses

## Overview

Stateless Responses API for text, images, reasoning, function calls, and streaming.

### Available Operations

* [create](#create) - Create Response
* [count_input_tokens](#count_input_tokens) - Count Input Tokens

## create

Create a response.

Generate a model response from text or image inputs. The response can
include text, reasoning, and function calls. Set stream to true to
receive Server-Sent Events.

For multi-turn conversations, send the full history in input, including
prior output items and function results. Responses are not stored. Only
client-executed function tools are supported.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_response_v1_responses_post" method="post" path="/v1/responses" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.responses.create(model="V90", input=[], parallel_tool_calls=True, stream=False, additional_properties={
        "truncation": "disabled",
        "background": False,
        "store": False,
        "top_logprobs": 0,
    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Parameters

| Parameter                                                                                                                                     | Type                                                                                                                                          | Required                                                                                                                                      | Description                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                                                                                                                                       | *str*                                                                                                                                         | :heavy_check_mark:                                                                                                                            | N/A                                                                                                                                           |
| `input`                                                                                                                                       | [models.CreateResponseRequestInput2](../../models/createresponserequestinput2.md)                                                             | :heavy_check_mark:                                                                                                                            | N/A                                                                                                                                           |
| `instructions`                                                                                                                                | *OptionalNullable[str]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `parallel_tool_calls`                                                                                                                         | *Optional[bool]*                                                                                                                              | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `previous_response_id`                                                                                                                        | *OptionalNullable[Any]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `tools`                                                                                                                                       | List[[models.CreateResponseRequestTool](../../models/createresponserequesttool.md)]                                                           | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `tool_choice`                                                                                                                                 | [Optional[models.CreateResponseRequestToolChoiceUnion]](../../models/createresponserequesttoolchoiceunion.md)                                 | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `reasoning`                                                                                                                                   | [OptionalNullable[models.CreateResponseRequestResponsesSupportedReasoning]](../../models/createresponserequestresponsessupportedreasoning.md) | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `conversation`                                                                                                                                | *OptionalNullable[Any]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `prompt`                                                                                                                                      | *OptionalNullable[Any]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `text`                                                                                                                                        | [OptionalNullable[models.CreateResponseRequestResponsesTextConfig]](../../models/createresponserequestresponsestextconfig.md)                 | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `stream`                                                                                                                                      | *Optional[bool]*                                                                                                                              | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `max_output_tokens`                                                                                                                           | *OptionalNullable[int]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `temperature`                                                                                                                                 | *OptionalNullable[float]*                                                                                                                     | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `top_p`                                                                                                                                       | *OptionalNullable[float]*                                                                                                                     | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `metadata`                                                                                                                                    | Dict[str, *str*]                                                                                                                              | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `prompt_cache_key`                                                                                                                            | *OptionalNullable[str]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `max_tool_calls`                                                                                                                              | *OptionalNullable[int]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `moderation`                                                                                                                                  | *OptionalNullable[Any]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `additional_properties`                                                                                                                       | Dict[str, *Any*]                                                                                                                              | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |
| `retries`                                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                              | :heavy_minus_sign:                                                                                                                            | Configuration to override the default retry behavior of the client.                                                                           |

### Response

**[models.CreateResponseV1ResponsesPostResponse](../../models/createresponsev1responsespostresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |

## count_input_tokens

Count response input tokens.

Count the input tokens for a Responses request without generating a
response. The count includes the supplied conversation, instructions,
and tool definitions.

Use the same input, instructions, and tools that you plan to send when
creating a response. For multi-turn conversations, include prior output
items and function results in input.

### Example Usage

<!-- UsageSnippet language="python" operationID="count_input_tokens_v1_responses_input_tokens_post" method="post" path="/v1/responses/input_tokens" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.responses.count_input_tokens(model="Corvette", input="<value>", parallel_tool_calls=True, additional_properties={
        "truncation": "disabled",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                         | Type                                                                                                                                                              | Required                                                                                                                                                          | Description                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`                                                                                                                                                           | *str*                                                                                                                                                             | :heavy_check_mark:                                                                                                                                                | N/A                                                                                                                                                               |
| `input`                                                                                                                                                           | [models.CountResponseInputTokensRequestInput2](../../models/countresponseinputtokensrequestinput2.md)                                                             | :heavy_check_mark:                                                                                                                                                | N/A                                                                                                                                                               |
| `instructions`                                                                                                                                                    | *OptionalNullable[str]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `parallel_tool_calls`                                                                                                                                             | *Optional[bool]*                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `previous_response_id`                                                                                                                                            | *OptionalNullable[Any]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `tools`                                                                                                                                                           | List[[models.CountResponseInputTokensRequestTool](../../models/countresponseinputtokensrequesttool.md)]                                                           | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `tool_choice`                                                                                                                                                     | [Optional[models.CountResponseInputTokensRequestToolChoiceUnion]](../../models/countresponseinputtokensrequesttoolchoiceunion.md)                                 | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `reasoning`                                                                                                                                                       | [OptionalNullable[models.CountResponseInputTokensRequestResponsesSupportedReasoning]](../../models/countresponseinputtokensrequestresponsessupportedreasoning.md) | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `conversation`                                                                                                                                                    | *OptionalNullable[Any]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `prompt`                                                                                                                                                          | *OptionalNullable[Any]*                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `text`                                                                                                                                                            | [OptionalNullable[models.CountResponseInputTokensRequestResponsesTextConfig]](../../models/countresponseinputtokensrequestresponsestextconfig.md)                 | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `additional_properties`                                                                                                                                           | Dict[str, *Any*]                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                | N/A                                                                                                                                                               |
| `retries`                                                                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                  | :heavy_minus_sign:                                                                                                                                                | Configuration to override the default retry behavior of the client.                                                                                               |

### Response

**[models.CountResponseInputTokensResponse](../../models/countresponseinputtokensresponse.md)**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.SDKError | 4XX, 5XX        | \*/\*           |