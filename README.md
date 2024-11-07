# Mistral Python Client

## Migration warning
 
This documentation is for Mistral AI SDK v1. You can find more details on how to migrate from v0 to v1 [here](MIGRATION.md)

## API Key Setup

Before you begin, you will need a Mistral AI API key.

1. Get your own Mistral API Key: <https://docs.mistral.ai/#api-access>
2. Set your Mistral API Key as an environment variable. You only need to do this once.

```bash
# set Mistral API Key (using zsh for example)
$ echo 'export MISTRAL_API_KEY=[your_key_here]' >> ~/.zshenv

# reload the environment (or just quit and open a new terminal)
$ source ~/.zshenv
```

<!-- Start Summary [summary] -->
## Summary

Mistral AI API: Our Chat Completion and Embeddings APIs specification. Create your account on [La Plateforme](https://console.mistral.ai) to get access and read the [docs](https://docs.mistral.ai) to learn how to use it.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents

* [SDK Installation](#sdk-installation)
* [IDE Support](#ide-support)
* [SDK Example Usage](#sdk-example-usage)
* [Available Resources and Operations](#available-resources-and-operations)
* [Server-sent event streaming](#server-sent-event-streaming)
* [File uploads](#file-uploads)
* [Retries](#retries)
* [Error Handling](#error-handling)
* [Server Selection](#server-selection)
* [Custom HTTP Client](#custom-http-client)
* [Authentication](#authentication)
* [Debugging](#debugging)
<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install mistralai
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add mistralai
```
<!-- End SDK Installation [installation] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.chat.complete(model="mistral-small-latest", messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
])

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ])
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```

### Upload a file

This example shows how to upload a file.

```python
# Synchronous Example
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.files.upload(file={
    "file_name": "example.file",
    "content": open("example.file", "rb"),
})

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.files.upload_async(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    })
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```

### Create Agents Completions

This example shows how to create agents completions.

```python
# Synchronous Example
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.agents.complete(messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
], agent_id="<value>")

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.agents.complete_async(messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], agent_id="<value>")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```

### Create Embedding Request

This example shows how to create embedding request.

```python
# Synchronous Example
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.embeddings.create(inputs=[
    "Embed this sentence.",
    "As well as this one.",
], model="Wrangler")

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from mistralai import Mistral
import os

async def main():
    s = Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    )
    res = await s.embeddings.create_async(inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ], model="Wrangler")
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->


### More examples

You can run the examples in the `examples/` directory using `poetry run` or by entering the virtual environment using `poetry shell`.


## Providers' SDKs Example Usage

### Azure AI

**Prerequisites**

Before you begin, ensure you have `AZUREAI_ENDPOINT` and an `AZURE_API_KEY`. To obtain these, you will need to deploy Mistral on Azure AI.
See [instructions for deploying Mistral on Azure AI here](https://docs.mistral.ai/deployment/cloud/azure/).

Here's a basic example to get you started. You can also run [the example in the `examples` directory](/examples/azure).

```python
import asyncio
import os

from mistralai_azure import MistralAzure

client = MistralAzure(
    azure_api_key=os.getenv("AZURE_API_KEY", ""),
    azure_endpoint=os.getenv("AZURE_ENDPOINT", "")
)

async def main() -> None:
    res = await client.chat.complete_async( 
        max_tokens= 100,
        temperature= 0.5,
        messages= [
            {
                "content": "Hello there!",
                "role": "user"
            }
        ]
    )
    print(res)

asyncio.run(main())
```
The documentation for the Azure SDK is available [here](packages/mistralai_azure/README.md).

### Google Cloud


**Prerequisites**

Before you begin, you will need to create a Google Cloud project and enable the Mistral API. To do this, follow the instructions [here](https://docs.mistral.ai/deployment/cloud/vertex/).

To run this locally you will also need to ensure you are authenticated with Google Cloud. You can do this by running

```bash
gcloud auth application-default login
```

**Step 1: Install**

Install the extras dependencies specific to Google Cloud:

```bash
pip install mistralai[gcp]
```

**Step 2: Example Usage**

Here's a basic example to get you started.

```python
import asyncio
from mistralai_gcp import MistralGoogleCloud

client = MistralGoogleCloud()


async def main() -> None:
    res = await client.chat.complete_async(
        model= "mistral-small-2402",
        messages= [
            {
                "content": "Hello there!",
                "role": "user"
            }
        ]
    )
    print(res)

asyncio.run(main())
```

The documentation for the GCP SDK is available [here](packages/mistralai_gcp/README.md).


<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [agents](docs/sdks/agents/README.md)

* [complete](docs/sdks/agents/README.md#complete) - Agents Completion
* [stream](docs/sdks/agents/README.md#stream) - Stream Agents completion

### [batch](docs/sdks/batch/README.md)


#### [batch.jobs](docs/sdks/mistraljobs/README.md)

* [list](docs/sdks/mistraljobs/README.md#list) - Get Batch Jobs
* [create](docs/sdks/mistraljobs/README.md#create) - Create Batch Job
* [get](docs/sdks/mistraljobs/README.md#get) - Get Batch Job
* [cancel](docs/sdks/mistraljobs/README.md#cancel) - Cancel Batch Job

### [chat](docs/sdks/chat/README.md)

* [complete](docs/sdks/chat/README.md#complete) - Chat Completion
* [stream](docs/sdks/chat/README.md#stream) - Stream chat completion

### [classifiers](docs/sdks/classifiers/README.md)

* [moderate](docs/sdks/classifiers/README.md#moderate) - Moderations
* [moderate_chat](docs/sdks/classifiers/README.md#moderate_chat) - Moderations Chat

### [embeddings](docs/sdks/embeddings/README.md)

* [create](docs/sdks/embeddings/README.md#create) - Embeddings

### [files](docs/sdks/files/README.md)

* [upload](docs/sdks/files/README.md#upload) - Upload File
* [list](docs/sdks/files/README.md#list) - List Files
* [retrieve](docs/sdks/files/README.md#retrieve) - Retrieve File
* [delete](docs/sdks/files/README.md#delete) - Delete File
* [download](docs/sdks/files/README.md#download) - Download File

### [fim](docs/sdks/fim/README.md)

* [complete](docs/sdks/fim/README.md#complete) - Fim Completion
* [stream](docs/sdks/fim/README.md#stream) - Stream fim completion

### [fine_tuning](docs/sdks/finetuning/README.md)


#### [fine_tuning.jobs](docs/sdks/jobs/README.md)

* [list](docs/sdks/jobs/README.md#list) - Get Fine Tuning Jobs
* [create](docs/sdks/jobs/README.md#create) - Create Fine Tuning Job
* [get](docs/sdks/jobs/README.md#get) - Get Fine Tuning Job
* [cancel](docs/sdks/jobs/README.md#cancel) - Cancel Fine Tuning Job
* [start](docs/sdks/jobs/README.md#start) - Start Fine Tuning Job


### [models](docs/sdks/models/README.md)

* [list](docs/sdks/models/README.md#list) - List Models
* [retrieve](docs/sdks/models/README.md#retrieve) - Retrieve Model
* [delete](docs/sdks/models/README.md#delete) - Delete Model
* [update](docs/sdks/models/README.md#update) - Update Fine Tuned Model
* [archive](docs/sdks/models/README.md#archive) - Archive Fine Tuned Model
* [unarchive](docs/sdks/models/README.md#unarchive) - Unarchive Fine Tuned Model

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.chat.stream(model="mistral-small-latest", messages=[
    {
        "content": "Who is the best French painter? Answer in one short sentence.",
        "role": "user",
    },
])

if res is not None:
    for event in res:
        # handle event
        print(event, flush=True)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://wiki.python.org/moin/Generators
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.files.upload(file={
    "file_name": "example.file",
    "content": open("example.file", "rb"),
})

if res is not None:
    # handle response
    pass

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from mistral.utils import BackoffStrategy, RetryConfig
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.models.list(,
    RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

if res is not None:
    # handle response
    pass

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from mistral.utils import BackoffStrategy, RetryConfig
from mistralai import Mistral
import os

s = Mistral(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.models.list()

if res is not None:
    # handle response
    pass

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.SDKError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `list_async` method may raise the following exceptions:

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| models.HTTPValidationError | 422                        | application/json           |
| models.SDKError            | 4XX, 5XX                   | \*/\*                      |

### Example

```python
from mistralai import Mistral, models
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = None
try:
    res = s.models.list()

    if res is not None:
        # handle response
        pass

except models.HTTPValidationError as e:
    # handle e.data: models.HTTPValidationErrorData
    raise(e)
except models.SDKError as e:
    # handle exception
    raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Name

You can override the default server globally by passing a server name to the `server: str` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the names associated with the available servers:

| Name | Server | Variables |
| ----- | ------ | --------- |
| `eu` | `https://api.mistral.ai` | None |

#### Example

```python
from mistralai import Mistral
import os

s = Mistral(
    server="eu",
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.models.list()

if res is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from mistralai import Mistral
import os

s = Mistral(
    server_url="https://api.mistral.ai",
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.models.list()

if res is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from mistralai import Mistral
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Mistral(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from mistralai import Mistral
from mistralai.httpclient import AsyncHttpClient
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

s = Mistral(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name                 | Type                 | Scheme               | Environment Variable |
| -------------------- | -------------------- | -------------------- | -------------------- |
| `api_key`            | http                 | HTTP Bearer          | `MISTRAL_API_KEY`    |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from mistralai import Mistral
import os

s = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
)

res = s.models.list()

if res is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from mistralai import Mistral
import logging

logging.basicConfig(level=logging.DEBUG)
s = Mistral(debug_logger=logging.getLogger("mistralai"))
```

You can also enable a default debug logger by setting an environment variable `MISTRAL_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 