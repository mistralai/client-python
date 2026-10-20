# Realtime.Sessions

## Overview

### Available Operations

* [create](#create) - Create Client Session

## create

Create a client session. Requires the `create_client_session` permission.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_client_session_v1_client_sessions_post" method="post" path="/v1/client/sessions" -->
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.realtime.sessions.create(request={
        "purpose": "realtime",
        "model": "Ranchero",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `request`                                                           | [models.Body](../../models/body.md)                                 | :heavy_check_mark:                                                  | The request object to use for the request.                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateRealtimeSessionResponse](../../models/createrealtimesessionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.SDKError            | 4XX, 5XX                   | \*/\*                      |