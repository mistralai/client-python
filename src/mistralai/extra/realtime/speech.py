from __future__ import annotations

import asyncio
import base64
import json
import time
from asyncio import CancelledError
from collections import deque
from typing import Any, AsyncIterator, Deque, Mapping, Optional, Union
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

try:
    from websockets.asyncio.client import (
        ClientConnection,
        connect,
    )  # websockets >= 13.0
    from websockets.exceptions import ConnectionClosed, ConnectionClosedError
except ImportError as exc:
    raise ImportError(
        "The `websockets` package (>=13.0) is required for real-time speech. "
        "Install with: pip install 'mistralai[realtime]'"
    ) from exc

from pydantic import ValidationError

from mistralai.client import models, utils
from mistralai.client._hooks.service_account_auth import (
    bearer_header,
    read_service_account_token,
)
from mistralai.client.models import (
    RealtimeSpeechError,
    RealtimeSpeechInputTextAppend,
    RealtimeSpeechInputTextEnd,
    RealtimeSpeechInputTextFlush,
    RealtimeSpeechSession,
    RealtimeSpeechSessionCreated,
    RealtimeSpeechSessionUpdated,
    RealtimeSpeechSessionUpdateMessage,
    RealtimeSpeechSessionUpdatePayload,
    RealtimeSpeechStreamingMode,
    SpeechOutputFormat,
    SpeechStreamAudioDelta,
    SpeechStreamDone,
)
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils import generate_url, get_security, get_security_from_env

from ..exceptions import RealtimeSpeechException, RealtimeSpeechWSError
from .connection import UnknownRealtimeEvent

RealtimeSpeechEvent = Union[
    RealtimeSpeechSessionCreated,
    RealtimeSpeechSessionUpdated,
    RealtimeSpeechError,
    SpeechStreamAudioDelta,
    SpeechStreamDone,
    UnknownRealtimeEvent,
]

_MESSAGE_MODELS: dict[str, Any] = {
    "session.created": RealtimeSpeechSessionCreated,
    "session.updated": RealtimeSpeechSessionUpdated,
    "error": RealtimeSpeechError,
    "speech.audio.delta": SpeechStreamAudioDelta,
    "speech.audio.done": SpeechStreamDone,
}


def parse_realtime_speech_event(payload: Any) -> RealtimeSpeechEvent:
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
        return model_cls.model_validate(payload)
    except ValidationError as exc:
        return UnknownRealtimeEvent(type=msg_type, content=payload, error=str(exc))


def _parse_message(msg: Union[str, bytes, bytearray]) -> RealtimeSpeechEvent:
    text = (
        msg.decode("utf-8", errors="replace")
        if isinstance(msg, (bytes, bytearray))
        else msg
    )
    try:
        data = json.loads(text)
    except Exception as exc:
        return UnknownRealtimeEvent(
            type=None, content=text, error=f"invalid JSON: {exc}"
        )
    return parse_realtime_speech_event(data)


class RealtimeSpeechConnection:
    def __init__(
        self,
        websocket: ClientConnection,
        session: RealtimeSpeechSession,
        *,
        initial_events: Optional[list[RealtimeSpeechEvent]] = None,
    ) -> None:
        self._websocket = websocket
        self._session = session
        self._closed = False
        self._initial_events: Deque[RealtimeSpeechEvent] = deque(initial_events or [])

    @property
    def request_id(self) -> str:
        return self._session.request_id

    @property
    def session(self) -> RealtimeSpeechSession:
        return self._session

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def send_text(self, text: str) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")
        await self._websocket.send(
            RealtimeSpeechInputTextAppend(text=text).model_dump_json()
        )

    async def flush(self, text: Optional[str] = None) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")
        message = (
            RealtimeSpeechInputTextFlush()
            if text is None
            else RealtimeSpeechInputTextFlush(text=text)
        )
        await self._websocket.send(message.model_dump_json())

    async def end(self) -> None:
        if self._closed:
            return
        await self._websocket.send(RealtimeSpeechInputTextEnd().model_dump_json())

    async def update_session(
        self,
        *,
        voice_id: Optional[str] = None,
        ref_audio: Optional[str] = None,
        response_format: Optional[SpeechOutputFormat] = None,
        streaming_mode: Optional[RealtimeSpeechStreamingMode] = None,
        expressiveness: Optional[float] = None,
    ) -> None:
        if self._closed:
            raise RuntimeError("Connection is closed")

        fields = {
            "voice": voice_id,
            "ref_audio": ref_audio,
            "response_format": response_format,
            "streaming_mode": streaming_mode,
            "expressiveness": expressiveness,
        }
        fields = {name: value for name, value in fields.items() if value is not None}
        if not fields:
            raise ValueError("At least one session field must be provided")

        message = RealtimeSpeechSessionUpdateMessage(
            session=RealtimeSpeechSessionUpdatePayload.model_validate(fields)
        )
        await self._websocket.send(message.model_dump_json())

    async def close(self, *, code: int = 1000, reason: str = "") -> None:
        if self._closed:
            return
        self._closed = True
        await self._websocket.close(code=code, reason=reason)

    async def __aenter__(self) -> "RealtimeSpeechConnection":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def __aiter__(self) -> AsyncIterator[RealtimeSpeechEvent]:
        return self.events()

    async def events(self) -> AsyncIterator[RealtimeSpeechEvent]:
        while self._initial_events:
            ev = self._initial_events.popleft()
            self._apply_session_updates(ev)
            yield ev

        try:
            async for msg in self._websocket:
                ev = _parse_message(msg)
                self._apply_session_updates(ev)
                yield ev
        except CancelledError:
            pass
        except ConnectionClosedError as exc:
            # Unknown voices etc. are rejected with a close frame, not an error event.
            raise RealtimeSpeechException(
                exc.rcvd.reason if exc.rcvd else "Connection closed by the server",
                code=exc.rcvd.code if exc.rcvd else None,
            ) from exc
        finally:
            await self.close()

    def _apply_session_updates(self, ev: RealtimeSpeechEvent) -> None:
        if isinstance(ev, (RealtimeSpeechSessionCreated, RealtimeSpeechSessionUpdated)):
            self._session = ev.session


class RealtimeSpeech:
    def __init__(self, sdk_config: SDKConfiguration) -> None:
        self._sdk_config = sdk_config

    def _build_url(
        self,
        model: str,
        *,
        server_url: Optional[str],
        query_params: Mapping[str, str],
    ) -> str:
        if server_url is not None:
            base_url = utils.remove_suffix(server_url, "/")
        else:
            base_url, _ = self._sdk_config.get_server_details()

        url = generate_url(base_url, "/v1/audio/speech/realtime", None)

        parsed = urlparse(url)
        merged = dict(parse_qsl(parsed.query, keep_blank_values=True))
        merged["model"] = model
        merged.update(dict(query_params))

        return urlunparse(parsed._replace(query=urlencode(merged)))

    async def connect(
        self,
        model: str,
        *,
        voice_id: Optional[str] = None,
        ref_audio: Optional[str] = None,
        response_format: Optional[SpeechOutputFormat] = None,
        streaming_mode: Optional[RealtimeSpeechStreamingMode] = None,
        expressiveness: Optional[float] = None,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> RealtimeSpeechConnection:
        if timeout_ms is None:
            timeout_ms = self._sdk_config.timeout_ms

        security = self._sdk_config.security
        if security is not None and callable(security):
            security = security()

        resolved_security = get_security_from_env(security, models.Security)

        headers: dict[str, str] = {}
        query_params: dict[str, str] = {}

        if resolved_security is not None:
            security_headers, security_query = get_security(resolved_security)
            headers |= security_headers
            for key, values in security_query.items():
                if values:
                    query_params[key] = values[-1]

        # Websocket handshake bypasses SDK hooks: apply service-account auth here.
        caller_authorization = any(
            name.lower() == "authorization" for name in (http_headers or {})
        )
        if self._sdk_config.security is None and not caller_authorization:
            token = read_service_account_token()
            if token is not None:
                headers["Authorization"] = bearer_header(token)

        if http_headers is not None:
            headers |= dict(http_headers)

        url = self._build_url(model, server_url=server_url, query_params=query_params)

        parsed = urlparse(url)
        if parsed.scheme == "https":
            parsed = parsed._replace(scheme="wss")
        elif parsed.scheme == "http":
            parsed = parsed._replace(scheme="ws")
        ws_url = urlunparse(parsed)
        open_timeout = None if timeout_ms is None else timeout_ms / 1000.0

        websocket: Optional[ClientConnection] = None
        try:
            websocket = await connect(
                ws_url,
                additional_headers=dict(headers),
                open_timeout=open_timeout,
                user_agent_header=self._sdk_config.user_agent,
            )

            created_session, initial_events = await _recv_handshake(
                websocket, timeout_ms=timeout_ms
            )
            connection = RealtimeSpeechConnection(
                websocket=websocket,
                session=created_session,
                initial_events=initial_events,
            )

            session_fields = (
                voice_id,
                ref_audio,
                response_format,
                streaming_mode,
                expressiveness,
            )
            if any(value is not None for value in session_fields):
                await connection.update_session(
                    voice_id=voice_id,
                    ref_audio=ref_audio,
                    response_format=response_format,
                    streaming_mode=streaming_mode,
                    expressiveness=expressiveness,
                )

            return connection

        except RealtimeSpeechException:
            if websocket is not None:
                await websocket.close()
            raise
        except Exception as exc:
            if websocket is not None:
                await websocket.close()
            raise RealtimeSpeechException(f"Failed to connect: {exc}") from exc

    async def speak_stream(
        self,
        text_stream: AsyncIterator[str],
        model: str,
        *,
        voice_id: Optional[str] = None,
        ref_audio: Optional[str] = None,
        response_format: Optional[SpeechOutputFormat] = None,
        streaming_mode: Optional[RealtimeSpeechStreamingMode] = None,
        expressiveness: Optional[float] = None,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> AsyncIterator[RealtimeSpeechEvent]:
        async with await self.connect(
            model,
            voice_id=voice_id,
            ref_audio=ref_audio,
            response_format=response_format,
            streaming_mode=streaming_mode,
            expressiveness=expressiveness,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
        ) as connection:

            async def _send() -> None:
                try:
                    async for text in text_stream:
                        if connection.is_closed:
                            break
                        await connection.send_text(text)
                    await connection.end()
                except Exception:
                    await connection.close()
                    raise

            send_task = asyncio.create_task(_send())

            try:
                async for event in connection:
                    yield event

                    if isinstance(event, (RealtimeSpeechError, SpeechStreamDone)):
                        break
            finally:
                send_task.cancel()
                try:
                    await send_task
                except (asyncio.CancelledError, ConnectionClosed):
                    pass
                await connection.close()


def audio_bytes(event: SpeechStreamAudioDelta) -> bytes:
    return base64.b64decode(event.audio_data)


def _extract_error_message(payload: dict) -> str:
    err = payload.get("error")
    if isinstance(err, dict):
        msg = err.get("message")
        if isinstance(msg, str):
            return msg
        if isinstance(msg, dict):
            detail = msg.get("detail")
            if isinstance(detail, str):
                return detail
    return "Realtime speech error"


async def _recv_handshake(
    websocket: ClientConnection,
    *,
    timeout_ms: Optional[int],
) -> tuple[RealtimeSpeechSession, list[RealtimeSpeechEvent]]:
    timeout_s = None if timeout_ms is None else timeout_ms / 1000.0
    deadline = None if timeout_s is None else (time.monotonic() + timeout_s)

    initial_events: list[RealtimeSpeechEvent] = []

    def remaining() -> Optional[float]:
        if deadline is None:
            return None
        return max(0.0, deadline - time.monotonic())

    try:
        while True:
            raw = await asyncio.wait_for(websocket.recv(), timeout=remaining())
            event = _parse_message(raw)
            initial_events.append(event)

            if isinstance(event, RealtimeSpeechError):
                raise RealtimeSpeechWSError(
                    _extract_error_message(event.model_dump()), payload=event
                )
            if isinstance(event, UnknownRealtimeEvent) and event.type == "error":
                raw_payload = event.content if isinstance(event.content, dict) else {}
                raise RealtimeSpeechWSError(
                    _extract_error_message(raw_payload), raw=event.content
                )
            if isinstance(event, RealtimeSpeechSessionCreated):
                return event.session, initial_events

    except asyncio.TimeoutError as exc:
        raise RealtimeSpeechException("Timeout waiting for session creation.") from exc
    except RealtimeSpeechException:
        raise
    except Exception as exc:
        raise RealtimeSpeechException(
            f"Unexpected websocket handshake failure: {exc}"
        ) from exc
