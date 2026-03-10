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
