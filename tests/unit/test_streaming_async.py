"""Tests for asynchronous streaming: chat.stream_async(), agents.stream_async(), fim.stream_async()."""

import json

import httpx
import pytest

from mistralai.client import models
from mistralai.client.errors import HTTPValidationError, SDKError
from mistralai.client.utils.eventstreaming import EventStreamAsync

from .conftest import (
    VALIDATION_ERROR_RESPONSE,
    make_sse_body,
    make_stream_chunk,
    user_msg,
)


class TestChatStreamAsyncYieldsEvents:
    @pytest.mark.asyncio
    async def test_chat_stream_async_yields_events(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Hello"),
            make_stream_chunk(" world", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = await mistral_client.chat.stream_async(model="m", messages=user_msg())
        results = []
        async for event in stream:
            results.append(event)

        assert len(results) == 2
        assert isinstance(results[0], models.CompletionEvent)
        assert results[0].data.choices[0].delta.content == "Hello"
        assert results[1].data.choices[0].delta.content == " world"


class TestAgentsStreamAsyncYieldsEvents:
    @pytest.mark.asyncio
    async def test_agents_stream_async_yields_events(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Agent async"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = await mistral_client.agents.stream_async(
            agent_id="agent-001", messages=user_msg()
        )
        results = []
        async for event in stream:
            results.append(event)

        assert len(results) == 2
        assert results[0].data.choices[0].delta.content == "Agent async"


class TestFimStreamAsyncYieldsEvents:
    @pytest.mark.asyncio
    async def test_fim_stream_async_yields_events(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("def hello():"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = await mistral_client.fim.stream_async(
            model="codestral-latest", prompt="def "
        )
        results = []
        async for event in stream:
            results.append(event)

        assert len(results) == 2
        assert results[0].data.choices[0].delta.content == "def hello():"


class TestStreamAsyncContextManager:
    @pytest.mark.asyncio
    async def test_stream_async_context_manager(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Hello"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        collected = []
        stream = await mistral_client.chat.stream_async(model="m", messages=user_msg())
        async with stream as s:
            assert isinstance(s, EventStreamAsync)
            async for event in s:
                collected.append(event)

        assert len(collected) == 2


class TestStreamAsync422Error:
    @pytest.mark.asyncio
    async def test_stream_async_422_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=VALIDATION_ERROR_RESPONSE,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(HTTPValidationError) as exc_info:
            await mistral_client.chat.stream_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 422
        assert exc_info.value.data.detail is not None


class TestStreamAsync500Error:
    @pytest.mark.asyncio
    async def test_stream_async_500_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                500,
                text="Internal Server Error",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            await mistral_client.chat.stream_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 500


class TestEmptyDataLinesIgnoredAsync:
    @pytest.mark.asyncio
    async def test_empty_data_lines_ignored_async(self, mock_router, mistral_client):
        """SSE body with extra blank lines between events should not break async parsing."""
        chunk = make_stream_chunk("content", finish_reason="stop")
        raw = (
            "\n\n"  # leading blank lines
            f"data: {json.dumps(chunk)}\n\n"
            "\n\n"  # extra blank lines
            "data: [DONE]\n\n"
        )
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=raw.encode(),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.chat.stream_async(model="m", messages=user_msg())
        results = []
        async for event in stream:
            results.append(event)

        assert len(results) == 1
        assert results[0].data.choices[0].delta.content == "content"
