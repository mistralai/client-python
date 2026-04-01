from typing import TYPE_CHECKING, overload

from .config import WorkflowEncodingConfig

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


@overload
async def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    *,
    namespace: str,
) -> None: ...


@overload
async def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    *,
    client: "Mistral",
) -> None: ...


async def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    *,
    client: "Mistral | None" = None,
    namespace: str | None = None,
) -> None:
    """Configure workflow payload encoding for the SDK.

    This enables encryption and/or blob storage offloading for workflow payloads.

    Args:
        config: The workflow encoding configuration.
        client: The Mistral client instance. Required if namespace is not provided.
        namespace: The workflow namespace. If not provided, it will be fetched
            from the scheduler using the client.
    """
    from mistralai.client._hooks.workflow_encoding_hook import (
        configure_workflow_encoding as _configure_workflow_encoding,
    )

    if not namespace:
        if not client:
            raise ValueError("client is required when namespace is not provided")
        from mistralai.extra.workflows.helpers import get_scheduler_namespace

        namespace = await get_scheduler_namespace(client)
    _configure_workflow_encoding(config, namespace)
