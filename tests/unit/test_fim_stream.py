"""Tests for fim.stream() and fim.stream_async()."""

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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFimStreamYieldsEvents:
    def test_fim_stream_yields_events(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.fim.stream(
            model="codestral-latest", prompt="def hello():"
        )
        events = list(stream)

        assert len(events) >= 1


class TestFimStreamAsync:
    @pytest.mark.asyncio
    async def test_fim_stream_async(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.fim.stream_async(
            model="codestral-latest", prompt="def hello():"
        )
        events = [event async for event in stream]

        assert len(events) >= 1


class TestFimStreamWithSuffix:
    def test_fim_stream_with_suffix(self, mock_router, mistral_client):
        chunks = [
            _make_stream_chunk("Hi"),
            _make_stream_chunk("", finish_reason="stop"),
        ]
        route = mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(
                200,
                content=_make_sse_body(chunks),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.fim.stream(
            model="codestral-latest",
            prompt="def hello():",
            suffix="    return 'hello'",
        )
        # Consume the stream to trigger the request
        list(stream)

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["suffix"] == "    return 'hello'"
