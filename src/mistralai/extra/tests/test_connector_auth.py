import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import httpx2 as httpx
import pytest

from mistralai.client import Mistral
from mistralai.extra.workflows import connector_auth
from mistralai.extra.workflows.connector_auth import (
    ConnectorAuthTaskState,
    execute_with_connector_auth_async,
)

ROOT_ID = "root-exec"
CHILD_A_ID = "child-a-exec"
CHILD_B_ID = "child-b-exec"


def _event(
    event_type: str,
    workflow_exec_id: str,
    attributes: dict[str, Any],
) -> dict[str, Any]:
    is_root = workflow_exec_id == ROOT_ID
    return {
        "event_id": f"{event_type}-{workflow_exec_id}",
        "event_timestamp": 0,
        "root_workflow_exec_id": ROOT_ID,
        "parent_workflow_exec_id": None if is_root else ROOT_ID,
        "workflow_exec_id": workflow_exec_id,
        "workflow_run_id": f"{workflow_exec_id}-run",
        "workflow_name": "root-wf" if is_root else "child-wf",
        "attributes": attributes,
        "event_type": event_type,
    }


def _completed(workflow_exec_id: str) -> dict[str, Any]:
    return _event(
        "WORKFLOW_EXECUTION_COMPLETED",
        workflow_exec_id,
        {"task_id": "t", "result": {"type": "json", "value": None}},
    )


def _failed(workflow_exec_id: str) -> dict[str, Any]:
    return _event(
        "WORKFLOW_EXECUTION_FAILED",
        workflow_exec_id,
        {"task_id": "t", "failure": {"message": "boom"}},
    )


def _canceled(workflow_exec_id: str) -> dict[str, Any]:
    return _event(
        "WORKFLOW_EXECUTION_CANCELED",
        workflow_exec_id,
        {"task_id": "t", "reason": "canceled"},
    )


def _auth_requested(workflow_exec_id: str, connector_name: str) -> dict[str, Any]:
    return _event(
        "CUSTOM_TASK_STARTED",
        workflow_exec_id,
        {
            "custom_task_id": f"auth-{connector_name}",
            "custom_task_type": "connector_auth",
            "payload": {
                "type": "json",
                "value": {
                    "connector_name": connector_name,
                    "connector_id": f"{connector_name}-id",
                    "auth_url": f"https://auth.example.test/{connector_name}",
                },
            },
        },
    )


class _FakeWorkflowsServer:
    """Serves a fixed event log for ROOT_ID, replaying from ``start_seq``.

    Each stream request returns every remaining event and then closes, like a
    server whose connection drops after the last available event.
    """

    def __init__(self, events: list[dict[str, Any]]) -> None:
        self.events = events
        self.stream_start_seqs: list[int] = []

    def _sse_body(self, start_seq: int) -> bytes:
        frames = []
        for seq, event in enumerate(self.events):
            if seq < start_seq:
                continue
            payload = {
                "stream": "workflows",
                "data": event,
                "workflow_context": {
                    "namespace": "default",
                    "workflow_name": event["workflow_name"],
                    "workflow_exec_id": event["workflow_exec_id"],
                    "root_workflow_exec_id": ROOT_ID,
                },
                "broker_sequence": seq,
            }
            frames.append(f"event: workflow.event\ndata: {json.dumps(payload)}\n\n")
        return "".join(frames).encode()

    def _execution(self, status: str) -> dict[str, Any]:
        return {
            "workflow_name": "root-wf",
            "execution_id": ROOT_ID,
            "root_execution_id": ROOT_ID,
            "status": status,
            "start_time": "2026-01-01T00:00:00Z",
            "end_time": None,
            "result": None,
        }

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "POST" and path == "/v1/workflows/root-wf/execute":
            return httpx.Response(200, json=self._execution("RUNNING"))
        if path == "/v1/workflows/events/stream":
            start_seq = int(request.url.params.get("start_seq", "0"))
            self.stream_start_seqs.append(start_seq)
            return httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=self._sse_body(start_seq),
            )
        if path == f"/v1/workflows/executions/{ROOT_ID}":
            return httpx.Response(200, json=self._execution("COMPLETED"))
        return httpx.Response(404, json={"detail": f"unexpected {path}"})


@asynccontextmanager
async def _mistral_client(server: _FakeWorkflowsServer) -> AsyncIterator[Mistral]:
    async_client = httpx.AsyncClient(transport=httpx.MockTransport(server.handle))
    try:
        yield Mistral(
            api_key="test-api-key",
            server_url="https://api.example.test",
            async_client=async_client,
        )
    finally:
        await async_client.aclose()


@pytest.fixture(autouse=True)
def _no_reconnect_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    async def no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(connector_auth.asyncio, "sleep", no_sleep)


async def _run(server: _FakeWorkflowsServer) -> list[ConnectorAuthTaskState]:
    auth_requests: list[ConnectorAuthTaskState] = []

    async def on_auth_required(state: ConnectorAuthTaskState) -> None:
        auth_requests.append(state)

    async with _mistral_client(server) as client:
        result = await execute_with_connector_auth_async(
            client,
            workflow_identifier="root-wf",
            on_auth_required=on_auth_required,
            polling_interval=0,
            max_polling_attempts=1,
        )
    assert result.status == "COMPLETED"
    return auth_requests


@pytest.mark.asyncio
@pytest.mark.parametrize("child_end_event", [_completed, _failed, _canceled])
async def test_child_end_event_does_not_stop_auth_handling(child_end_event) -> None:
    # Child A ends before child B starts and asks for OAuth.
    server = _FakeWorkflowsServer(
        [
            child_end_event(CHILD_A_ID),
            _auth_requested(CHILD_B_ID, "gmail"),
            _completed(CHILD_B_ID),
            _completed(ROOT_ID),
        ]
    )

    auth_requests = await _run(server)

    assert [state.connector_name for state in auth_requests] == ["gmail"]
    assert auth_requests[0].auth_url == "https://auth.example.test/gmail"
    assert server.stream_start_seqs == [0]


@pytest.mark.asyncio
async def test_handles_auth_from_root_and_children() -> None:
    server = _FakeWorkflowsServer(
        [
            _auth_requested(ROOT_ID, "slack"),
            _auth_requested(CHILD_A_ID, "drive"),
            _completed(CHILD_A_ID),
            _auth_requested(CHILD_B_ID, "gmail"),
            _failed(CHILD_B_ID),
            _completed(ROOT_ID),
        ]
    )

    auth_requests = await _run(server)

    assert [state.connector_name for state in auth_requests] == [
        "slack",
        "drive",
        "gmail",
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("root_end_event", [_completed, _failed, _canceled])
async def test_root_end_event_stops_streaming(root_end_event) -> None:
    # Anything after the root's end event must not be read.
    server = _FakeWorkflowsServer(
        [
            root_end_event(ROOT_ID),
            _auth_requested(CHILD_B_ID, "gmail"),
        ]
    )

    auth_requests = await _run(server)

    assert auth_requests == []
    assert server.stream_start_seqs == [0]


@pytest.mark.asyncio
async def test_reconnects_after_child_end_event_without_root_end() -> None:
    # The connection drops right after a child's end event: the client must
    # resume from the next sequence rather than treat the run as finished.
    server = _FakeWorkflowsServer([_completed(CHILD_A_ID)])
    original_handle = server.handle

    def handle(request: httpx.Request) -> httpx.Response:
        if len(server.stream_start_seqs) == 1:
            server.events.extend(
                [_auth_requested(CHILD_B_ID, "gmail"), _completed(ROOT_ID)]
            )
        return original_handle(request)

    server.handle = handle  # type: ignore[method-assign]

    auth_requests = await _run(server)

    assert [state.connector_name for state in auth_requests] == ["gmail"]
    assert server.stream_start_seqs == [0, 1]
