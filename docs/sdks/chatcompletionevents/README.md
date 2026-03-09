# Beta.Observability.ChatCompletionEvents

## Overview

### Available Operations

* [search](#search) - Get Chat Completion Events
* [search_ids](#search_ids) - Alternative to /search that returns only the IDs and that can return many IDs at once
* [fetch](#fetch) - Get Chat Completion Event
* [fetch_similar_events](#fetch_similar_events) - Get Similar Chat Completion Events
* [judge](#judge) - Run Judge on an event based on the given options

## search

Get Chat Completion Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_events_v1_observability_chat_completion_events_search_post" method="post" path="/v1/observability/chat-completion-events/search" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.search(search_params={
        "filters": None,
    }, page_size=50)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `search_params`                                                     | [models.FilterPayload](../../models/filterpayload.md)               | :heavy_check_mark:                                                  | N/A                                                                 |
| `page_size`                                                         | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `cursor`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `extra_fields`                                                      | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SearchChatCompletionEventsResponse](../../models/searchchatcompletioneventsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## search_ids

Alternative to /search that returns only the IDs and that can return many IDs at once

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_event_ids_v1_observability_chat_completion_events_search_ids_post" method="post" path="/v1/observability/chat-completion-events/search-ids" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.search_ids(search_params={
        "filters": {
            "field": "<value>",
            "op": "lt",
            "value": "<value>",
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `search_params`                                                     | [models.FilterPayload](../../models/filterpayload.md)               | :heavy_check_mark:                                                  | N/A                                                                 |
| `extra_fields`                                                      | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SearchChatCompletionEventIdsResponse](../../models/searchchatcompletioneventidsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch

Get Chat Completion Event

### Example Usage

<!-- UsageSnippet language="python" operationID="get_chat_completion_event_v1_observability_chat_completion_events__event_id__get" method="get" path="/v1/observability/chat-completion-events/{event_id}" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.fetch(event_id="e79bf81b-b37f-425e-9dff-071a54592e44")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `event_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ChatCompletionEvent](../../models/chatcompletionevent.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## fetch_similar_events

Get Similar Chat Completion Events

### Example Usage

<!-- UsageSnippet language="python" operationID="get_similar_chat_completion_events_v1_observability_chat_completion_events__event_id__similar_events_get" method="get" path="/v1/observability/chat-completion-events/{event_id}/similar-events" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.fetch_similar_events(event_id="b7be6e08-d068-45fc-b77a-966232e92fd6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `event_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.SearchChatCompletionEventsResponse](../../models/searchchatcompletioneventsresponse.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |

## judge

Run Judge on an event based on the given options

### Example Usage

<!-- UsageSnippet language="python" operationID="judge_chat_completion_event_v1_observability_chat_completion_events__event_id__live_judging_post" method="post" path="/v1/observability/chat-completion-events/{event_id}/live-judging" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.beta.observability.chat_completion_events.judge(event_id="dfcd5582-1373-4de5-af51-987464da561c", judge_definition={
        "name": "<value>",
        "description": "total plain self-confidence candid hungrily partial astride cruelly brr",
        "model_name": "<value>",
        "output": {
            "type": "CLASSIFICATION",
            "options": [
                {
                    "value": "<value>",
                    "description": "indeed insolence delightfully following",
                },
            ],
        },
        "instructions": "<value>",
        "tools": [],
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `event_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `judge_definition`                                                  | [models.CreateJudgeRequest](../../models/createjudgerequest.md)     | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.JudgeOutput](../../models/judgeoutput.md)**

### Errors

| Error Type                | Status Code               | Content Type              |
| ------------------------- | ------------------------- | ------------------------- |
| errors.ObservabilityError | 400, 404, 408, 409, 422   | application/json          |
| errors.SDKError           | 4XX, 5XX                  | \*/\*                     |