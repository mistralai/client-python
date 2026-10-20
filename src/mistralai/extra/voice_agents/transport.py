from __future__ import annotations

import asyncio
import inspect
import json
import logging
import re
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

try:
    import numpy as np
    from livekit import rtc
    from livekit.rtc.room import EventTypes
except ModuleNotFoundError as exc:
    from .errors import VoiceAgentDependencyError

    raise VoiceAgentDependencyError(
        "Voice agents require: pip install 'mistralai[voice-agents]'"
    ) from exc
except ImportError as exc:
    from .errors import VoiceAgentDependencyError

    raise VoiceAgentDependencyError(
        f"Voice transport cannot load {exc.name or 'its dependencies'}: it is "
        f"installed but failed to import ({exc}). On Windows this usually means "
        "the installed wheel does not match the running interpreter."
    ) from exc

from mistralai.client.models import AudioSessionCreateResponse as SessionCreateResponse
from pydantic import BaseModel, ValidationError

from .audio import BYTES_PER_SAMPLE, CHANNELS
from .errors import VoiceAgentConnectionError
from .events import (
    TransportDisconnectReason,
    UnhandledToolEvent,
    VoiceAgentErrorEvent,
    VoiceEvent,
    VoiceEventName,
    parse_voice_agent_event,
)
from .tools import FunctionHandler
from .utils import (
    _decode_json_payload,
    _optional_attr,
)

EventCallback = Callable[[VoiceEventName, VoiceEvent], Awaitable[None]]

logger = logging.getLogger(__name__)

SAMPLE_RATE = 48_000
FUNCTION_TOOL_RPC_METHOD = "mistral.function_tool"
SESSION_UPDATE_RPC_METHOD = "mistral.session_update"
FUNCTION_CALL_INVALID_PAYLOAD_CODE = 2400
FUNCTION_CALL_NO_HANDLER_CODE = 2404
FUNCTION_CALL_HANDLER_FAILED_CODE = 1
AGENT_JOIN_TIMEOUT_S = 30.0

_TRANSPORT_DISCONNECT_REASONS: dict[str, TransportDisconnectReason] = {
    "CLIENT_INITIATED": "client_closed",
    "USER_REJECTED": "client_closed",
    "SERVER_SHUTDOWN": "server_closed",
    "PARTICIPANT_REMOVED": "server_closed",
    "DUPLICATE_IDENTITY": "server_closed",
    "MIGRATION": "server_closed",
    "ROOM_DELETED": "session_ended",
    "ROOM_CLOSED": "session_ended",
    "AGENT_ERROR": "agent_error",
    "CONNECTION_TIMEOUT": "timeout",
    "USER_UNAVAILABLE": "timeout",
    "SIGNAL_CLOSE": "network_failure",
    "MEDIA_FAILURE": "network_failure",
    "SIP_TRUNK_FAILURE": "network_failure",
    "JOIN_FAILURE": "network_failure",
    "STATE_MISMATCH": "network_failure",
}


class _DropDataTrackClose(logging.Filter):
    """Drop the harmless "'_data_track' closed unexpectedly" error.

    The livekit Rust core opens a `_data_track` data channel on every connect
    and logs an error when it closes. The SDK does not use data tracks.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return "'_data_track' closed unexpectedly" not in record.getMessage()


logging.getLogger("livekit").addFilter(_DropDataTrackClose())


class _FunctionCall(BaseModel):
    name: str
    arguments: dict[str, Any] | str | None = None


class Transport(ABC):
    """Abstract base class for voice agent transports."""

    def __init__(self, *, emit: EventCallback) -> None:
        self._emit = emit

    @abstractmethod
    async def start(self) -> None:
        """Connect to the remote voice agent."""

    async def wait_for_agent(self) -> None:
        """Block until the agent can hear audio sent to it."""

    @abstractmethod
    async def send_audio(self, audio: bytes) -> None:
        """Send audio bytes to the remote voice agent."""

    @abstractmethod
    async def set_input_enabled(self, enabled: bool) -> None:
        """Mute or unmute the local audio input track."""

    @abstractmethod
    async def send_session_update(self, payload: str) -> str:
        """Send a JSON session update to the agent and return its JSON reply."""

    @abstractmethod
    def add_function_handlers(self, function_handlers: list[FunctionHandler]) -> None:
        """Register additional local handlers, replacing any with the same name."""

    @abstractmethod
    async def close(self) -> None:
        """Disconnect from the remote voice agent."""


class LiveKitTransport(Transport):
    def __init__(
        self,
        session: SessionCreateResponse,
        *,
        emit: EventCallback,
        function_handlers: list[FunctionHandler] | None = None,
    ) -> None:
        super().__init__(emit=emit)
        self._session = session
        self._tools_by_name = {tool.name: tool for tool in function_handlers or []}
        self._rtc: Any | None = None
        self._room: Any | None = None
        self._room_listeners: list[tuple[EventTypes, Callable[..., Any]]] = []
        self._audio_source: Any | None = None
        self._input_track: Any | None = None
        self._publication: Any | None = None
        self._mixer_buffers: list[_PcmBuffer] = []
        self._mixer_started = False
        self._tasks: set[asyncio.Task[Any]] = set()
        self._closing = False
        self._reconnecting = False
        self._disconnect_error_emitted = False
        self._pending_agent_disconnect: VoiceAgentErrorEvent | None = None
        self._agent_disconnect_check: asyncio.Task[None] | None = None
        self._agent_present = asyncio.Event()

    async def start(self) -> None:
        self._rtc = rtc
        room = rtc.Room()
        self._room = room
        self._room_listeners = [
            ("track_subscribed", self._on_track_subscribed),
            ("data_received", self._on_data_received),
            ("disconnected", self._on_disconnected),
            ("reconnecting", self._on_reconnecting),
            ("reconnected", self._on_reconnected),
            ("participant_connected", self._on_participant_connected),
            ("participant_disconnected", self._on_participant_disconnected),
        ]
        for event, callback in self._room_listeners:
            room.on(event, callback)

        try:
            await room.connect(
                self._session.server_url,
                self._session.participant_token,
            )
        except rtc.ConnectError as exc:
            raise VoiceAgentConnectionError(
                _connect_error_message(self._session.id, exc.message)
            ) from exc
        self._register_function_handlers()
        await self._publish_input_track()
        if self._has_agent_participant():
            self._agent_present.set()

    async def wait_for_agent(self) -> None:
        await self._agent_present.wait()

    def _register_function_handlers(self) -> None:
        assert self._room is not None

        async def handler(data: Any) -> str:
            return await self._dispatch_function_call(data.payload)

        self._room.local_participant.register_rpc_method(
            FUNCTION_TOOL_RPC_METHOD, handler
        )

    async def _dispatch_function_call(self, payload: str) -> str:
        try:
            call = _FunctionCall.model_validate(_decode_json_payload(payload))
        except ValidationError as exc:
            problems = "; ".join(
                f"{'.'.join(map(str, error['loc'])) or 'payload'}: {error['msg']}"
                for error in exc.errors()
            )
            raise rtc.RpcError(
                FUNCTION_CALL_INVALID_PAYLOAD_CODE,
                f"Malformed function call payload: {problems}",
            ) from exc
        tool = self._tools_by_name.get(call.name)
        if tool is None:
            await self._emit(
                "unhandled_tool",
                UnhandledToolEvent(name=call.name, arguments=call.arguments),
            )
            raise rtc.RpcError(
                FUNCTION_CALL_NO_HANDLER_CODE,
                f"No handler for function `{call.name}`",
            )
        try:
            arguments = call.arguments
            raw = json.dumps(arguments) if isinstance(arguments, dict) else arguments
            return await tool.invoke(raw)
        except Exception as exc:
            raise rtc.RpcError(
                FUNCTION_CALL_HANDLER_FAILED_CODE,
                f"function `{tool.name}` failed: {exc}",
            ) from exc

    def add_function_handlers(self, function_handlers: list[FunctionHandler]) -> None:
        # Handlers are only ever added or overridden, never dropped: the agent
        # applies tool changes at the next turn boundary, so a call already in
        # flight may still target a tool the latest update removed.
        self._tools_by_name |= {tool.name: tool for tool in function_handlers}

    async def send_session_update(self, payload: str) -> str:
        try:
            await asyncio.wait_for(self.wait_for_agent(), timeout=AGENT_JOIN_TIMEOUT_S)
        except asyncio.TimeoutError as exc:
            raise VoiceAgentConnectionError(
                f"Agent did not join within {AGENT_JOIN_TIMEOUT_S:g}s"
            ) from exc
        if self._room is None or self._closing:
            raise VoiceAgentConnectionError("Voice session is not connected")
        agent_identity = self._find_agent_identity(self._room)
        return await self._room.local_participant.perform_rpc(
            destination_identity=agent_identity,
            method=SESSION_UPDATE_RPC_METHOD,
            payload=payload,
            response_timeout=5.0,
        )

    def _find_agent_identity(self, room: Any) -> str:
        for identity, participant in room.remote_participants.items():
            if _is_agent_participant(self._rtc, participant):
                return identity
        raise VoiceAgentConnectionError("No voice agent found in the session")

    async def send_audio(self, audio: bytes) -> None:
        if self._audio_source is None:
            raise VoiceAgentConnectionError("Audio input track is not ready")

        samples_per_channel = len(audio) // (BYTES_PER_SAMPLE * CHANNELS)
        assert self._rtc is not None
        frame = self._rtc.AudioFrame(
            data=audio,
            sample_rate=SAMPLE_RATE,
            num_channels=CHANNELS,
            samples_per_channel=samples_per_channel,
        )
        result = self._audio_source.capture_frame(frame)
        if inspect.isawaitable(result):
            await result

    async def set_input_enabled(self, enabled: bool) -> None:
        track = self._input_track
        if track is None and self._publication is not None:
            track = getattr(self._publication, "track", None)
        if track is None:
            return

        for name in ("set_enabled", "set_muted"):
            method = getattr(track, name, None)
            if method is None:
                continue
            if name == "set_muted":
                result = method(not enabled)
            else:
                result = method(enabled)
            if inspect.isawaitable(result):
                await result
            return

        method_name = "unmute" if enabled else "mute"
        method = getattr(track, method_name, None)
        if method is None:
            return
        result = method()
        if inspect.isawaitable(result):
            await result

    async def close(self) -> None:
        self._closing = True
        self._agent_present.set()
        try:
            # Keep remote tracks alive until LiveKit finishes room teardown;
            # closing their streams first makes native cleanup drop them twice.
            room = self._room
            if room is not None:
                result = room.disconnect()
                if inspect.isawaitable(result):
                    await result
        finally:
            # close() may be called by an event handler running in _tasks.
            # Never cancel/await that callback from its own cleanup path.
            tasks = [task for task in self._tasks if task is not asyncio.current_task()]
            for task in tasks:
                task.cancel()
            for task in tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass

            self._mixer_buffers.clear()
            await self._release_room()

    async def _release_room(self) -> None:
        room, self._room = self._room, None
        audio_source, self._audio_source = self._audio_source, None
        self._input_track = None
        self._publication = None
        if audio_source is not None:
            try:
                await audio_source.aclose()
            except Exception:
                pass
        if room is not None:
            for event, callback in self._room_listeners:
                room.off(event, callback)

    async def _publish_input_track(self) -> None:
        assert self._room is not None
        assert self._rtc is not None

        self._audio_source = self._rtc.AudioSource(SAMPLE_RATE, CHANNELS)
        track = self._rtc.LocalAudioTrack.create_audio_track(
            "mistral-voice-input",
            self._audio_source,
        )
        self._input_track = track

        publish_options = None
        track_publish_options = getattr(self._rtc, "TrackPublishOptions", None)
        if track_publish_options is not None:
            publish_options = track_publish_options()
            track_source = getattr(self._rtc, "TrackSource", None)
            source = getattr(track_source, "SOURCE_MICROPHONE", None)
            if source is not None:
                publish_options.source = source

        publish_track = self._room.local_participant.publish_track
        if publish_options is None:
            self._publication = await publish_track(track)
        else:
            self._publication = await publish_track(track, publish_options)

    def _on_track_subscribed(
        self,
        track: Any,
        publication: Any = None,
        _participant: Any = None,
        *_args: Any,
    ) -> None:
        if not _is_audio_track(self._rtc, track):
            return
        if not _is_agent_output_track(self._rtc, track, publication):
            return
        self._add_agent_audio(track)

    def _add_agent_audio(self, track: Any) -> None:
        assert self._rtc is not None
        stream = self._rtc.AudioStream(
            track, capacity=10, sample_rate=SAMPLE_RATE, num_channels=CHANNELS
        )
        buf = _PcmBuffer()
        self._mixer_buffers.append(buf)
        reader = asyncio.create_task(self._read_track_into(stream, buf))
        self._tasks.add(reader)

        def _release(task: asyncio.Task[None]) -> None:
            self._tasks.discard(task)
            # Otherwise the pump keeps mixing silence from a dead track's buffer,
            # and the list grows for every track the session ever subscribed to.
            if buf in self._mixer_buffers:
                self._mixer_buffers.remove(buf)

        reader.add_done_callback(_release)

        if not self._mixer_started:
            self._mixer_started = True
            pump = asyncio.create_task(self._pump_mixer())
            self._tasks.add(pump)
            pump.add_done_callback(self._tasks.discard)

    async def _read_track_into(self, stream: Any, buf: _PcmBuffer) -> None:
        try:
            async for event in stream:
                frame = getattr(event, "frame", event)
                data = getattr(frame, "data", b"")
                buf.push(np.frombuffer(bytes(data), dtype=np.int16))
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            if not self._closing:
                await self._emit(
                    "error",
                    VoiceAgentErrorEvent(
                        message=f"Error while receiving agent audio: {exc}",
                        fatal=True,
                        code="audio_receive_error",
                        source="transport",
                    ),
                )
        finally:
            aclose = getattr(stream, "aclose", None)
            if aclose is not None:
                try:
                    result = aclose()
                    if inspect.isawaitable(result):
                        await result
                except Exception:
                    pass

    async def _pump_mixer(self) -> None:
        block = (SAMPLE_RATE // 50) * CHANNELS  # 20ms
        block_s = (SAMPLE_RATE // 50) / SAMPLE_RATE
        loop = asyncio.get_running_loop()
        next_at = loop.time()
        try:
            while True:
                acc = np.zeros(block, dtype=np.int32)
                for buf in self._mixer_buffers:
                    acc += buf.take(block).astype(np.int32)
                mixed = np.clip(acc, -32768, 32767).astype(np.int16)
                await self._emit("audio", mixed.tobytes())
                next_at += block_s
                delay = next_at - loop.time()
                if delay > 0:
                    await asyncio.sleep(delay)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            await self._emit(
                "error",
                VoiceAgentErrorEvent(
                    message=f"Error while receiving agent audio: {exc}",
                    fatal=True,
                    code="audio_receive_error",
                    source="transport",
                ),
            )

    def _on_disconnected(self, reason: Any = None, *_args: Any) -> None:
        mapped = _disconnect_reason(reason)
        self._emit_disconnect_error(
            code="session_disconnected",
            message=f"Voice session disconnected unexpectedly: {mapped}",
            reason=mapped,
        )

    def _on_reconnecting(self, *_args: Any) -> None:
        self._reconnecting = True

    def _on_reconnected(self, *_args: Any) -> None:
        self._reconnecting = False
        self._schedule_agent_disconnect_check()

    def _has_agent_participant(self) -> bool:
        if self._room is None:
            return False
        return any(
            _is_agent_participant(self._rtc, participant)
            for participant in self._room.remote_participants.values()
        )

    def _on_participant_connected(self, participant: Any, *_args: Any) -> None:
        if _is_agent_participant(self._rtc, participant):
            self._pending_agent_disconnect = None
            self._agent_present.set()

    def _on_participant_disconnected(self, participant: Any, *_args: Any) -> None:
        if not _is_agent_participant(self._rtc, participant):
            return
        mapped = _disconnect_reason(getattr(participant, "disconnect_reason", None))
        self._pending_agent_disconnect = VoiceAgentErrorEvent(
            message=f"Voice agent disconnected unexpectedly: {mapped}",
            fatal=True,
            code="agent_disconnected",
            source="transport",
            payload={"reason": mapped},
        )
        self._schedule_agent_disconnect_check()

    def _schedule_agent_disconnect_check(self) -> None:
        if self._pending_agent_disconnect is None:
            return
        if (
            self._agent_disconnect_check is not None
            and not self._agent_disconnect_check.done()
        ):
            return
        check = asyncio.create_task(self._confirm_agent_disconnected())
        self._agent_disconnect_check = check
        self._tasks.add(check)
        check.add_done_callback(self._tasks.discard)

    async def _confirm_agent_disconnected(self) -> None:
        # Browser LiveKit emits ParticipantDisconnected immediately before
        # Reconnecting during a full reconnect. Yield once so that event can
        # arrive before deciding whether the agent actually left.
        await asyncio.sleep(0)
        if self._closing or self._reconnecting:
            return
        if self._has_agent_participant():
            self._pending_agent_disconnect = None
            return
        event = self._pending_agent_disconnect
        self._pending_agent_disconnect = None
        if event is not None:
            self._emit_disconnect_error_event(event)

    def _emit_disconnect_error(
        self, *, code: str, message: str, reason: TransportDisconnectReason
    ) -> None:
        self._emit_disconnect_error_event(
            VoiceAgentErrorEvent(
                message=message,
                fatal=True,
                code=code,
                source="transport",
                payload={"reason": reason},
            )
        )

    def _emit_disconnect_error_event(self, event: VoiceAgentErrorEvent) -> None:
        if self._closing or self._disconnect_error_emitted:
            return
        self._disconnect_error_emitted = True
        self._pending_agent_disconnect = None
        self._emit_nowait("error", event)

    def _on_data_received(
        self,
        packet: Any,
        participant: Any = None,
        _kind: Any = None,
        topic: Any = None,
        *_args: Any,
    ) -> None:
        topic = topic if topic is not None else getattr(packet, "topic", None)
        if topic != "voice_agent.events":
            return
        sender = (
            participant
            if participant is not None
            else getattr(packet, "participant", None)
        )
        if sender is None or not _is_agent_participant(self._rtc, sender):
            return
        name, event = parse_voice_agent_event(
            _decode_json_payload(getattr(packet, "data", packet))
        )
        self._emit_nowait(name, event)

    def _emit_nowait(self, name: VoiceEventName, event: VoiceEvent) -> None:
        task: asyncio.Task[None] = asyncio.create_task(self._emit_async(name, event))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _emit_async(self, name: VoiceEventName, event: VoiceEvent) -> None:
        await self._emit(name, event)


class _PcmBuffer:
    """Per-track PCM ring. The reader appends frames; the mixer pump takes fixed
    blocks. Capped at ~1s so a stalled reader can't grow unbounded."""

    _MAX = SAMPLE_RATE * CHANNELS  # ~1s of samples

    def __init__(self) -> None:
        self._buf: np.ndarray = np.empty(0, dtype=np.int16)

    def push(self, samples: np.ndarray) -> None:
        self._buf = np.concatenate((self._buf, samples))
        if self._buf.shape[0] > self._MAX:
            self._buf = self._buf[-self._MAX :]

    def take(self, n: int) -> np.ndarray:
        head, self._buf = self._buf[:n], self._buf[n:]
        if head.shape[0] < n:
            pad = np.zeros(n - head.shape[0], dtype=np.int16)
            head = np.concatenate((head, pad))
        return head


def _is_audio_track(rtc: Any, track: Any) -> bool:
    kind = getattr(track, "kind", None)
    track_kind = getattr(rtc, "TrackKind", None)
    audio_kind = getattr(track_kind, "KIND_AUDIO", None)
    if audio_kind is not None and kind == audio_kind:
        return True
    return str(kind).lower().endswith("audio")


def _is_agent_participant(rtc: Any, participant: Any) -> bool:
    participant_kind = getattr(rtc, "ParticipantKind", None)
    agent_kind = getattr(participant_kind, "PARTICIPANT_KIND_AGENT", None)
    if agent_kind is not None and getattr(participant, "kind", None) == agent_kind:
        return True
    # rtc.Participant.permissions exposes the server-issued permission proto,
    # unlike participant attributes, which a normal participant can set.
    permissions = getattr(participant, "permissions", None)
    return getattr(permissions, "agent", False) is True


def _connect_error_message(session_id: str, detail: str) -> str:
    """Explain a rejected join from the status LiveKit's signal server returned.

    ConnectError only carries a message, e.g. "... client error: 401
    Unauthorized - invalid authorization token: token has invalid claims:
    token is expired". Unrecognized messages keep LiveKit's own wording.
    """
    match = re.search(r"client error: (\d{3})", detail)
    status = int(match.group(1)) if match else None
    if status == 401 and "expired" in detail:
        return (
            f"Voice session {session_id} can no longer be joined: its participant "
            "token expired. Create a new session and connect before its expires_at."
        )
    if status == 404:
        return (
            f"Voice session {session_id} has ended: its room was closed, timed "
            "out or deleted. Create a new session."
        )
    if status == 401:
        return f"Voice session {session_id} rejected its participant token: {detail}"
    return f"Failed to connect to voice session {session_id}: {detail}"


def _disconnect_reason(reason: Any) -> TransportDisconnectReason:
    name = getattr(reason, "name", None)
    if not isinstance(name, str):
        try:
            name = rtc.DisconnectReason.Name(reason)
        except (KeyError, TypeError, ValueError):
            name = str(reason)
    mapped = _TRANSPORT_DISCONNECT_REASONS.get(name.upper(), "unknown")
    logger.debug("livekit disconnect reason %s reported as %s", name, mapped)
    return mapped


def _is_agent_output_track(rtc: Any, track: Any, publication: Any) -> bool:
    track_names = {
        name
        for name in (
            _optional_attr(track, "name"),
            _optional_attr(publication, "name"),
        )
        if name is not None
    }
    # roomio_audio is agent speech, background_audio carries tool-call fillers;
    # both are agent output the user should hear (they play at disjoint times).
    if "background_audio" in track_names:
        return True
    if "roomio_audio" in track_names:
        return True

    track_source = getattr(rtc, "TrackSource", None)
    microphone_source = getattr(track_source, "SOURCE_MICROPHONE", None)
    publication_source = getattr(publication, "source", None)
    if microphone_source is not None and publication_source is not None:
        return publication_source == microphone_source

    return True
