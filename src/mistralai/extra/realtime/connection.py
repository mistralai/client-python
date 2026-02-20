from __future__ import annotations

import base64
import json
from asyncio import CancelledError
from collections import deque
from typing import Any, AsyncIterator, Deque, Optional, Union

from pydantic import ValidationError, BaseModel

try:
    from websockets.asyncio.client import ClientConnection  # websockets >= 13.0
except ImportError as exc:
    raise ImportError(
        "The `websockets` package (>=13.0) is required for real-time transcription. "
        "Install with: pip install 'mistralai[realtime]'"
    ) from exc

from mistralai.models import (
    AudioFormat,
    RealtimeTranscriptionInputAudioAppend,
    RealtimeTranscriptionInputAudioEnd,
    RealtimeTranscriptionInputAudioFlush,
    RealtimeTranscriptionError,
    RealtimeTranscriptionSession,
    RealtimeTranscriptionSessionCreated,
    RealtimeTranscriptionSessionUpdated,
    RealtimeTranscriptionSessionUpdateMessage,
    RealtimeTranscriptionSessionUpdatePayload,
    TranscriptionStreamDone,
    TranscriptionStreamLanguage,
    TranscriptionStreamSegmentDelta,
    TranscriptionStreamTextDelta,
)
from mistralai.types import UNSET


class UnknownRealtimeEvent(BaseModel):
    """
    Forward-compat fallback event:
    - unknown message type
    - invalid JSON payload
    - schema validation failure
    """

    type: Optional[str]
    content: Any
    error: Optional[str] = None


RealtimeEvent = Union[
    # session lifecycle
    RealtimeTranscriptionSessionCreated,
    RealtimeTranscriptionSessionUpdated,
    # server errors
    RealtimeTranscriptionError,
    # transcription events
    TranscriptionStreamLanguage,
    TranscriptionStreamSegmentDelta,
    TranscriptionStreamTextDelta,
    TranscriptionStreamDone,
    # forward-compat fallback
    UnknownRealtimeEvent,
]

_MESSAGE_MODELS: dict[str, Any] = {
    "session.created": RealtimeTranscriptionSessionCreated,
    "session.updated": RealtimeTranscriptionSessionUpdated,
    "error": RealtimeTranscriptionError,
    "transcription.language": TranscriptionStreamLanguage,
    "transcription.segment": TranscriptionStreamSegmentDelta,
    "transcription.text.delta": TranscriptionStreamTextDelta,
    "transcription.done": TranscriptionStreamDone,
}


def parse_realtime_event(payload: Any) -> RealtimeEvent:
    """
    Tolerant parser:
    - unknown event type -> UnknownRealtimeEvent
    - validation failures -> UnknownRealtimeEvent (includes error string)
    - invalid payload -> UnknownRealtimeEvent
    """
    if not isinstance(payload, dict):
        return UnknownRealtimeEvent(
            type=None, content=payload, error="expected JSON object"
        )

    msg_type = payload.get("type")
    if not isinstance(msg_type, str):
        return UnknownRealtimeEvent(
            type=None, content=payload, error="missing/invalid 'type'"
        )

    model_cls = _MESSAGE_MODELS.get(msg_type)
    if model_cls is None:
        return UnknownRealtimeEvent(
            type=msg_type, content=payload, error="unknown event type"
        )
    try:
        parsed = model_cls.model_validate(payload)
        return parsed
    except ValidationError as exc:
        return UnknownRealtimeEvent(type=msg_type, content=payload, error=str(exc))


class RealtimeConnection:
    def __init__(
        self,
        websocket: ClientConnection,
        session: RealtimeTranscriptionSession,
        *,
        initial_events: Optional[list[RealtimeEvent]] = None,
    ) -> None:
        self._websocket = websocket
        self._session = session
        self._closed = False
        self._initial_events: Deque[RealtimeEvent] = deque(initial_events or [])

    @property
    def request_id(self) -> str:
        return self._session.request_id

    @property
    def session(self) -> RealtimeTranscriptionSession:
        return self._session

    @property
    def audio_format(self) -> AudioFormat:
        return self._session.audio_format

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def send_audio(
        self, audio_bytes: Union[bytes, bytearray, memoryview]
    ) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")

        message = RealtimeTranscriptionInputAudioAppend(
            audio=base64.b64encode(bytes(audio_bytes)).decode("ascii")
        )
        await self._websocket.send(message.model_dump_json())

    async def flush_audio(self) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")
        await self._websocket.send(
            RealtimeTranscriptionInputAudioFlush().model_dump_json()
        )

    async def update_session(
        self,
        audio_format: Optional[AudioFormat] = None,
        *,
        target_streaming_delay_ms: Optional[int] = None,
    ) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")

        if audio_format is None and target_streaming_delay_ms is None:
            raise ValueError("At least one session field must be provided")

        message = RealtimeTranscriptionSessionUpdateMessage(
            session=RealtimeTranscriptionSessionUpdatePayload(
                audio_format=audio_format if audio_format is not None else UNSET,
                target_streaming_delay_ms=target_streaming_delay_ms
                if target_streaming_delay_ms is not None
                else UNSET,
            )
        )
        await self._websocket.send(message.model_dump_json())

    async def end_audio(self) -> None:
        if self._closed:
            return
        await self._websocket.send(
            RealtimeTranscriptionInputAudioEnd().model_dump_json()
        )

    async def close(self, *, code: int = 1000, reason: str = "") -> None:
        if self._closed:
            return
        self._closed = True
        await self._websocket.close(code=code, reason=reason)

    async def __aenter__(self) -> "RealtimeConnection":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def __aiter__(self) -> AsyncIterator[RealtimeEvent]:
        return self.events()

    async def events(self) -> AsyncIterator[RealtimeEvent]:
        # replay any handshake/prelude events (including session.created)
        while self._initial_events:
            ev = self._initial_events.popleft()
            self._apply_session_updates(ev)
            yield ev

        try:
            async for msg in self._websocket:
                text = (
                    msg.decode("utf-8", errors="replace")
                    if isinstance(msg, (bytes, bytearray))
                    else msg
                )
                try:
                    data = json.loads(text)
                except Exception as exc:
                    yield UnknownRealtimeEvent(
                        type=None, content=text, error=f"invalid JSON: {exc}"
                    )
                    continue

                ev = parse_realtime_event(data)
                self._apply_session_updates(ev)
                yield ev
        except CancelledError:
            pass
        finally:
            await self.close()

    def _apply_session_updates(self, ev: RealtimeEvent) -> None:
        if isinstance(ev, RealtimeTranscriptionSessionCreated) or isinstance(
            ev, RealtimeTranscriptionSessionUpdated
        ):
            self._session = ev.session
