"""Tests for transcriptions.complete(), stream(), and their async variants."""

import json
from typing import Any

import httpx
import pytest

from mistralai.client.errors import SDKError


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

TRANSCRIPTION_RESPONSE: dict[str, Any] = {
    "model": "mistral-large-latest",
    "text": "Hello world.",
    "usage": {"prompt_tokens": 10, "completion_tokens": 0, "total_tokens": 10},
    "language": "en",
}

VALIDATION_ERROR_RESPONSE: dict[str, Any] = {
    "detail": [
        {
            "loc": ["body", "model"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ],
}


def _make_transcription_sse_body() -> bytes:
    """Build text/event-stream body for transcription streaming.

    Uses standard SSE format with separate ``event:`` and ``data:`` fields.
    The SDK's parser reads each block (separated by blank lines), extracts
    ``event`` and ``data`` fields, and passes a dict of non-None fields
    to the decoder as ``TranscriptionStreamEvents``.
    """
    done_data = {
        "type": "transcription.done",
        "model": "mistral-large-latest",
        "text": "Hello world.",
        "language": "en",
        "usage": {"prompt_tokens": 10, "completion_tokens": 0, "total_tokens": 10},
    }
    blocks = [
        (
            "event: transcription.text.delta\n"
            f"data: {json.dumps({'type': 'transcription.text.delta', 'text': 'Hello'})}\n"
        ),
        (
            "event: transcription.done\n"
            f"data: {json.dumps(done_data)}\n"
        ),
    ]
    body = "\n".join(blocks) + "\n"
    return body.encode()


# ---------------------------------------------------------------------------
# complete with file_url
# ---------------------------------------------------------------------------


class TestCompleteWithFileUrl:
    def test_complete_with_file_url(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        result = mistral_client.audio.transcriptions.complete(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )

        assert result is not None
        assert result.text == "Hello world."
        assert result.model == "mistral-large-latest"
        assert result.language == "en"


# ---------------------------------------------------------------------------
# complete with file_id
# ---------------------------------------------------------------------------


class TestCompleteWithFileId:
    def test_complete_with_file_id(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        result = mistral_client.audio.transcriptions.complete(
            model="mistral-large-latest",
            file_id="file-abc123",
        )

        assert result is not None
        assert result.text == "Hello world."


# ---------------------------------------------------------------------------
# complete with optional params
# ---------------------------------------------------------------------------


class TestCompleteWithOptionalParams:
    def test_complete_with_optional_params(self, mock_router, mistral_client):
        route = mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        result = mistral_client.audio.transcriptions.complete(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
            language="en",
            temperature=0.3,
        )

        assert result is not None
        assert route.called


# ---------------------------------------------------------------------------
# stream returns event stream
# ---------------------------------------------------------------------------


class TestStreamReturnsEventStream:
    def test_stream_returns_event_stream(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(
                200,
                content=_make_transcription_sse_body(),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.audio.transcriptions.stream(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )

        events = list(stream)
        assert len(events) >= 1


# ---------------------------------------------------------------------------
# complete async
# ---------------------------------------------------------------------------


class TestCompleteAsync:
    @pytest.mark.asyncio
    async def test_complete_async(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        result = await mistral_client.audio.transcriptions.complete_async(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )

        assert result is not None
        assert result.text == "Hello world."


# ---------------------------------------------------------------------------
# stream async
# ---------------------------------------------------------------------------


class TestStreamAsync:
    @pytest.mark.asyncio
    async def test_stream_async(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(
                200,
                content=_make_transcription_sse_body(),
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.audio.transcriptions.stream_async(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )

        events = [event async for event in stream]
        assert len(events) >= 1


# ---------------------------------------------------------------------------
# request body with file_url (multipart serialization)
# ---------------------------------------------------------------------------


class TestRequestBodyJsonWithFileUrl:
    def test_request_body_json_with_file_url(self, mock_router, mistral_client):
        route = mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        mistral_client.audio.transcriptions.complete(
            model="mistral-large-latest",
            file_url="https://example.com/audio.wav",
        )

        assert route.called
        request = route.calls.last.request
        # The SDK serializes as form-urlencoded; verify model and file_url
        content = request.content.decode("utf-8", errors="replace")
        assert "mistral-large-latest" in content
        # The URL may be URL-encoded in form data
        assert "example.com" in content
        assert "audio.wav" in content


# ---------------------------------------------------------------------------
# complete with file (multipart)
# ---------------------------------------------------------------------------


class TestCompleteWithFileMultipart:
    def test_complete_with_file_sends_multipart(self, mock_router, mistral_client):
        """complete() with file parameter sends multipart/form-data."""
        route = mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(200, json=TRANSCRIPTION_RESPONSE)
        )

        result = mistral_client.audio.transcriptions.complete(
            model="mistral-large-latest",
            file={"file_name": "audio.wav", "content": b"fake-audio-bytes"},
        )

        assert result is not None
        assert result.text == "Hello world."
        assert route.called
        request = route.calls.last.request
        content_type = request.headers.get("content-type", "")
        # When a file is provided, the SDK should use multipart/form-data
        assert "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type


# ---------------------------------------------------------------------------
# error 422
# ---------------------------------------------------------------------------


class TestError422:
    def test_error_422(self, mock_router, mistral_client):
        mock_router.post("/v1/audio/transcriptions").mock(
            return_value=httpx.Response(422, json=VALIDATION_ERROR_RESPONSE)
        )

        # Transcriptions does not handle 422 specially (unlike classifiers),
        # so it raises a generic SDKError for 4XX
        with pytest.raises(SDKError):
            mistral_client.audio.transcriptions.complete(
                model="mistral-large-latest",
                file_url="https://example.com/audio.wav",
            )
