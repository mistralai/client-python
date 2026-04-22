"""Helper for executing workflows that require connector OAuth authentication.

When a workflow uses connectors that need OAuth, it emits ``connector-auth``
custom task events.  This module provides a high-level async function that
automates the handshake:

1. Start the workflow execution.
2. Stream events, watching for ``connector-auth`` custom task events.
3. When a ``waiting_for_auth`` event arrives, invoke a user-supplied callback.
4. The interceptor polls for credentials server-side and resumes automatically.
5. Return the final execution result once the workflow completes.

Example::

    from mistralai import Mistral
    from mistralai.extra.workflows import (
        ConnectorAuthTaskState,
        ConnectorSlot,
        execute_with_connector_auth_async,
    )

    async def prompt_user(state: ConnectorAuthTaskState) -> None:
        print(f"Please authenticate: {state.auth_url}")
        input("Press Enter when done...")

    gmail = ConnectorSlot(connector_name="gmail")

    client = Mistral(api_key="...")
    result = await execute_with_connector_auth_async(
        client,
        workflow_identifier="my-workflow",
        input_data={"query": "summarize my emails"},
        on_auth_required=prompt_user,
        connectors=[gmail],
    )
"""

from __future__ import annotations

import asyncio
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
)

import httpx
from pydantic import BaseModel

from mistralai.client.models import (
    CustomTaskStartedResponse,
    WorkflowExecutionCanceledResponse,
    WorkflowExecutionCompletedResponse,
    WorkflowExecutionFailedResponse,
    WorkflowExecutionResponse,
)

from .connector_slot import ConnectorSlot

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral

logger = logging.getLogger(__name__)

_TERMINAL_EVENT_TYPES = (
    WorkflowExecutionCompletedResponse,
    WorkflowExecutionFailedResponse,
    WorkflowExecutionCanceledResponse,
)

_MAX_RECONNECT_ATTEMPTS = 10


class ConnectorAuthTaskState(BaseModel):
    """State emitted by a ``connector-auth`` custom task when it needs OAuth.

    Attributes:
        connector_name: Identifier of the connector requiring authentication.
        status: Current state of the auth flow.
        auth_url: URL the user should visit to complete authentication.
        message: Optional human-readable context about the auth request.
    """

    connector_name: str
    connector_id: str
    status: Literal[
        "waiting_for_auth",
        "connected",
        "access_denied",
        "timed_out",
        "error",
    ]
    auth_url: Optional[str] = None
    message: Optional[str] = None


class ConnectorBindings(BaseModel):
    """Connector bindings passed within extensions."""

    bindings: List[ConnectorSlot]


class ConnectorExtensions(BaseModel):
    """The ``mistralai`` key within workflow extensions."""

    connectors: ConnectorBindings


class WorkflowExtensions(BaseModel):
    """Top-level extensions dict forwarded to ``execute_workflow_async``."""

    mistralai: ConnectorExtensions


async def execute_with_connector_auth_async(
    client: Mistral,
    workflow_identifier: str,
    input_data: Any = None,
    *,
    on_auth_required: Optional[
        Callable[[ConnectorAuthTaskState], Awaitable[None]]
    ] = None,
    execution_id: Optional[str] = None,
    task_queue: Optional[str] = None,
    deployment_name: Optional[str] = None,
    connectors: Sequence[ConnectorSlot] = (),
    extensions: Optional[Dict[str, Any]] = None,
    polling_interval: float = 2,
    max_polling_attempts: Optional[int] = None,
) -> WorkflowExecutionResponse:
    """Execute a workflow, automatically handling connector OAuth flows.

    Args:
        client: An initialised :class:`Mistral` client.
        workflow_identifier: Name or ID of the workflow to execute.
        input_data: Input payload for the workflow.  Pydantic models are
            serialised via ``model_dump(mode="json")``.
        on_auth_required: Async callback invoked when a connector needs
            the user to authenticate.  Receives a
            :class:`ConnectorAuthTaskState` whose ``auth_url`` field
            contains the OAuth URL.  The workflow resumes automatically
            after this callback returns.
        execution_id: Optional custom execution ID.
        task_queue: Optional task queue name (deprecated upstream).
        deployment_name: Optional deployment target.
        connectors: Typed connector slots that declare which connectors
            the workflow needs.  Converted to the ``extensions`` dict
            automatically.
        extensions: Additional plugin-specific data to propagate into
            ``WorkflowContext.extensions`` at execution time.  Merged
            with connector bindings from *connectors*.
        polling_interval: Seconds between status polls after the event
            stream ends.
        max_polling_attempts: Maximum number of polling iterations before
            raising :class:`TimeoutError`.  ``None`` means poll forever.

    Returns:
        The completed :class:`WorkflowExecutionResponse`.

    Raises:
        RuntimeError: If the workflow finishes with a non-COMPLETED status.
        TimeoutError: If *max_polling_attempts* is set and exceeded.
    """
    input_dict = _serialize_input(input_data)

    merged_extensions = _build_extensions(connectors, extensions)

    execute_kwargs: Dict[str, Any] = dict(
        workflow_identifier=workflow_identifier,
        input_=input_dict,
        execution_id=execution_id,
        task_queue=task_queue,
        deployment_name=deployment_name,
    )
    if merged_extensions is not None:
        execute_kwargs["extensions"] = merged_extensions

    execution = await client.workflows.execute_workflow_async(**execute_kwargs)
    exec_id = execution.execution_id

    await _stream_and_handle_auth(client, exec_id, on_auth_required)

    return await _poll_until_done(
        client, exec_id, polling_interval, max_polling_attempts
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _serialize_input(input_data: Any) -> Optional[Dict[str, Any]]:
    if input_data is None:
        return None
    if hasattr(input_data, "model_dump"):
        return input_data.model_dump(mode="json")
    return input_data


def _build_extensions(
    connectors: Sequence[ConnectorSlot],
    extra: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Merge connector slot bindings with any additional extensions."""
    if not connectors and not extra:
        return None

    result: Dict[str, Any] = dict(extra) if extra else {}
    if connectors:
        ext = WorkflowExtensions(
            mistralai=ConnectorExtensions(
                connectors=ConnectorBindings(
                    bindings=list(connectors),
                ),
            ),
        )
        ext_dict = ext.model_dump(mode="json", exclude_none=True)
        # Merge: connector bindings go under result["mistralai"]["connectors"]
        mistralai = result.setdefault("mistralai", {})
        existing_bindings = mistralai.get("connectors", {}).get("bindings", [])
        new_bindings = ext_dict["mistralai"]["connectors"]["bindings"]
        mistralai["connectors"] = {"bindings": existing_bindings + new_bindings}
    return result


async def _stream_and_handle_auth(
    client: Mistral,
    exec_id: str,
    on_auth_required: Optional[Callable[[ConnectorAuthTaskState], Awaitable[None]]],
) -> None:
    """Stream workflow events, handling connector-auth tasks.

    Reconnects automatically with exponential back-off when the SSE
    connection drops.
    """
    last_seq = 0

    for attempt in range(_MAX_RECONNECT_ATTEMPTS):
        try:
            event_stream = await client.workflows.events.get_stream_events_async(
                root_workflow_exec_id=exec_id,
                workflow_exec_id="*",
                parent_workflow_exec_id="*",
                start_seq=last_seq,
            )
            async with event_stream:
                async for sse_event in event_stream:
                    if sse_event.data is None:
                        continue

                    payload = sse_event.data
                    last_seq = payload.broker_sequence + 1
                    event = payload.data

                    if isinstance(event, _TERMINAL_EVENT_TYPES):
                        return

                    if not isinstance(event, CustomTaskStartedResponse):
                        continue
                    if event.attributes.custom_task_type != "connector-auth":
                        continue

                    payload_value = (
                        event.attributes.payload.value
                        if event.attributes.payload is not None
                        else None
                    )
                    if (
                        not isinstance(payload_value, dict)
                        or payload_value.get("status") != "waiting_for_auth"
                    ):
                        continue

                    state = ConnectorAuthTaskState.model_validate(payload_value)

                    if on_auth_required:
                        await on_auth_required(state)

                    # The interceptor polls for credentials server-side —
                    # no signal or update needed from the client.
                else:
                    # Stream exhausted without a terminal event — retry.
                    continue
            # Terminal event received.
            return
        except (ConnectionError, httpx.RemoteProtocolError):
            logger.debug(
                "Event stream connection lost, reconnecting "
                "(execution_id=%s, attempt=%d)",
                exec_id,
                attempt,
            )
            await asyncio.sleep(min(2**attempt, 30))


async def _poll_until_done(
    client: Mistral,
    exec_id: str,
    polling_interval: float,
    max_attempts: Optional[int],
) -> WorkflowExecutionResponse:
    """Poll the execution status until it reaches a terminal state."""
    attempts = 0
    while True:
        result = await client.workflows.executions.get_workflow_execution_async(
            execution_id=exec_id,
        )
        if result.status != "RUNNING":
            if result.status == "COMPLETED":
                return result
            raise RuntimeError(f"Workflow failed with status: {result.status}")

        attempts += 1
        if max_attempts is not None and attempts >= max_attempts:
            raise TimeoutError(
                f"Workflow still running after {max_attempts} polling attempts"
            )
        await asyncio.sleep(polling_interval)
