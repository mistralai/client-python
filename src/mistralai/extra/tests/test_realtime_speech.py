import asyncio
import inspect
import json
import unittest
from typing import Any, AsyncIterator, cast
from unittest import mock

from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.frames import Close

from mistralai.client.models import (
    RealtimeSpeechError,
    RealtimeSpeechSession,
    RealtimeSpeechSessionCreated,
    RealtimeSpeechSessionUpdated,
    RealtimeSpeechSessionUpdatePayload,
    SpeechStreamAudioDelta,
    SpeechStreamDone,
)
from mistralai.extra.exceptions import RealtimeSpeechException, RealtimeSpeechWSError
from mistralai.extra.realtime.connection import UnknownRealtimeEvent
from mistralai.extra.realtime.speech import (
    RealtimeSpeech,
    RealtimeSpeechConnection,
    audio_bytes,
    parse_realtime_speech_event,
)

MODEL = "voxtral-mini-tts-3"
SESSION = {
    "request_id": "ws-123",
    "model": MODEL,
    "voice": "voice_447",
    "is_ref_audio": False,
    "is_voice_profile": False,
    "streaming_mode": "responsive",
    "response_format": "wav",
    "expressiveness": 2.0,
}
SESSION_CREATED = {"type": "session.created", "session": SESSION}
AUDIO_DELTA = {"type": "speech.audio.delta", "audio_data": "AAAAAA=="}
AUDIO_DONE = {
    "type": "speech.audio.done",
    "usage": {"prompt_tokens": 3, "completion_tokens": 10, "total_tokens": 13},
}


class FakeWebSocket:
    def __init__(
        self,
        incoming: list[dict[str, Any]] | None = None,
        close_frame: Close | None = None,
        text_send_error: Exception | None = None,
        wait_for_close: bool = False,
    ) -> None:
        self.sent: list[dict[str, Any]] = []
        self.closed = False
        self._incoming = [json.dumps(message) for message in incoming or []]
        self._close_frame = close_frame
        self._text_send_error = text_send_error
        self._wait_for_close = wait_for_close
        self._closed_event = asyncio.Event()

    async def send(self, message: str) -> None:
        payload = json.loads(message)
        if self._text_send_error and payload["type"] == "input_text.append":
            self._closed_event.set()
            raise self._text_send_error
        self.sent.append(payload)

    async def recv(self) -> str:
        return self._incoming.pop(0)

    async def close(self, code: int = 1000, reason: str = "") -> None:
        self.closed = True
        self._closed_event.set()

    def __aiter__(self) -> AsyncIterator[str]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[str]:
        while self._incoming:
            yield self._incoming.pop(0)
        if self._wait_for_close:
            await self._closed_event.wait()
        if self._close_frame is not None:
            await asyncio.sleep(0)
            raise ConnectionClosedError(self._close_frame, None)


def _connection(ws: FakeWebSocket) -> RealtimeSpeechConnection:
    session = RealtimeSpeechSession.model_validate(SESSION)
    return RealtimeSpeechConnection(websocket=cast(Any, ws), session=session)


class TestParseEvents(unittest.TestCase):
    def test_events_are_typed(self) -> None:
        cases = [
            (SESSION_CREATED, RealtimeSpeechSessionCreated),
            (
                {**SESSION_CREATED, "type": "session.updated"},
                RealtimeSpeechSessionUpdated,
            ),
            (AUDIO_DELTA, SpeechStreamAudioDelta),
            (AUDIO_DONE, SpeechStreamDone),
            (
                {"type": "error", "error": {"message": "bad voice", "code": 3001}},
                RealtimeSpeechError,
            ),
        ]
        for payload, expected_cls in cases:
            with self.subTest(event=expected_cls.__name__):
                self.assertIsInstance(
                    parse_realtime_speech_event(payload), expected_cls
                )

    def test_unknown_and_invalid_events_fall_back(self) -> None:
        for payload in (
            {"type": "speech.surprise"},
            {"type": "speech.audio.delta"},
            ["not", "an", "object"],
        ):
            with self.subTest(payload=payload):
                self.assertIsInstance(
                    parse_realtime_speech_event(payload), UnknownRealtimeEvent
                )

    def test_audio_bytes_decodes_delta(self) -> None:
        event = parse_realtime_speech_event(AUDIO_DELTA)
        assert isinstance(event, SpeechStreamAudioDelta)
        self.assertEqual(audio_bytes(event), b"\x00\x00\x00\x00")


class TestConnection(unittest.IsolatedAsyncioTestCase):
    async def test_sends_text_messages(self) -> None:
        ws = FakeWebSocket()
        connection = _connection(ws)
        await connection.send_text("Hello, ")
        await connection.flush("world.")
        await connection.flush()
        await connection.end()
        self.assertEqual(
            ws.sent,
            [
                {"type": "input_text.append", "text": "Hello, "},
                {"type": "input_text.flush", "text": "world."},
                {"type": "input_text.flush"},
                {"type": "input_text.end"},
            ],
        )

    async def test_update_session_sends_set_fields(self) -> None:
        ws = FakeWebSocket()
        await _connection(ws).update_session(
            voice_id="my-voice", response_format="pcm", expressiveness=1.5
        )
        self.assertEqual(
            ws.sent,
            [
                {
                    "type": "session.update",
                    "session": {
                        "voice": "my-voice",
                        "response_format": "pcm",
                        "expressiveness": 1.5,
                    },
                }
            ],
        )

    async def test_rejects_empty_update(self) -> None:
        ws = FakeWebSocket()
        with self.assertRaisesRegex(ValueError, "At least one session field"):
            await _connection(ws).update_session()
        self.assertEqual(ws.sent, [])

    async def test_events_track_session_updates(self) -> None:
        updated = {**SESSION, "response_format": "pcm"}
        ws = FakeWebSocket([{"type": "session.updated", "session": updated}])
        connection = _connection(ws)
        events = [event async for event in connection.events()]
        self.assertIsInstance(events[0], RealtimeSpeechSessionUpdated)
        self.assertEqual(connection.session.response_format, "pcm")
        self.assertTrue(ws.closed)


class TestRealtimeSpeech(unittest.IsolatedAsyncioTestCase):
    def _client(self) -> RealtimeSpeech:
        sdk_config = mock.Mock(timeout_ms=None, security=None, user_agent="test-agent")
        sdk_config.get_server_details.return_value = ("https://example.com", {})
        return RealtimeSpeech(sdk_config)

    def _patch(
        self, ws: FakeWebSocket, connect_mock: mock.AsyncMock | None = None
    ) -> Any:
        return mock.patch.multiple(
            "mistralai.extra.realtime.speech",
            connect=connect_mock or mock.AsyncMock(return_value=ws),
            read_service_account_token=mock.Mock(return_value=None),
        )

    async def test_connect_url_and_session_update(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED])
        connect_mock = mock.AsyncMock(return_value=ws)
        with self._patch(ws, connect_mock):
            connection = await self._client().connect(
                MODEL, voice_id="my-voice", response_format="pcm"
            )
        self.assertEqual(
            connect_mock.call_args.args[0],
            "wss://example.com/v1/audio/speech/realtime?model=voxtral-mini-tts-3",
        )
        self.assertEqual(
            ws.sent,
            [
                {
                    "type": "session.update",
                    "session": {"voice": "my-voice", "response_format": "pcm"},
                }
            ],
        )
        self.assertEqual(connection.request_id, "ws-123")

    async def test_connect_sends_nothing_without_session_fields(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED])
        with self._patch(ws):
            await self._client().connect(MODEL)
        self.assertEqual(ws.sent, [])

    async def test_connect_raises_on_handshake_error(self) -> None:
        error = {"type": "error", "error": {"message": "Invalid model", "code": 1500}}
        ws = FakeWebSocket([error])
        with self._patch(ws):
            with self.assertRaisesRegex(RealtimeSpeechWSError, "Invalid model") as ctx:
                await self._client().connect(MODEL)
        self.assertEqual(ctx.exception.code, 1500)
        self.assertTrue(ws.closed)

    async def test_speak_stream_sends_text_and_stops_on_done(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED, AUDIO_DELTA, AUDIO_DONE, AUDIO_DELTA])

        async def text() -> AsyncIterator[str]:
            yield "Hello, "
            yield "world."

        with self._patch(ws):
            events = [
                event
                async for event in self._client().speak_stream(
                    text(), MODEL, voice_id="my-voice"
                )
            ]

        self.assertEqual(
            [type(event) for event in events],
            [RealtimeSpeechSessionCreated, SpeechStreamAudioDelta, SpeechStreamDone],
        )
        self.assertEqual(
            ws.sent[0],
            {"type": "session.update", "session": {"voice": "my-voice"}},
        )
        self.assertTrue(ws.closed)

    async def test_server_close_is_raised(self) -> None:
        async def text() -> AsyncIterator[str]:
            yield "Hi."

        close_frame = Close(1008, "Voice 'nope' not found.")
        for fail_text_send in (False, True):
            with self.subTest(fail_text_send=fail_text_send):
                ws = FakeWebSocket(
                    [SESSION_CREATED],
                    close_frame=close_frame,
                    text_send_error=(
                        ConnectionClosedError(close_frame, None)
                        if fail_text_send
                        else None
                    ),
                    wait_for_close=fail_text_send,
                )
                with self._patch(ws):
                    with self.assertRaisesRegex(
                        RealtimeSpeechException, "Voice 'nope' not found."
                    ) as ctx:
                        async for _ in self._client().speak_stream(
                            text(), MODEL, voice_id="nope"
                        ):
                            pass
                self.assertEqual(ctx.exception.code, 1008)

    async def test_clean_server_close_while_sending_ends_quietly(self) -> None:
        ws = FakeWebSocket(
            [SESSION_CREATED],
            text_send_error=ConnectionClosedOK(Close(1000, ""), None),
            wait_for_close=True,
        )

        async def text() -> AsyncIterator[str]:
            yield "Hi."

        with self._patch(ws):
            events = [
                event async for event in self._client().speak_stream(text(), MODEL)
            ]
        self.assertEqual(
            [type(event) for event in events], [RealtimeSpeechSessionCreated]
        )

    async def test_text_stream_error_is_raised(self) -> None:
        ws = FakeWebSocket([SESSION_CREATED], wait_for_close=True)

        async def text() -> AsyncIterator[str]:
            yield "Hi."
            raise ValueError("LLM stream failed")

        async def consume() -> None:
            async for _ in self._client().speak_stream(text(), MODEL):
                pass

        with self._patch(ws):
            task = asyncio.create_task(consume())
            await asyncio.wait({task}, timeout=1)
            self.assertTrue(task.done())
            with self.assertRaisesRegex(ValueError, "LLM stream failed"):
                await task
        self.assertTrue(ws.closed)


class TestSessionKwargsMatchGeneratedPayload(unittest.TestCase):
    """Fails when a regen adds or removes a session field the helper doesn't expose."""

    def test_helpers_expose_every_session_field(self) -> None:
        kwarg_names = {"voice": "voice_id"}
        fields = {
            kwarg_names.get(name, name)
            for name in RealtimeSpeechSessionUpdatePayload.model_fields
        }
        update_params = set(
            inspect.signature(RealtimeSpeechConnection.update_session).parameters
        )
        self.assertEqual(update_params - {"self"}, fields)

        for method in (RealtimeSpeech.connect, RealtimeSpeech.speak_stream):
            with self.subTest(method=method.__qualname__):
                params = set(inspect.signature(method).parameters)
                self.assertEqual(fields - params, set())


if __name__ == "__main__":
    unittest.main()
