import uuid
from typing import TYPE_CHECKING

from .config import WorkflowEncodingConfig

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


def generate_two_part_id(
    primary_seed: str | None = None, secondary_seed: str | None = None
) -> str:
    """Generates a unique ID composed of two parts derived from seeds."""
    if not primary_seed:
        primary_seed = uuid.uuid4().hex
    if not secondary_seed:
        secondary_seed = uuid.uuid4().hex
    first_part = uuid.uuid5(uuid.NAMESPACE_DNS, primary_seed).hex
    second_part = uuid.uuid5(uuid.NAMESPACE_DNS, secondary_seed).hex
    return f"{first_part}{second_part}".replace("-", "")


async def configure_workflow_encoding(
    config: WorkflowEncodingConfig,
    *,
    client: "Mistral",
    namespace: str | None = None,
) -> None:
    """Configure workflow payload encoding for the SDK.

    This enables encryption and/or blob storage offloading for workflow payloads.

    Args:
        config: The workflow encoding configuration.
        client: The Mistral client instance.
        namespace: The workflow namespace. If not provided, it will be fetched
            from the scheduler using the client.
    """
    from mistralai.client._hooks.workflow_encoding_hook import (
        configure_workflow_encoding as _configure_workflow_encoding,
    )

    if not namespace:
        from mistralai.extra.workflows.helpers import get_scheduler_namespace

        namespace = await get_scheduler_namespace(client)
    _configure_workflow_encoding(config, namespace, client.sdk_configuration)
