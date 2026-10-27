import inspect
import json
import unittest
from typing import Any, AsyncIterator, cast
from unittest import mock

from mistralai.client.models import (
    AudioFormat,
    RealtimeTranscriptionSession,
    RealtimeTranscriptionSessionUpdatePayload,
    TurnDetectionConfig,
    TurnDetectionEagerEndEvent,
    TurnDetectionEndEvent,
    TurnDetectionResumeEvent,
    TurnDetectionStartEvent,
)
from mistralai.extra.realtime.connection import (
    RealtimeConnection,
    UnknownRealtimeEvent,
    parse_realtime_event,
)
from mistralai.extra.realtime.transcription import RealtimeTranscription

MODEL = "voxtral-mini-transcribe-realtime-3"
PCM_16K = {"encoding": "pcm_s16le", "sample_rate": 16000}
SESSION = {"request_id": "ws-123", "model": MODEL, "audio_format": PCM_16K}
SESSION_CREATED = {"type": "session.created", "session": SESSION}
DEFAULT_TURN_DETECTION = TurnDetectionConfig().model_dump()


class FakeWebSocket:
    def __init__(self, incoming: list[dict[str, Any]] | None = None) -> None:
        self.sent: list[dict[str, Any]] = []
        self._incoming = [json.dumps(message) for message in incoming or []]

    async def send(self, message: str) -> None:
        self.sent.append(json.loads(message))

    async def recv(self) -> str:
        return self._incoming.pop(0)

    async def close(self, code: int = 1000, reason: str = "") -> None:
        pass

    def __aiter__(self) -> AsyncIterator[str]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[str]:
        while self._incoming:
            yield self._incoming.pop(0)


def _connection(ws: FakeWebSocket) -> RealtimeConnection:
    session = RealtimeTranscriptionSession.model_validate(SESSION)
    return RealtimeConnection(websocket=cast(Any, ws), session=session)


def _session_update(session: dict[str, Any]) -> dict[str, Any]:
    return {"type": "session.update", "session": session}


class TestParseTurnDetectionEvents(unittest.TestCase):
    def test_turn_events_are_typed(self) -> None:
        cases = [
            ({"type": "turn.start", "time_s": 1.84}, TurnDetectionStartEvent),
            ({"type": "turn.eager_end", "time_s": 2.5}, TurnDetectionEagerEndEvent),
            ({"type": "turn.resume", "time_s": 2.9}, TurnDetectionResumeEvent),
            (
                {"type": "turn.end", "time_s": 4.4, "end_reason": "threshold"},
                TurnDetectionEndEvent,
            ),
        ]
        for payload, expected_cls in cases:
            with self.subTest(event=payload["type"]):
                event = parse_realtime_event(payload)
                self.assertIsInstance(event, expected_cls)
                self.assertEqual(getattr(event, "time_s"), payload["time_s"])
        end_event = parse_realtime_event(cases[-1][0])
        assert isinstance(end_event, TurnDetectionEndEvent)
        self.assertEqual(end_event.end_reason, "threshold")

    def test_invalid_turn_event_falls_back_to_unknown(self) -> None:
        event = parse_realtime_event({"type": "turn.end", "time_s": 4.4})
        self.assertIsInstance(event, UnknownRealtimeEvent)
        self.assertEqual(event.type, "turn.end")


class TestUpdateSession(unittest.IsolatedAsyncioTestCase):
    async def test_sends_audio_format_only(self) -> None:
        ws = FakeWebSocket()
        await _connection(ws).update_session(
            AudioFormat(encoding="pcm_s16le", sample_rate=24000)
        )
        self.assertEqual(
            ws.sent,
            [
                _session_update(
                    {"audio_format": {"encoding": "pcm_s16le", "sample_rate": 24000}}
                )
            ],
        )

    async def test_sends_voxtral3_session_fields(self) -> None:
        ws = FakeWebSocket()
        await _connection(ws).update_session(
            diarize=True,
            context_bias=["Voxtral", "Harmattan"],
            language="en",
            speaker_references={"alice": "UklGRg=="},
        )
        self.assertEqual(
            ws.sent,
            [
                _session_update(
                    {
                        "diarize": True,
                        "context_bias": ["Voxtral", "Harmattan"],
                        "language": "en",
                        "speaker_references": {"alice": "UklGRg=="},
                    }
                )
            ],
        )

    async def test_sends_turn_detection_dict(self) -> None:
        ws = FakeWebSocket()
        await _connection(ws).update_session(
            turn_detection={"start_threshold": 0.8, "end_threshold": 0.2}
        )
        expected_turn_detection = {
            **DEFAULT_TURN_DETECTION,
            "start_threshold": 0.8,
            "end_threshold": 0.2,
        }
        self.assertEqual(
            ws.sent, [_session_update({"turn_detection": expected_turn_detection})]
        )

    async def test_rejects_empty_update(self) -> None:
        ws = FakeWebSocket()
        with self.assertRaisesRegex(ValueError, "At least one session field"):
            await _connection(ws).update_session()
        self.assertEqual(ws.sent, [])


class TestConnect(unittest.IsolatedAsyncioTestCase):
    def _client(self) -> RealtimeTranscription:
        sdk_config = mock.Mock(timeout_ms=None, security=None, user_agent="test-agent")
        sdk_config.get_server_details.return_value = ("https://example.com", {})
        return RealtimeTranscription(sdk_config)

    def _patch(self, ws: FakeWebSocket) -> Any:
        return mock.patch.multiple(
            "mistralai.extra.realtime.transcription",
            connect=mock.AsyncMock(return_value=ws),
            read_service_account_token=mock.Mock(return_value=None),
        )

    async def test_sends_session_after_handshake(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED])
        with self._patch(ws):
            await self._client().connect(
                MODEL,
                audio_format=AudioFormat(encoding="pcm_s16le", sample_rate=16000),
                language="fr",
                turn_detection=TurnDetectionConfig(),
            )
        self.assertEqual(
            ws.sent,
            [
                _session_update(
                    {
                        "audio_format": PCM_16K,
                        "language": "fr",
                        "turn_detection": DEFAULT_TURN_DETECTION,
                    }
                )
            ],
        )

    async def test_sends_nothing_without_session_fields(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED])
        with self._patch(ws):
            await self._client().connect(MODEL)
        self.assertEqual(ws.sent, [])

    async def test_transcribe_stream_forwards_session(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED])

        async def audio() -> AsyncIterator[bytes]:
            yield b"\x00\x00"

        with self._patch(ws):
            async for _ in self._client().transcribe_stream(
                audio(), MODEL, diarize=True
            ):
                pass
        self.assertEqual(ws.sent[0], _session_update({"diarize": True}))


class TestSessionKwargsMatchGeneratedPayload(unittest.TestCase):
    """Fails when a regen adds or removes a session field the helper doesn't expose."""

    def test_helpers_expose_every_session_field(self) -> None:
        fields = set(RealtimeTranscriptionSessionUpdatePayload.model_fields)
        update_params = set(
            inspect.signature(RealtimeConnection.update_session).parameters
        )
        self.assertEqual(update_params - {"self"}, fields)

        for method in (
            RealtimeTranscription.connect,
            RealtimeTranscription.transcribe_stream,
        ):
            with self.subTest(method=method.__qualname__):
                params = set(inspect.signature(method).parameters)
                self.assertEqual(fields - params, set())


if __name__ == "__main__":
    unittest.main()
