# Mistral on GCP Python Client


**Prerequisites**

Before you begin, you will need to create a Google Cloud project and enable the Mistral API. To do this, follow the instructions [here](https://docs.mistral.ai/deployment/cloud/vertex/).

To run this locally you will also need to ensure you are authenticated with Google Cloud. You can do this by running

```bash
gcloud auth application-default login
```

## SDK Installation

Install the extras dependencies specific to Google Cloud:

```bash
pip install mistralai[gcp]
```

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Create Chat Completions

This example shows how to create chat completions.

> **Note:** GCP Vertex AI requires constructing the endpoint URL from your
> project ID, region, and model. An access token is obtained via `gcloud`.

```python
# Synchronous Example
import os
import subprocess
from mistralai.gcp.client import MistralGCP


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
)

res = s.chat.complete(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model=GCP_MODEL)

if res is not None:
    # handle response
    print(res.choices[0].message.content)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import os
import subprocess
from mistralai.gcp.client import MistralGCP


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

async def main():
    s = MistralGCP(
        api_key=get_token(),
        server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
    )
    res = await s.chat.complete_async(messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], model=GCP_MODEL)
    if res is not None:
        # handle response
        print(res.choices[0].message.content)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [chat](docs/sdks/chat/README.md)

* [stream](docs/sdks/chat/README.md#stream) - Stream chat completion
* [complete](docs/sdks/chat/README.md#complete) - Chat Completion

### [fim](docs/sdks/fim/README.md)

* [stream](docs/sdks/fim/README.md#stream) - Stream fim completion
* [complete](docs/sdks/fim/README.md#complete) - Fim Completion
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.

```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
)

res = s.chat.stream(messages=[
    {
        "role": "user",
        "content": "Who is the best French painter? Answer in one short sentence.",
    },
], model=GCP_MODEL)

if res is not None:
    for event in res:
        # handle event
        print(event)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://wiki.python.org/moin/Generators
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.utils import BackoffStrategy, RetryConfig


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
)

res = s.chat.stream(
    messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ],
    model=GCP_MODEL,
    retries=RetryConfig(
        "backoff",
        BackoffStrategy(1, 50, 1.1, 100),
        False
    )
)

if res is not None:
    for event in res:
        # handle event
        print(event)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.utils import BackoffStrategy, RetryConfig


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
)

res = s.chat.stream(
    messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ],
    model=GCP_MODEL,
)

if res is not None:
    for event in res:
        # handle event
        print(event)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an error. If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object               | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| models.HTTPValidationError | 422         | application/json |
| models.SDKError            | 4xx-5xx     | */*              |

### Example

```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client import models


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


def build_vertex_url(project_id, region, model):
    return (
        f"https://{region}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{region}/"
        f"publishers/mistralai/models/{model}"
    )


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=build_vertex_url(GCP_PROJECT_ID, GCP_REGION, GCP_MODEL),
)

res = None
try:
    res = s.chat.complete(
        messages=[
            {
                "role": "user",
                "content": "Who is the best French painter? Answer in one short sentence.",
            },
        ],
        model=GCP_MODEL,
    )

except models.HTTPValidationError as e:
    # handle exception
    raise(e)
except models.SDKError as e:
    # handle exception
    raise(e)

if res is not None:
    # handle response
    pass

```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

For GCP, you **must** override the default server URL with your Vertex AI endpoint:
```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP


def get_token():
    return subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True,
    ).stdout.strip()


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=get_token(),
    server_url=(
        f"https://{GCP_REGION}-aiplatform.googleapis.com/v1/"
        f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/"
        f"publishers/mistralai/models/{GCP_MODEL}"
    ),
)

res = s.chat.stream(
    messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ],
    model=GCP_MODEL,
)

if res is not None:
    for event in res:
        # handle event
        print(event)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from mistralai.gcp.client import MistralGCP
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = MistralGCP(
    api_key="<your-gcloud-token>",
    server_url="<your-vertex-ai-url>",
    client=http_client,
)
```

or you could wrap the client with your own custom logic:
```python
from typing import Any, Optional, Union
from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = MistralGCP(
    api_key="<your-gcloud-token>",
    server_url="<your-vertex-ai-url>",
    async_client=CustomClient(httpx.AsyncClient()),
)
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type | Scheme      |
| --------- | ---- | ----------- |
| `api_key` | http | HTTP Bearer |

For GCP, the `api_key` is a short-lived OAuth token obtained via `gcloud auth print-access-token`. You must also provide `server_url` pointing to your Vertex AI endpoint. For example:
```python
import os
import subprocess
from mistralai.gcp.client import MistralGCP

token = subprocess.run(
    ["gcloud", "auth", "print-access-token"],
    capture_output=True, text=True,
).stdout.strip()

GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_MODEL = os.environ["GCP_MODEL"]

s = MistralGCP(
    api_key=token,
    server_url=(
        f"https://{GCP_REGION}-aiplatform.googleapis.com/v1/"
        f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/"
        f"publishers/mistralai/models/{GCP_MODEL}"
    ),
)

res = s.chat.stream(
    messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ],
    model=GCP_MODEL,
)

if res is not None:
    for event in res:
        # handle event
        print(event)

```
<!-- End Authentication [security] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation.
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release.
