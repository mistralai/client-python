"""Tests for agents.stream() and agents.stream_async()."""

import json
from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

_STREAM_CHUNK_TEMPLATE: dict[str, Any] = {
    "id": "stream-001",
    "object": "chat.completion.chunk",
    "model": "mistral-small-latest",
    "created": 1700000000,
}


def _make_stream_chunk(
    content: str = "",
    finish_reason: str | None = None,
    index: int = 0,
) -> dict[str, Any]:
    delta: dict[str, Any] = {"role": "assistant"}
    if content:
        delta["content"] = content
    choice: dict[str, Any] = {"index": index, "delta": delta, "finish_reason": finish_reason}
    return {**_STREAM_CHUNK_TEMPLATE, "choices": [choice]}


def _make_sse_body(
    events: list[dict[str, Any]],
    sentinel: str = "[DONE]",
) -> bytes:
    lines = [f"data: {json.dumps(e)}\n\n" for e in events]
    lines.append(f"data: {sentinel}\n\n")
    return "".join(lines).encode()


def _user_msg(content: str = "Hello") -> list[dict[str, str]]:
    return [{"role": "user", "content": content}]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAgentsStreamYieldsEvents:
    def test_agents_stream_yields_events(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.agents.stream(
            agent_id="agent-123", messages=_user_msg()
        )
        events = list(stream)

        assert len(events) >= 1


class TestAgentsStreamAsync:
    @pytest.mark.asyncio
    async def test_agents_stream_async(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.agents.stream_async(
            agent_id="agent-123", messages=_user_msg()
        )
        events = [event async for event in stream]

        assert len(events) >= 1


class TestAgentsStreamWithAgentId:
    def test_agents_stream_with_agent_id(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        route = mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.agents.stream(
            agent_id="agent-456", messages=_user_msg()
        )
        # Consume the stream to ensure the request is sent
        list(stream)

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["agent_id"] == "agent-456"
