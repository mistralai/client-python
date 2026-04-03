# Mistral Python Client

## Migrating from v1

If you are upgrading from v1 to v2, check the [migration guide](https://github.com/mistralai/client-python/blob/main/MIGRATION.md) for details on breaking changes and how to update your code.

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
<!-- $toc-max-depth=2 -->
* [Mistral Python Client](#mistral-python-client)
  * [Migrating from v1](#migrating-from-v1)
  * [API Key Setup](#api-key-setup)
  * [SDK Installation](#sdk-installation)
  * [SDK Example Usage](#sdk-example-usage)
  * [Providers' SDKs Example Usage](#providers-sdks-example-usage)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Server-sent event streaming](#server-sent-event-streaming)
  * [Pagination](#pagination)
  * [File uploads](#file-uploads)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Authentication](#authentication)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
  * [IDE Support](#ide-support)
* [Development](#development)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with *uv*, *pip*, or *poetry* package managers.

### uv

*uv* is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add mistralai
```

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

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from mistralai python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mistralai",
# ]
# ///

from mistralai.client import Mistral

sdk = Mistral(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

### Agents extra dependencies

When using the agents related feature it is required to add the `agents` extra dependencies. This can be added when
installing the package:

```bash
pip install "mistralai[agents]"
```

> Note: These features require Python 3.10+ (the SDK minimum).

### Additional packages

Additional `mistralai-*` packages (e.g. `mistralai-workflows`) can be installed separately and are available under the `mistralai` namespace:

```bash
pip install mistralai-workflows
```

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Create Chat Completions

This example shows how to create chat completions.

```python
# Synchronous Example
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-large-latest", messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], stream=False, response_format={
        "type": "text",
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "role": "user",
                "content": "Who is the best French painter? Answer in one short sentence.",
            },
        ], stream=False, response_format={
            "type": "text",
        })

        # Handle response
        print(res)

asyncio.run(main())
```

### Upload a file

This example shows how to upload a file.

```python
# Synchronous Example
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.files.upload(file={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    }, visibility="workspace")

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.files.upload_async(file={
            "file_name": "example.file",
            "content": open("example.file", "rb"),
        }, visibility="workspace")

        # Handle response
        print(res)

asyncio.run(main())
```

### Create Agents Completions

This example shows how to create agents completions.

```python
# Synchronous Example
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.agents.complete(messages=[
        {
            "role": "user",
            "content": "Who is the best French painter? Answer in one short sentence.",
        },
    ], agent_id="<id>", stream=False, response_format={
        "type": "text",
    })

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.agents.complete_async(messages=[
            {
                "role": "user",
                "content": "Who is the best French painter? Answer in one short sentence.",
            },
        ], agent_id="<id>", stream=False, response_format={
            "type": "text",
        })

        # Handle response
        print(res)

asyncio.run(main())
```

### Create Embedding Request

This example shows how to create embedding request.

```python
# Synchronous Example
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.embeddings.create(model="mistral-embed", inputs=[
        "Embed this sentence.",
        "As well as this one.",
    ])

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from mistralai.client import Mistral
import os

async def main():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        res = await mistral.embeddings.create_async(model="mistral-embed", inputs=[
            "Embed this sentence.",
            "As well as this one.",
        ])

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->


### More examples

You can run the examples in the `examples/` directory using `uv run`.


## Providers' SDKs Example Usage

### Azure AI

**Prerequisites**

Before you begin, ensure you have `AZURE_ENDPOINT` and an `AZURE_API_KEY`. To obtain these, you will need to deploy Mistral on Azure AI.
See [instructions for deploying Mistral on Azure AI here](https://docs.mistral.ai/deployment/cloud/azure/).

**Step 1: Install**

```bash
pip install mistralai
```

**Step 2: Example Usage**

Here's a basic example to get you started. You can also run [the example in the `examples` directory](/examples/azure).

```python
import os
from mistralai.azure.client import MistralAzure

# The SDK automatically injects api-version as a query parameter
client = MistralAzure(
    api_key=os.environ["AZURE_API_KEY"],
    server_url=os.environ["AZURE_ENDPOINT"],
    api_version="2024-05-01-preview",  # Optional, this is the default
)

res = client.chat.complete(
    model=os.environ["AZURE_MODEL"],
    messages=[
        {
            "role": "user",
            "content": "Hello there!",
        }
    ],
)
print(res.choices[0].message.content)
```

### Google Cloud


**Prerequisites**

Before you begin, you will need to create a Google Cloud project and enable the Mistral API. To do this, follow the instructions [here](https://docs.mistral.ai/deployment/cloud/vertex/).

To run this locally you will also need to ensure you are authenticated with Google Cloud. You can do this by running

```bash
gcloud auth application-default login
```

**Step 1: Install**

```bash
pip install mistralai
# For GCP authentication support (required):
pip install "mistralai[gcp]"
```

**Step 2: Example Usage**

Here's a basic example to get you started. You can also run [the example in the `examples` directory](/examples/gcp).

The SDK automatically:
- Detects credentials via `google.auth.default()`
- Auto-refreshes tokens when they expire
- Builds the Vertex AI URL from `project_id` and `region`

```python
import os
from mistralai.gcp.client import MistralGCP

# The SDK auto-detects credentials and builds the Vertex AI URL
client = MistralGCP(
    project_id=os.environ.get("GCP_PROJECT_ID"),  # Optional: auto-detected from credentials
    region="us-central1",  # Default: europe-west4
)

res = client.chat.complete(
    model="mistral-small-2503",
    messages=[
        {
            "role": "user",
            "content": "Hello there!",
        }
    ],
)
print(res.choices[0].message.content)
```


<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [Agents](docs/sdks/agents/README.md)

* [complete](docs/sdks/agents/README.md#complete) - Agents Completion
* [stream](docs/sdks/agents/README.md#stream) - Stream Agents completion

### [Audio.Speech](docs/sdks/speech/README.md)

* [complete](docs/sdks/speech/README.md#complete) - Speech

### [Audio.Transcriptions](docs/sdks/transcriptions/README.md)

* [complete](docs/sdks/transcriptions/README.md#complete) - Create Transcription
* [stream](docs/sdks/transcriptions/README.md#stream) - Create Streaming Transcription (SSE)

### [Audio.Voices](docs/sdks/voices/README.md)

* [list](docs/sdks/voices/README.md#list) - List all voices
* [create](docs/sdks/voices/README.md#create) - Create a new voice
* [delete](docs/sdks/voices/README.md#delete) - Delete a custom voice
* [update](docs/sdks/voices/README.md#update) - Update voice metadata
* [get](docs/sdks/voices/README.md#get) - Get voice details
* [get_sample_audio](docs/sdks/voices/README.md#get_sample_audio) - Get voice sample audio

### [Batch.Jobs](docs/sdks/batchjobs/README.md)

* [list](docs/sdks/batchjobs/README.md#list) - Get Batch Jobs
* [create](docs/sdks/batchjobs/README.md#create) - Create Batch Job
* [get](docs/sdks/batchjobs/README.md#get) - Get Batch Job
* [delete](docs/sdks/batchjobs/README.md#delete) - Delete Batch Job
* [cancel](docs/sdks/batchjobs/README.md#cancel) - Cancel Batch Job

### [Beta.Agents](docs/sdks/betaagents/README.md)

* [create](docs/sdks/betaagents/README.md#create) - Create a agent that can be used within a conversation.
* [list](docs/sdks/betaagents/README.md#list) - List agent entities.
* [get](docs/sdks/betaagents/README.md#get) - Retrieve an agent entity.
* [update](docs/sdks/betaagents/README.md#update) - Update an agent entity.
* [delete](docs/sdks/betaagents/README.md#delete) - Delete an agent entity.
* [update_version](docs/sdks/betaagents/README.md#update_version) - Update an agent version.
* [list_versions](docs/sdks/betaagents/README.md#list_versions) - List all versions of an agent.
* [get_version](docs/sdks/betaagents/README.md#get_version) - Retrieve a specific version of an agent.
* [create_version_alias](docs/sdks/betaagents/README.md#create_version_alias) - Create or update an agent version alias.
* [list_version_aliases](docs/sdks/betaagents/README.md#list_version_aliases) - List all aliases for an agent.
* [delete_version_alias](docs/sdks/betaagents/README.md#delete_version_alias) - Delete an agent version alias.

### [Beta.Connectors](docs/sdks/connectors/README.md)

* [create](docs/sdks/connectors/README.md#create) - Create a new connector.
* [list](docs/sdks/connectors/README.md#list) - List all connectors.
* [get_auth_url](docs/sdks/connectors/README.md#get_auth_url) - Get the auth URL for a connector.
* [call_tool](docs/sdks/connectors/README.md#call_tool) - Call Connector Tool
* [list_tools](docs/sdks/connectors/README.md#list_tools) - List tools for a connector.
* [get](docs/sdks/connectors/README.md#get) - Get a connector.
* [update](docs/sdks/connectors/README.md#update) - Update a connector.
* [delete](docs/sdks/connectors/README.md#delete) - Delete a connector.

### [Beta.Conversations](docs/sdks/conversations/README.md)

* [start](docs/sdks/conversations/README.md#start) - Create a conversation and append entries to it.
* [list](docs/sdks/conversations/README.md#list) - List all created conversations.
* [get](docs/sdks/conversations/README.md#get) - Retrieve a conversation information.
* [delete](docs/sdks/conversations/README.md#delete) - Delete a conversation.
* [append](docs/sdks/conversations/README.md#append) - Append new entries to an existing conversation.
* [get_history](docs/sdks/conversations/README.md#get_history) - Retrieve all entries in a conversation.
* [get_messages](docs/sdks/conversations/README.md#get_messages) - Retrieve all messages in a conversation.
* [restart](docs/sdks/conversations/README.md#restart) - Restart a conversation starting from a given entry.
* [start_stream](docs/sdks/conversations/README.md#start_stream) - Create a conversation and append entries to it.
* [append_stream](docs/sdks/conversations/README.md#append_stream) - Append new entries to an existing conversation.
* [restart_stream](docs/sdks/conversations/README.md#restart_stream) - Restart a conversation starting from a given entry.

### [Beta.Libraries](docs/sdks/libraries/README.md)

* [list](docs/sdks/libraries/README.md#list) - List all libraries you have access to.
* [create](docs/sdks/libraries/README.md#create) - Create a new Library.
* [get](docs/sdks/libraries/README.md#get) - Detailed information about a specific Library.
* [delete](docs/sdks/libraries/README.md#delete) - Delete a library and all of it's document.
* [update](docs/sdks/libraries/README.md#update) - Update a library.

#### [Beta.Libraries.Accesses](docs/sdks/accesses/README.md)

* [list](docs/sdks/accesses/README.md#list) - List all of the access to this library.
* [update_or_create](docs/sdks/accesses/README.md#update_or_create) - Create or update an access level.
* [delete](docs/sdks/accesses/README.md#delete) - Delete an access level.

#### [Beta.Libraries.Documents](docs/sdks/documents/README.md)

* [list](docs/sdks/documents/README.md#list) - List documents in a given library.
* [upload](docs/sdks/documents/README.md#upload) - Upload a new document.
* [get](docs/sdks/documents/README.md#get) - Retrieve the metadata of a specific document.
* [update](docs/sdks/documents/README.md#update) - Update the metadata of a specific document.
* [delete](docs/sdks/documents/README.md#delete) - Delete a document.
* [text_content](docs/sdks/documents/README.md#text_content) - Retrieve the text content of a specific document.
* [status](docs/sdks/documents/README.md#status) - Retrieve the processing status of a specific document.
* [get_signed_url](docs/sdks/documents/README.md#get_signed_url) - Retrieve the signed URL of a specific document.
* [extracted_text_signed_url](docs/sdks/documents/README.md#extracted_text_signed_url) - Retrieve the signed URL of text extracted from a given document.
* [reprocess](docs/sdks/documents/README.md#reprocess) - Reprocess a document.

### [Beta.Observability.Campaigns](docs/sdks/campaigns/README.md)

* [create](docs/sdks/campaigns/README.md#create) - Create and start a new campaign
* [list](docs/sdks/campaigns/README.md#list) - Get all campaigns
* [fetch](docs/sdks/campaigns/README.md#fetch) - Get campaign by id
* [delete](docs/sdks/campaigns/README.md#delete) - Delete a campaign
* [fetch_status](docs/sdks/campaigns/README.md#fetch_status) - Get campaign status by campaign id
* [list_events](docs/sdks/campaigns/README.md#list_events) - Get event ids that were selected by the given campaign

### [Beta.Observability.ChatCompletionEvents](docs/sdks/chatcompletionevents/README.md)

* [search](docs/sdks/chatcompletionevents/README.md#search) - Get Chat Completion Events
* [search_ids](docs/sdks/chatcompletionevents/README.md#search_ids) - Alternative to /search that returns only the IDs and that can return many IDs at once
* [fetch](docs/sdks/chatcompletionevents/README.md#fetch) - Get Chat Completion Event
* [fetch_similar_events](docs/sdks/chatcompletionevents/README.md#fetch_similar_events) - Get Similar Chat Completion Events
* [judge](docs/sdks/chatcompletionevents/README.md#judge) - Run Judge on an event based on the given options

#### [Beta.Observability.ChatCompletionEvents.Fields](docs/sdks/fields/README.md)

* [list](docs/sdks/fields/README.md#list) - Get Chat Completion Fields
* [fetch_options](docs/sdks/fields/README.md#fetch_options) - Get Chat Completion Field Options
* [fetch_option_counts](docs/sdks/fields/README.md#fetch_option_counts) - Get Chat Completion Field Options Counts

### [Beta.Observability.Datasets](docs/sdks/datasets/README.md)

* [create](docs/sdks/datasets/README.md#create) - Create a new empty dataset
* [list](docs/sdks/datasets/README.md#list) - List existing datasets
* [fetch](docs/sdks/datasets/README.md#fetch) - Get dataset by id
* [delete](docs/sdks/datasets/README.md#delete) - Delete a dataset
* [update](docs/sdks/datasets/README.md#update) - Patch dataset
* [list_records](docs/sdks/datasets/README.md#list_records) - List existing records in the dataset
* [create_record](docs/sdks/datasets/README.md#create_record) - Add a conversation to the dataset
* [import_from_campaign](docs/sdks/datasets/README.md#import_from_campaign) - Populate the dataset with a campaign
* [import_from_explorer](docs/sdks/datasets/README.md#import_from_explorer) - Populate the dataset with samples from the explorer
* [import_from_file](docs/sdks/datasets/README.md#import_from_file) - Populate the dataset with samples from an uploaded file
* [import_from_playground](docs/sdks/datasets/README.md#import_from_playground) - Populate the dataset with samples from the playground
* [import_from_dataset_records](docs/sdks/datasets/README.md#import_from_dataset_records) - Populate the dataset with samples from another dataset
* [export_to_jsonl](docs/sdks/datasets/README.md#export_to_jsonl) - Export to the Files API and retrieve presigned URL to download the resulting JSONL file
* [fetch_task](docs/sdks/datasets/README.md#fetch_task) - Get status of a dataset import task
* [list_tasks](docs/sdks/datasets/README.md#list_tasks) - List import tasks for the given dataset

#### [Beta.Observability.Datasets.Records](docs/sdks/records/README.md)

* [fetch](docs/sdks/records/README.md#fetch) - Get the content of a given conversation from a dataset
* [delete](docs/sdks/records/README.md#delete) - Delete a record from a dataset
* [bulk_delete](docs/sdks/records/README.md#bulk_delete) - Delete multiple records from datasets
* [judge](docs/sdks/records/README.md#judge) - Run Judge on a dataset record based on the given options
* [update_payload](docs/sdks/records/README.md#update_payload) - Update a dataset record conversation payload
* [update_properties](docs/sdks/records/README.md#update_properties) - Update conversation properties

### [Beta.Observability.Judges](docs/sdks/judges/README.md)

* [create](docs/sdks/judges/README.md#create) - Create a new judge
* [list](docs/sdks/judges/README.md#list) - Get judges with optional filtering and search
* [fetch](docs/sdks/judges/README.md#fetch) - Get judge by id
* [delete](docs/sdks/judges/README.md#delete) - Delete a judge
* [update](docs/sdks/judges/README.md#update) - Update a judge
* [judge_conversation](docs/sdks/judges/README.md#judge_conversation) - Run a saved judge on a conversation

### [Chat](docs/sdks/chat/README.md)

* [complete](docs/sdks/chat/README.md#complete) - Chat Completion
* [stream](docs/sdks/chat/README.md#stream) - Stream chat completion

### [Classifiers](docs/sdks/classifiers/README.md)

* [moderate](docs/sdks/classifiers/README.md#moderate) - Moderations
* [moderate_chat](docs/sdks/classifiers/README.md#moderate_chat) - Chat Moderations
* [classify](docs/sdks/classifiers/README.md#classify) - Classifications
* [classify_chat](docs/sdks/classifiers/README.md#classify_chat) - Chat Classifications

### [Embeddings](docs/sdks/embeddings/README.md)

* [create](docs/sdks/embeddings/README.md#create) - Embeddings

### [Events](docs/sdks/events/README.md)

* [get_stream_events](docs/sdks/events/README.md#get_stream_events) - Get Stream Events
* [get_workflow_events](docs/sdks/events/README.md#get_workflow_events) - Get Workflow Events

### [Files](docs/sdks/files/README.md)

* [upload](docs/sdks/files/README.md#upload) - Upload File
* [list](docs/sdks/files/README.md#list) - List Files
* [retrieve](docs/sdks/files/README.md#retrieve) - Retrieve File
* [delete](docs/sdks/files/README.md#delete) - Delete File
* [download](docs/sdks/files/README.md#download) - Download File
* [get_signed_url](docs/sdks/files/README.md#get_signed_url) - Get Signed Url

### [Fim](docs/sdks/fim/README.md)

* [complete](docs/sdks/fim/README.md#complete) - Fim Completion
* [stream](docs/sdks/fim/README.md#stream) - Stream fim completion

### [FineTuning.Jobs](docs/sdks/finetuningjobs/README.md)

* [list](docs/sdks/finetuningjobs/README.md#list) - Get Fine Tuning Jobs
* [create](docs/sdks/finetuningjobs/README.md#create) - Create Fine Tuning Job
* [get](docs/sdks/finetuningjobs/README.md#get) - Get Fine Tuning Job
* [cancel](docs/sdks/finetuningjobs/README.md#cancel) - Cancel Fine Tuning Job
* [start](docs/sdks/finetuningjobs/README.md#start) - Start Fine Tuning Job

### [Models](docs/sdks/models/README.md)

* [list](docs/sdks/models/README.md#list) - List Models
* [retrieve](docs/sdks/models/README.md#retrieve) - Retrieve Model
* [delete](docs/sdks/models/README.md#delete) - Delete Model
* [update](docs/sdks/models/README.md#update) - Update Fine Tuned Model
* [archive](docs/sdks/models/README.md#archive) - Archive Fine Tuned Model
* [unarchive](docs/sdks/models/README.md#unarchive) - Unarchive Fine Tuned Model

### [Ocr](docs/sdks/ocr/README.md)

* [process](docs/sdks/ocr/README.md#process) - OCR

### [Workflows](docs/sdks/workflows/README.md)

* [get_workflows](docs/sdks/workflows/README.md#get_workflows) - Get Workflows
* [get_workflow_registrations](docs/sdks/workflows/README.md#get_workflow_registrations) - Get Workflow Registrations
* [execute_workflow](docs/sdks/workflows/README.md#execute_workflow) - Execute Workflow
* [~~execute_workflow_registration~~](docs/sdks/workflows/README.md#execute_workflow_registration) - Execute Workflow Registration :warning: **Deprecated**
* [get_workflow](docs/sdks/workflows/README.md#get_workflow) - Get Workflow
* [update_workflow](docs/sdks/workflows/README.md#update_workflow) - Update Workflow
* [get_workflow_registration](docs/sdks/workflows/README.md#get_workflow_registration) - Get Workflow Registration
* [archive_workflow](docs/sdks/workflows/README.md#archive_workflow) - Archive Workflow
* [unarchive_workflow](docs/sdks/workflows/README.md#unarchive_workflow) - Unarchive Workflow

#### [Workflows.Deployments](docs/sdks/deployments/README.md)

* [list_deployments](docs/sdks/deployments/README.md#list_deployments) - List Deployments
* [get_deployment](docs/sdks/deployments/README.md#get_deployment) - Get Deployment

#### [Workflows.Events](docs/sdks/workflowsevents/README.md)

* [get_stream_events](docs/sdks/workflowsevents/README.md#get_stream_events) - Get Stream Events
* [get_workflow_events](docs/sdks/workflowsevents/README.md#get_workflow_events) - Get Workflow Events

#### [Workflows.Executions](docs/sdks/executions/README.md)

* [get_workflow_execution](docs/sdks/executions/README.md#get_workflow_execution) - Get Workflow Execution
* [get_workflow_execution_history](docs/sdks/executions/README.md#get_workflow_execution_history) - Get Workflow Execution History
* [signal_workflow_execution](docs/sdks/executions/README.md#signal_workflow_execution) - Signal Workflow Execution
* [query_workflow_execution](docs/sdks/executions/README.md#query_workflow_execution) - Query Workflow Execution
* [terminate_workflow_execution](docs/sdks/executions/README.md#terminate_workflow_execution) - Terminate Workflow Execution
* [batch_terminate_workflow_executions](docs/sdks/executions/README.md#batch_terminate_workflow_executions) - Batch Terminate Workflow Executions
* [cancel_workflow_execution](docs/sdks/executions/README.md#cancel_workflow_execution) - Cancel Workflow Execution
* [batch_cancel_workflow_executions](docs/sdks/executions/README.md#batch_cancel_workflow_executions) - Batch Cancel Workflow Executions
* [reset_workflow](docs/sdks/executions/README.md#reset_workflow) - Reset Workflow
* [update_workflow_execution](docs/sdks/executions/README.md#update_workflow_execution) - Update Workflow Execution
* [get_workflow_execution_trace_otel](docs/sdks/executions/README.md#get_workflow_execution_trace_otel) - Get Workflow Execution Trace Otel
* [get_workflow_execution_trace_summary](docs/sdks/executions/README.md#get_workflow_execution_trace_summary) - Get Workflow Execution Trace Summary
* [get_workflow_execution_trace_events](docs/sdks/executions/README.md#get_workflow_execution_trace_events) - Get Workflow Execution Trace Events
* [stream](docs/sdks/executions/README.md#stream) - Stream

#### [Workflows.Metrics](docs/sdks/metrics/README.md)

* [get_workflow_metrics](docs/sdks/metrics/README.md#get_workflow_metrics) - Get Workflow Metrics

#### [Workflows.Runs](docs/sdks/runs/README.md)

* [list_runs](docs/sdks/runs/README.md#list_runs) - List Runs
* [get_run](docs/sdks/runs/README.md#get_run) - Get Run
* [get_run_history](docs/sdks/runs/README.md#get_run_history) - Get Run History

#### [Workflows.Schedules](docs/sdks/schedules/README.md)

* [get_schedules](docs/sdks/schedules/README.md#get_schedules) - Get Schedules
* [schedule_workflow](docs/sdks/schedules/README.md#schedule_workflow) - Schedule Workflow
* [unschedule_workflow](docs/sdks/schedules/README.md#unschedule_workflow) - Unschedule Workflow

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Server-sent event streaming [eventstream] -->
## Server-sent event streaming

[Server-sent events][mdn-sse] are used to stream content from certain
operations. These operations will expose the stream as [Generator][generator] that
can be consumed using a simple `for` loop. The loop will
terminate when the server no longer has any events to send and closes the
underlying connection.  

The stream is also a [Context Manager][context-manager] and can be used with the `with` statement and will close the
underlying connection when the context is exited.

```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

[mdn-sse]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[generator]: https://book.pythontips.com/en/latest/generators.html
[context-manager]: https://book.pythontips.com/en/latest/context_managers.html
<!-- End Server-sent event streaming [eventstream] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.workflows.get_workflows(active_only=False, include_shared=True, limit=50)

    while res is not None:
        # Handle items

        res = res.next()

```
<!-- End Pagination [pagination] -->

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.transcriptions.complete(model="Model X", diarize=False)

    # Handle response
    print(res)

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from mistralai.client import Mistral
from mistralai.client.utils import BackoffStrategy, RetryConfig
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    },
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from mistralai.client import Mistral
from mistralai.client.utils import BackoffStrategy, RetryConfig
import os


with Mistral(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`MistralError`](./src/mistralai/client/errors/mistralerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
from mistralai.client import Mistral, errors
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:
    res = None
    try:

        res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

        })

        with res as event_stream:
            for event in event_stream:
                # handle event
                print(event, flush=True)


    except errors.MistralError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.HTTPValidationError):
            print(e.data.detail)  # Optional[List[models.ValidationError]]
```

### Error Classes
**Primary error:**
* [`MistralError`](./src/mistralai/client/errors/mistralerror.py): The base class for HTTP error responses.

<details><summary>Less common errors (7)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`MistralError`](./src/mistralai/client/errors/mistralerror.py)**:
* [`HTTPValidationError`](./src/mistralai/client/errors/httpvalidationerror.py): Validation Error. Status code `422`. Applicable to 103 of 168 methods.*
* [`ObservabilityError`](./src/mistralai/client/errors/observabilityerror.py): Bad Request - Invalid request parameters or data. Applicable to 41 of 168 methods.*
* [`ResponseValidationError`](./src/mistralai/client/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>

\* Check [the method documentation](#available-resources-and-operations) to see if the error is applicable.
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Name

You can override the default server globally by passing a server name to the `server: str` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the names associated with the available servers:

| Name | Server                   | Description          |
| ---- | ------------------------ | -------------------- |
| `eu` | `https://api.mistral.ai` | EU Production server |

#### Example

```python
from mistralai.client import Mistral
import os


with Mistral(
    server="eu",
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from mistralai.client import Mistral
import os


with Mistral(
    server_url="https://api.mistral.ai",
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from mistralai.client import Mistral
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Mistral(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from mistralai.client import Mistral
from mistralai.client.httpclient import AsyncHttpClient
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

| Name      | Type | Scheme      | Environment Variable |
| --------- | ---- | ----------- | -------------------- |
| `api_key` | http | HTTP Bearer | `MISTRAL_API_KEY`    |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from mistralai.client import Mistral
import os


with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.audio.speech.complete(input="<value>", stream=False, additional_properties={

    })

    with res as event_stream:
        for event in event_stream:
            # handle event
            print(event, flush=True)

```
<!-- End Authentication [security] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Mistral` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from mistralai.client import Mistral
import os
def main():

    with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from mistralai.client import Mistral
import logging

logging.basicConfig(level=logging.DEBUG)
s = Mistral(debug_logger=logging.getLogger("mistralai.client"))
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
