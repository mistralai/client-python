"""Reusable helpers for running connector-backed workflows.

Provides:

- :func:`on_auth_required` — default callback that opens the browser for OAuth.
- :func:`build_connector_extensions` — builds the ``extensions`` dict from
  :class:`ConnectorSlot` instances.
- :func:`run_workflow_with_connectors` — high-level convenience that wires up a
  :class:`Mistral` client, calls
  :func:`execute_with_connector_auth_async`, and logs the result.
"""

from __future__ import annotations

import logging
import webbrowser
from typing import Any, Dict, Optional, Sequence

import pydantic

from .connector_auth import (
    ConnectorAuthTaskState,
    ConnectorBindings,
    ConnectorExtensions,
    WorkflowExtensions,
    execute_with_connector_auth_async,
)
from .connector_slot import ConnectorSlot

logger = logging.getLogger(__name__)


async def on_auth_required(state: ConnectorAuthTaskState) -> None:
    """Default callback: opens the OAuth URL in the browser and waits."""
    if state.auth_url:
        logger.info(
            "Auth required — opening browser (connector=%s, auth_url=%s)",
            state.connector_name,
            state.auth_url,
        )
        webbrowser.open(state.auth_url)
    else:
        logger.info(
            "Auth required — authenticate the connector manually (connector=%s)",
            state.connector_name,
        )
    input("Press Enter after completing the OAuth flow...")


def build_connector_extensions(
    connectors: Sequence[ConnectorSlot],
) -> Dict[str, Any]:
    """Build an extensions dict from :class:`ConnectorSlot` instances.

    The resulting dict is forwarded via ``execute_workflow_async(extensions=…)``
    and lands in ``WorkflowContext.extensions`` where the connector plugin
    reads it.
    """
    ext = WorkflowExtensions(
        mistralai=ConnectorExtensions(
            connectors=ConnectorBindings(
                bindings=list(connectors),
            ),
        ),
    )
    return ext.model_dump(mode="json", exclude_none=True)


async def run_workflow_with_connectors(
    workflow_name: str,
    input_data: pydantic.BaseModel,
    *,
    api_key: str,
    server_url: str,
    task_queue: Optional[str] = None,
    connectors: Sequence[ConnectorSlot] = (),
) -> None:
    """Execute a workflow, handling connector auth automatically."""
    from mistralai.client.sdk import Mistral

    extensions = build_connector_extensions(connectors) if connectors else None

    async with Mistral(api_key=api_key, server_url=server_url) as client:
        result = await execute_with_connector_auth_async(
            client,
            workflow_identifier=workflow_name,
            input_data=input_data,
            on_auth_required=on_auth_required,
            task_queue=task_queue,
            extensions=extensions,
        )
        logger.info(
            "Workflow completed (status=%s, result=%s)",
            result.status,
            result.result,
        )
