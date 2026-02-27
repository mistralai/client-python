"""Tests for RealtimeConnection and parse_realtime_event."""

import base64
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mistralai.extra.realtime.connection import (
    RealtimeConnection,
    UnknownRealtimeEvent,
    parse_realtime_event,
)
from mistralai.client.models import (
    AudioFormat,
    RealtimeTranscriptionSession,
    RealtimeTranscriptionSessionCreated,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_session():
    return RealtimeTranscriptionSession(
        request_id="req-123",
        model="mistral-small-latest",
        audio_format=AudioFormat(encoding="pcm_s16le", sample_rate=16000),
    )


def _make_mock_ws():
    ws = AsyncMock()
    ws.send = AsyncMock()
    ws.close = AsyncMock()
    return ws


def _make_connection(ws=None, session=None, closed=False):
    if ws is None:
        ws = _make_mock_ws()
    if session is None:
        session = _make_session()
    conn = RealtimeConnection(websocket=ws, session=session)
    if closed:
        conn._closed = True
    return conn, ws


# -------------------------------------------------------------------------
# 1. send_audio encodes bytes to base64
# -------------------------------------------------------------------------


class TestSendAudioBase64Encoding:
    @pytest.mark.asyncio
    async def test_send_audio_base64_encoding(self):
        conn, ws = _make_connection()
        audio_data = b"\x01\x02\x03\x04"

        await conn.send_audio(audio_data)

        ws.send.assert_called_once()
        sent_json = json.loads(ws.send.call_args[0][0])
        assert sent_json["type"] == "input_audio.append"
        # Verify the base64 encoding is correct
        decoded = base64.b64decode(sent_json["audio"])
        assert decoded == audio_data


# -------------------------------------------------------------------------
# 2. end_audio message format
# -------------------------------------------------------------------------


class TestEndAudioMessageFormat:
    @pytest.mark.asyncio
    async def test_end_audio_message_format(self):
        conn, ws = _make_connection()

        await conn.end_audio()

        ws.send.assert_called_once()
        sent_json = json.loads(ws.send.call_args[0][0])
        assert sent_json == {"type": "input_audio.end"}


# -------------------------------------------------------------------------
# 3. update_session message format
# -------------------------------------------------------------------------


class TestUpdateSessionMessageFormat:
    @pytest.mark.asyncio
    async def test_update_session_message_format(self):
        conn, ws = _make_connection()
        new_format = AudioFormat(encoding="pcm_f32le", sample_rate=44100)

        await conn.update_session(new_format)

        ws.send.assert_called_once()
        sent_json = json.loads(ws.send.call_args[0][0])
        assert sent_json["type"] == "session.update"
        assert "session" in sent_json
        assert "audio_format" in sent_json["session"]
        assert sent_json["session"]["audio_format"]["encoding"] == "pcm_f32le"
        assert sent_json["session"]["audio_format"]["sample_rate"] == 44100


# -------------------------------------------------------------------------
# 4. close is idempotent
# -------------------------------------------------------------------------


class TestCloseIdempotent:
    @pytest.mark.asyncio
    async def test_close_idempotent(self):
        conn, ws = _make_connection()

        await conn.close()
        await conn.close()
        await conn.close()

        # close on the websocket should only be called once
        assert ws.close.call_count == 1
        assert conn.is_closed is True


# -------------------------------------------------------------------------
# 5. Context manager
# -------------------------------------------------------------------------


class TestContextManager:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        conn, ws = _make_connection()

        async with conn as c:
            assert c is conn
            assert not c.is_closed

        assert conn.is_closed is True
        ws.close.assert_called_once()


# -------------------------------------------------------------------------
# 6. send_audio raises when closed
# -------------------------------------------------------------------------


class TestSendAudioRaisesWhenClosed:
    @pytest.mark.asyncio
    async def test_send_audio_raises_when_closed(self):
        conn, ws = _make_connection(closed=True)

        with pytest.raises(RuntimeError, match="Connection is closed"):
            await conn.send_audio(b"\x01\x02")


# -------------------------------------------------------------------------
# 7. parse_realtime_event: known event type parsed
# -------------------------------------------------------------------------


class TestParseRealtimeEventSessionCreated:
    def test_parse_realtime_event_session_created(self):
        payload = {
            "type": "session.created",
            "session": {
                "request_id": "req-123",
                "model": "mistral-small-latest",
                "audio_format": {
                    "encoding": "pcm_s16le",
                    "sample_rate": 16000,
                },
            },
        }

        result = parse_realtime_event(payload)

        assert isinstance(result, RealtimeTranscriptionSessionCreated)
        assert result.session.request_id == "req-123"
        assert result.type == "session.created"


# -------------------------------------------------------------------------
# 8. parse_realtime_event: unknown type -> UnknownRealtimeEvent
# -------------------------------------------------------------------------


class TestParseRealtimeEventUnknownType:
    def test_parse_realtime_event_unknown_type(self):
        payload = {"type": "completely.unknown.event", "data": {"foo": "bar"}}

        result = parse_realtime_event(payload)

        assert isinstance(result, UnknownRealtimeEvent)
        assert result.type == "completely.unknown.event"
        assert result.error == "unknown event type"


# -------------------------------------------------------------------------
# 9. parse_realtime_event: non-dict -> UnknownRealtimeEvent
# -------------------------------------------------------------------------


class TestParseRealtimeEventInvalidPayload:
    def test_parse_realtime_event_invalid_payload(self):
        result = parse_realtime_event("not a dict")

        assert isinstance(result, UnknownRealtimeEvent)
        assert result.type is None
        assert result.error == "expected JSON object"
        assert result.content == "not a dict"


# -------------------------------------------------------------------------
# 10. parse_realtime_event: missing type field -> UnknownRealtimeEvent
# -------------------------------------------------------------------------


class TestParseRealtimeEventMissingType:
    def test_parse_realtime_event_missing_type(self):
        payload = {"data": "some data", "no_type_field": True}

        result = parse_realtime_event(payload)

        assert isinstance(result, UnknownRealtimeEvent)
        assert result.type is None
        assert "missing/invalid 'type'" in result.error


# -------------------------------------------------------------------------
# 11. events() yields initial session event
# -------------------------------------------------------------------------


class TestEventsYieldsInitialSessionEvent:
    @pytest.mark.asyncio
    async def test_events_yields_session_created(self):
        session_event = json.dumps({
            "type": "session.created",
            "session": {
                "request_id": "req-123",
                "model": "mistral-small-latest",
                "audio_format": {
                    "encoding": "pcm_s16le",
                    "sample_rate": 16000,
                },
            },
        })

        # Create a proper async iterator for the websocket
        async def _async_iter():
            yield session_event

        ws = _make_mock_ws()
        ws.__aiter__ = MagicMock(return_value=_async_iter().__aiter__())

        conn, _ = _make_connection(ws=ws)

        events_list = []
        async for event in conn.events():
            events_list.append(event)

        assert len(events_list) == 1
        assert isinstance(events_list[0], RealtimeTranscriptionSessionCreated)
        assert events_list[0].type == "session.created"


# -------------------------------------------------------------------------
# 12. events() yields UnknownRealtimeEvent for invalid JSON
# -------------------------------------------------------------------------


class TestEventsInvalidJsonYieldsUnknownEvent:
    @pytest.mark.asyncio
    async def test_events_invalid_json(self):
        # Create a proper async iterator for the websocket
        async def _async_iter():
            yield "not json"

        ws = _make_mock_ws()
        ws.__aiter__ = MagicMock(return_value=_async_iter().__aiter__())

        conn, _ = _make_connection(ws=ws)

        events_list = []
        async for event in conn.events():
            events_list.append(event)

        assert len(events_list) == 1
        assert isinstance(events_list[0], UnknownRealtimeEvent)


# -------------------------------------------------------------------------
# 13. end_audio raises when closed
# -------------------------------------------------------------------------


class TestEndAudioRaisesWhenClosed:
    @pytest.mark.asyncio
    async def test_end_audio_noop_when_closed(self):
        conn, ws = _make_connection(closed=True)

        # end_audio() silently returns when connection is closed
        await conn.end_audio()

        # Verify send was never called
        ws.send.assert_not_called()


# -------------------------------------------------------------------------
# 14. update_session raises when closed
# -------------------------------------------------------------------------


class TestUpdateSessionRaisesWhenClosed:
    @pytest.mark.asyncio
    async def test_update_session_raises_when_closed(self):
        conn, ws = _make_connection(closed=True)
        new_format = AudioFormat(encoding="pcm_f32le", sample_rate=44100)

        with pytest.raises(RuntimeError, match="Connection is closed"):
            await conn.update_session(new_format)
