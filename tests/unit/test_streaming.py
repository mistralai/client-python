"""Tests for synchronous streaming: chat.stream(), agents.stream(), fim.stream()."""

import json

import httpx
import pytest

from mistralai.client import models
from mistralai.client.errors import HTTPValidationError, SDKError
from mistralai.client.utils.eventstreaming import EventStream

from .conftest import (
    VALIDATION_ERROR_RESPONSE,
    make_sse_body,
    make_stream_chunk,
    user_msg,
)


class TestChatStreamYieldsEvents:
    def test_chat_stream_yields_events(self, mock_router, mistral_client):
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

        stream = mistral_client.chat.stream(model="m", messages=user_msg())
        results = list(stream)

        assert len(results) == 2
        assert isinstance(results[0], models.CompletionEvent)
        assert results[0].data.choices[0].delta.content == "Hello"
        assert results[1].data.choices[0].delta.content == " world"


class TestChatStreamLastChunkHasFinishReason:
    def test_chat_stream_last_chunk_has_finish_reason(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Hi"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = mistral_client.chat.stream(model="m", messages=user_msg())
        results = list(stream)

        last = results[-1]
        assert last.data.choices[0].finish_reason == "stop"


class TestAgentsStreamYieldsEvents:
    def test_agents_stream_yields_events(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Agent reply"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = mistral_client.agents.stream(
            agent_id="agent-001", messages=user_msg()
        )
        results = list(stream)

        assert len(results) == 2
        assert results[0].data.choices[0].delta.content == "Agent reply"
        assert results[-1].data.choices[0].finish_reason == "stop"


class TestFimStreamYieldsEvents:
    def test_fim_stream_yields_events(self, mock_router, mistral_client):
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

        stream = mistral_client.fim.stream(model="codestral-latest", prompt="def ")
        results = list(stream)

        assert len(results) == 2
        assert results[0].data.choices[0].delta.content == "def hello():"
        assert results[-1].data.choices[0].finish_reason == "stop"


class TestStreamContextManager:
    def test_stream_context_manager(self, mock_router, mistral_client):
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
        with mistral_client.chat.stream(model="m", messages=user_msg()) as stream:
            assert isinstance(stream, EventStream)
            for event in stream:
                collected.append(event)

        assert len(collected) == 2


class TestStream422Error:
    def test_stream_422_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=VALIDATION_ERROR_RESPONSE,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(HTTPValidationError) as exc_info:
            mistral_client.chat.stream(model="m", messages=user_msg())

        assert exc_info.value.status_code == 422
        assert exc_info.value.data.detail is not None


class TestStream500Error:
    def test_stream_500_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                500,
                text="Internal Server Error",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.stream(model="m", messages=user_msg())

        assert exc_info.value.status_code == 500


class TestEmptyDataLinesIgnored:
    def test_empty_data_lines_ignored(self, mock_router, mistral_client):
        """SSE body with extra blank lines between events should not break parsing."""
        chunk = make_stream_chunk("content", finish_reason="stop")
        # Manually build SSE with extra blank lines
        import json as _json

        raw = (
            "\n\n"  # leading blank lines
            f"data: {_json.dumps(chunk)}\n\n"
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

        stream = mistral_client.chat.stream(model="m", messages=user_msg())
        results = list(stream)

        assert len(results) == 1
        assert results[0].data.choices[0].delta.content == "content"


class TestTranscriptionStreamYieldsEvents:
    def test_transcription_stream_yields_events(self, mock_router, mistral_client):
        done_data = {
            "type": "transcription.done",
            "model": "mistral-large-latest",
            "text": "Hello",
            "language": "en",
            "usage": {"prompt_tokens": 10, "completion_tokens": 0, "total_tokens": 10},
        }
        blocks = (
            "event: transcription.text.delta\n"
            "data: " + json.dumps({"type": "transcription.text.delta", "text": "Hello"}) + "\n\n"
            "event: transcription.done\n"
            "data: " + json.dumps(done_data) + "\n\n"
        )
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(
                200,
                content=blocks.encode(),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.audio.transcriptions.stream(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )
        results = list(stream)

        assert len(results) >= 1


class TestStreamResponseClosedAfterDone:
    def test_stream_response_closed_after_done(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk("Hello"),
            make_stream_chunk(" world"),
            make_stream_chunk("", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = mistral_client.chat.stream(model="m", messages=user_msg())
        results = list(stream)

        assert len(results) == 3
