# Mistral on Azure Python Client

## SDK Installation

PIP
```bash
pip install mistralai
```

UV
```bash
uv add mistralai
```

**Prerequisites**

Before you begin, ensure you have `AZUREAI_ENDPOINT` and an `AZURE_API_KEY`. To obtain these, you will need to deploy Mistral on Azure AI.
See [instructions for deploying Mistral on Azure AI here](https://docs.mistral.ai/deployment/cloud/azure/).

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.complete(
    messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], 
    model="azureai"
)

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai_azure import MistralAzure
import os

async def main():
    s = MistralAzure(
        azure_api_key=os.getenv("AZURE_API_KEY", ""),
        azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
    )
    res = await s.chat.complete_async(
        messages=[
            {
                "content": "Who is the best French painter? Answer in one short sentence.",
                "role": "user",
            },
        ], 
        model="azureai"
    )
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [chat](docs/sdks/chat/README.md)

* [stream](docs/sdks/chat/README.md#stream) - Stream chat completion
* [create](docs/sdks/chat/README.md#create) - Chat Completion
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.

```python
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(
    messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], 
    model="azureai"
)

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
from mistralai_azure import MistralAzure
from mistralazure.utils import BackoffStrategy, RetryConfig
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai",
    RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

if res is not None:
    for event in res:
        # handle event
        print(event)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from mistralai_azure import MistralAzure
from mistralazure.utils import BackoffStrategy, RetryConfig
import os

s = MistralAzure(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

if res is not None:
    for event in res:
        # handle event
        print(event)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object               | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| models.HTTPValidationError | 422         | application/json |
| models.SDKError            | 4xx-5xx     | */*              |

### Example

```python
from mistralai_azure import MistralAzure, models
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)

res = None
try:
    res = s.chat.complete(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

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

### Select Server by Name

You can override the default server globally by passing a server name to the `server: str` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the names associated with the available servers:

| Name   | Server                   | Variables |
| ------ | ------------------------ | --------- |
| `prod` | `https://api.mistral.ai` | None      |

#### Example

```python
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    server="prod",
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

if res is not None:
    for event in res:
        # handle event
        print(event)

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    server_url="https://api.mistral.ai",
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

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
from mistralai_azure import MistralAzure
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = MistralAzure(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from mistralai_azure import MistralAzure
from mistralai_azure.httpclient import AsyncHttpClient
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

s = MistralAzure(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type | Scheme      |
| --------- | ---- | ----------- |
| `api_key` | http | HTTP Bearer |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from mistralai_azure import MistralAzure
import os

s = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)


res = s.chat.stream(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], model="azureai")

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
