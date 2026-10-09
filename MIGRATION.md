# Migration Guide: v2.x to v3.x

Imports, core method names (`chat.complete`, `embeddings.create`, `files.upload`, ...) and the Python minimum (`>=3.10`) are unchanged. The breaking changes are the HTTP transport and a handful of beta and workflow APIs.

## HTTPX2 and MCP 2.2

The SDK depends on `httpx2` instead of `httpx`, and the `agents` extra on `mcp>=2.2,<3`. This also applies to `MistralAzure` and `MistralGCP`.

- A custom HTTP client must be the HTTPX2 equivalent:

  ```python
  import httpx2
  from mistralai.client import Mistral

  client = Mistral(
      api_key="...",
      client=httpx2.Client(timeout=60),
      async_client=httpx2.AsyncClient(timeout=60),
  )
  ```

- Raw requests and responses exposed on results and errors are `httpx2` types; catch `httpx2` exceptions instead of `httpx` ones.
- `mistral.beta.connectors.http_client()` returns an `httpx2.AsyncClient`.
- MCP results use MCP 2.2 field names, e.g. `structured_content` instead of `structuredContent`.

## Chat and Agents Completions

`chat.complete`, `chat.stream`, `agents.complete` and `agents.stream` no longer accept the `web_search`, `web_search_premium` and `code_interpreter` tools. Use them through the Conversations API (`beta.conversations`) or an agent created with `beta.agents.create`, where `WebSearchTool`, `WebSearchPremiumTool` and `CodeInterpreterTool` remain available.

## Connectors (beta)

The three credential deletions are one method with a scope:

| v2 | v3 |
|---|---|
| `beta.connectors.delete_user_credentials(...)` | `beta.connectors.delete_credentials(..., consumer_scope="user")` |
| `beta.connectors.delete_workspace_credentials(...)` | `beta.connectors.delete_credentials(..., consumer_scope="workspace")` |
| `beta.connectors.delete_organization_credentials(...)` | `beta.connectors.delete_credentials(..., consumer_scope="organization")` |

The `ConnectorDelete{User,Workspace,Organization}CredentialsV1Request` models are replaced by `ConnectorDeleteCredentialsRequest`.

- `beta.connectors.get()`: `fetch_customer_data` removed.
- `beta.connectors.list_tools()`: `page` removed; all tools are returned in one response.
- `beta.connectors.list()`: `query_filters.active` removed.

## Observability Pipeline Configs (beta)

A pipeline config holds a single definition:

| v2 | v3 |
|---|---|
| `create_pipeline_config(..., definitions=[d])` | `create_pipeline_config(..., definition=d)` |
| `update_pipeline_config(..., definitions=[d])` | `update_pipeline_config(..., definition=d)` |
| `config.definitions[0]` | `config.definition` |

`PipelineConfig.definitions` is still returned, as `[definition]`, but is now optional.

## Workflow Deployments

- The `koyeb` backend is now Mistral Cloud: `DeploymentKoyebBackendSpec` is replaced by `DeploymentMistralCloudBackendSpec` (`type="mistral_cloud"`). Requests accept only this backend; the Kubernetes backend can no longer be set.
- `DeploymentResourceConfig` and `DeploymentResourceConfigUpdate` keep only `replicas`; `cpu_request`, `cpu_limit`, `memory_request` and `memory_limit` are removed.
- `entrypoint` and `working_dir` are removed from `DeploymentWorkerSpecInput` and `WorkflowsWorkerSpecUpdate`, and together with `commit_sha` from `DeploymentWorkerSpecResponse`.
- `UnknownDeploymentWorkerSpecResponseBackendSpec` is renamed `UnknownBackendSpec`.

## Users (beta)

`beta.users.get_identity()`, `list_organizations()` and `list_workspaces()` accept either an API key or a bearer token, so both fields of their security models are optional. Set one of them; passing neither is rejected with a 401:

```python
import os
from mistralai.client import Mistral, models

with Mistral() as mistral:
    res = mistral.beta.users.get_identity(
        security=models.UsersAPIGetIdentitySecurity(
            dashboard_user_context_auth=os.environ["MISTRAL_API_KEY"],
        )
    )
```

---

# Migration Guide: v1.x to v2.x

## Import Changes

All SDK imports move from `mistralai` to `mistralai.client`:

| v1 | v2 |
|---|---|
| `from mistralai import Mistral` | `from mistralai.client import Mistral` |
| `from mistralai.models import ...` | `from mistralai.client.models import ...` |
| `from mistralai.types import ...` | `from mistralai.client.types import ...` |
| `from mistralai.utils import ...` | `from mistralai.client.utils import ...` |

`mistralai.extra` is unchanged (`RunContext`, `MCPClientSTDIO`, `MCPClientSSE`, `response_format_from_pydantic_model`, etc. stay at `mistralai.extra`).

## Azure & GCP

Azure and GCP are now namespace sub-packages under `mistralai`, no longer separate top-level packages.

| v1 | v2 |
|---|---|
| `from mistralai_azure import MistralAzure` | `from mistralai.azure.client import MistralAzure` |
| `from mistralai_azure.models import ...` | `from mistralai.azure.client.models import ...` |
| `from mistralai_gcp import MistralGoogleCloud` | `from mistralai.gcp.client import MistralGCP` |
| `from mistralai_gcp.models import ...` | `from mistralai.gcp.client.models import ...` |
GCP class renamed `MistralGoogleCloud` -> `MistralGCP`.

## Type Renames

42 request/response types renamed to follow `{Verb}{Entity}Request` / `{Verb}{Entity}Response` / `{Entity}` conventions. Core types (`Mistral`, `UserMessage`, `AssistantMessage`, `File`, `FunctionTool`, `ResponseFormat`, etc.) keep the same name — just different import path.

Only one user-facing type rename: `Tools` -> `ConversationRequestTool`.

<details>
<summary>Full rename table (42 schemas)</summary>

| v1 | v2 |
|---|---|
| `AgentCreationRequest` | `CreateAgentRequest` |
| `AgentUpdateRequest` | `UpdateAgentRequest` |
| `ArchiveFTModelOut` | `ArchiveModelResponse` |
| `BatchJobIn` | `CreateBatchJobRequest` |
| `BatchJobOut` | `BatchJob` |
| `BatchJobsOut` | `ListBatchJobsResponse` |
| `CheckpointOut` | `Checkpoint` |
| `ClassifierDetailedJobOut` | `ClassifierFineTuningJobDetails` |
| `ClassifierFTModelOut` | `ClassifierFineTunedModel` |
| `ClassifierJobOut` | `ClassifierFineTuningJob` |
| `ClassifierTargetIn` | `ClassifierTarget` |
| `ClassifierTargetOut` | `ClassifierTargetResult` |
| `ClassifierTrainingParametersIn` | `ClassifierTrainingParameters` |
| `CompletionDetailedJobOut` | `CompletionFineTuningJobDetails` |
| `CompletionFTModelOut` | `CompletionFineTunedModel` |
| `CompletionJobOut` | `CompletionFineTuningJob` |
| `CompletionTrainingParametersIn` | `CompletionTrainingParameters` |
| `ConversationAppendRequestBase` | `AppendConversationRequest` |
| `ConversationRestartRequestBase` | `RestartConversationRequest` |
| `DeleteFileOut` | `DeleteFileResponse` |
| `DocumentOut` | `Document` |
| `DocumentUpdateIn` | `UpdateDocumentRequest` |
| `EventOut` | `Event` |
| `FTModelCapabilitiesOut` | `FineTunedModelCapabilities` |
| `FileSignedURL` | `GetSignedUrlResponse` |
| `GithubRepositoryOut` | `GithubRepository` |
| `JobIn` | `CreateFineTuningJobRequest` |
| `JobMetadataOut` | `JobMetadata` |
| `JobsOut` | `ListFineTuningJobsResponse` |
| `LegacyJobMetadataOut` | `LegacyJobMetadata` |
| `LibraryIn` | `CreateLibraryRequest` |
| `LibraryInUpdate` | `UpdateLibraryRequest` |
| `LibraryOut` | `Library` |
| `ListDocumentOut` | `ListDocumentsResponse` |
| `ListFilesOut` | `ListFilesResponse` |
| `ListLibraryOut` | `ListLibrariesResponse` |
| `MetricOut` | `Metric` |
| `RetrieveFileOut` | `RetrieveFileResponse` |
| `UnarchiveFTModelOut` | `UnarchiveModelResponse` |
| `UpdateFTModelIn` | `UpdateModelRequest` |
| `UploadFileOut` | `UploadFileResponse` |
| `WandbIntegrationOut` | `WandbIntegrationResult` |

</details>

## Other Changes

- `FunctionTool.type` changed from `Optional[FunctionToolType]` to `Literal["function"]` (functionally equivalent if you omit `type`)
- Enums now accept unknown values for forward compatibility with API changes
- Forward-compatible unions: discriminated unions get an `Unknown` variant

## What Did NOT Change

- All method names (`chat.complete`, `chat.stream`, `embeddings.create`, `fim.complete`, `files.upload`, `models.list`, `fine_tuning.jobs.create`, etc.)
- Zero endpoints added/removed, zero path changes
- Python minimum `>=3.10`
- Installation: `pip install mistralai`

---

<details>
<summary><h1>Legacy: Migrating from v0.x to v1.x</h1></summary>

> **Note:** The v1.x examples below use v1-style imports (e.g., `from mistralai import Mistral`). If you're on v2.x, combine these API changes with the [v1 to v2 import changes](#migration-guide-v1x-to-v2x) above.

`MistralClient`/`MistralAsyncClient` consolidated into `Mistral`. `ChatMessage` replaced with `UserMessage`, `AssistantMessage`, etc. Streaming chunks now at `chunk.data.choices[0].delta.content`.

| v0.x | v1.x |
|---|---|
| `MistralClient` | `Mistral` |
| `client.chat` | `client.chat.complete` |
| `client.chat_stream` | `client.chat.stream` |
| `client.completions` | `client.fim.complete` |
| `client.completions_stream` | `client.fim.stream` |
| `client.embeddings` | `client.embeddings.create` |
| `client.list_models` | `client.models.list` |
| `client.delete_model` | `client.models.delete` |
| `client.files.create` | `client.files.upload` |
| `client.jobs.create` | `client.fine_tuning.jobs.create` |
| `client.jobs.list` | `client.fine_tuning.jobs.list` |
| `client.jobs.retrieve` | `client.fine_tuning.jobs.get` |
| `client.jobs.cancel` | `client.fine_tuning.jobs.cancel` |

</details>
