from __future__ import annotations

import asyncio
import inspect
import json
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, Literal, NoReturn, overload

from pydantic import ValidationError

from mistralai.client.models import (
    AudioSessionCreateResponse as SessionCreateResponse,
    AudioTurnConfig,
    AudioTurnConfigTypedDict,
    VoiceAgentFunctionTool,
)

from .audio import AudioInterface
from .errors import VoiceAgentConnectionError, VoiceAgentError
from .events import (
    ConnectedEvent,
    DisconnectedEvent,
    DisconnectReason,
    VoiceAgentErrorEvent,
    UnknownVoiceAgentEvent,
    VoiceAgentSessionUpdatedEvent,
    VoiceAgentToolCallEndedEvent,
    VoiceAgentToolCallStartedEvent,
    VoiceAgentTranscriptEvent,
    VoiceAgentStateChangedEvent,
    UnhandledToolEvent,
    VoiceEvent,
    VoiceEventName,
)
from .tools import FunctionHandler, Tool, VoiceAgentTool, check_function_handlers

if TYPE_CHECKING:
    from .transport import Transport

EventHandler = Callable[[Any], Any]
RemoteSessionDeleter = Callable[[str], Awaitable[None]]

logger = logging.getLogger(__name__)


class VoiceAgentSession:
    """A created remote session; returned by `client.audio.sessions.init()`."""

    def __init__(
        self,
        session: SessionCreateResponse,
        *,
        delete_remote_session: RemoteSessionDeleter,
        audio_interface: AudioInterface | None,
        function_handlers: list[FunctionHandler] | None = None,
    ) -> None:
        self._session_response = session
        self._delete_remote_session_callback = delete_remote_session
        self._audio_interface = audio_interface
        self._transport: Transport | None = None
        self._function_handlers = function_handlers or []
        self._fatal_error: VoiceAgentConnectionError | None = None
        self._handlers: dict[VoiceEventName, list[EventHandler]] = defaultdict(list)
        self._input_task: asyncio.Task[None] | None = None
        self._terminate_task: asyncio.Task[None] | None = None
        self._start_lock = asyncio.Lock()
        self._started = False
        self._closing = False
        self._closed = asyncio.Event()
        self._input_enabled = True
        self._transcript: dict[str, VoiceAgentTranscriptEvent] = {}

    @property
    def transcript(self) -> list[VoiceAgentTranscriptEvent]:
        """Latest cumulative segments, oldest first, retained after closure."""
        return list(self._transcript.values())

    @property
    def id(self) -> str:
        return self._session_response.id

    @property
    def session(self) -> SessionCreateResponse:
        """The created remote session, as returned by `init()`."""
        return self._session_response

    def _require_transport(self) -> Transport:
        if self._closing or self._closed.is_set():
            raise VoiceAgentConnectionError("Voice session is not running")
        if not self._started or self._transport is None:
            raise VoiceAgentConnectionError(
                "Voice session is not connected: call connect() first"
            )
        return self._transport

    @overload
    def on(
        self,
        event: Literal["connected"],
        handler: Callable[[ConnectedEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["disconnected"],
        handler: Callable[[DisconnectedEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["transcript"],
        handler: Callable[[VoiceAgentTranscriptEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["audio"],
        handler: Callable[[bytes], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["tool_call_started"],
        handler: Callable[[VoiceAgentToolCallStartedEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["tool_call_ended"],
        handler: Callable[[VoiceAgentToolCallEndedEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["unhandled_tool"],
        handler: Callable[[UnhandledToolEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["agent_state_changed"],
        handler: Callable[[VoiceAgentStateChangedEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["error"],
        handler: Callable[[VoiceAgentErrorEvent], Any],
    ) -> Callable[[], None]: ...

    @overload
    def on(self, event: Literal["unknown"], handler: Callable[[UnknownVoiceAgentEvent], Any]) -> Callable[[], None]: ...

    @overload
    def on(
        self,
        event: Literal["session_updated"],
        handler: Callable[[VoiceAgentSessionUpdatedEvent], Any],
    ) -> Callable[[], None]: ...

    def on(
        self,
        event: VoiceEventName,
        handler: EventHandler,
    ) -> Callable[[], None]:
        self._handlers[event].append(handler)

        def unsubscribe() -> None:
            self.off(event, handler)

        return unsubscribe

    @overload
    def off(
        self,
        event: Literal["connected"],
        handler: Callable[[ConnectedEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["disconnected"],
        handler: Callable[[DisconnectedEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["transcript"],
        handler: Callable[[VoiceAgentTranscriptEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["audio"],
        handler: Callable[[bytes], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["tool_call_started"],
        handler: Callable[[VoiceAgentToolCallStartedEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["tool_call_ended"],
        handler: Callable[[VoiceAgentToolCallEndedEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["unhandled_tool"],
        handler: Callable[[UnhandledToolEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["agent_state_changed"],
        handler: Callable[[VoiceAgentStateChangedEvent], Any],
    ) -> None: ...

    @overload
    def off(
        self,
        event: Literal["error"],
        handler: Callable[[VoiceAgentErrorEvent], Any],
    ) -> None: ...

    @overload
    def off(self, event: Literal["unknown"], handler: Callable[[UnknownVoiceAgentEvent], Any]) -> None: ...

    @overload
    def off(
        self,
        event: Literal["session_updated"],
        handler: Callable[[VoiceAgentSessionUpdatedEvent], Any],
    ) -> None: ...

    def off(self, event: VoiceEventName, handler: EventHandler) -> None:
        handlers = self._handlers[event]
        if handler in handlers:
            handlers.remove(handler)

    async def connect(self) -> None:
        """Join the session's room and start local audio.

        Handlers whose arguments don't fit their declaration raise
        VoiceAgentConfigurationError and close the session; unpaired handlers or
        declarations emit a recoverable `function_handler_configuration_error`.
        Failing or cancelling connect() closes the session.
        A session connects once: after it closes, create a new one.
        """
        if self._closing or self._closed.is_set():
            raise VoiceAgentConnectionError(
                "Cannot connect a closed voice session, create a new one"
            )
        async with self._start_lock:
            if self._started:
                return
            try:
                from .transport import LiveKitTransport

                error = check_function_handlers(
                    self._session_response.function_tools or [], self._function_handlers
                )
                if error is not None:
                    await self._emit("error", error)
                self._transport = LiveKitTransport(
                    self._session_response, emit=self._handle_transport_event,
                    function_handlers=self._function_handlers,
                )
                await self._transport.start()
            except asyncio.CancelledError:
                await self.close()
                raise
            except Exception as exc:
                await self._fail_start(exc, source="transport")

            if self._audio_interface is not None:
                try:
                    await self._audio_interface.start()
                except asyncio.CancelledError:
                    await self.close()
                    raise
                except Exception as exc:
                    await self._fail_start(exc, source="audio_interface")
                self._input_task = asyncio.create_task(self._pump_input_audio())
            self._started = True
        self._warn_without_audio()
        await self._emit("connected", ConnectedEvent(session_id=self.id))

    def _warn_without_audio(self) -> None:
        if self._audio_interface is not None or self._handlers.get("audio"):
            return
        logger.warning(
            "voice session %s can neither hear nor speak: pass "
            "audio_interface=DefaultAudioInterface() to init(), or subscribe "
            "with session.on('audio', ...) and feed audio with session.send_audio()",
            self.id,
        )

    async def _fail_start(
        self, exc: Exception, *, source: Literal["audio_interface", "transport"]
    ) -> NoReturn:
        event = VoiceAgentErrorEvent(
            message=f"Failed to start voice session: {exc}", fatal=True,
            code="session_start_failed", source=source,
        )
        try:
            await self._emit("error", event, log_unhandled=False)
        finally:
            await self.close(reason="start_failed")
        if isinstance(exc, VoiceAgentError):
            raise exc
        raise VoiceAgentConnectionError(event.message, error_event=event) from exc

    async def wait(self) -> None:
        """Wait for termination, raising a fatal runtime error if one occurred.

        Cancelling this waiter does not close the session.
        """
        await self._closed.wait()
        if self._fatal_error is not None:
            raise self._fatal_error

    async def send_audio(self, audio: bytes) -> None:
        transport = self._require_transport()
        try:
            await transport.send_audio(audio)
        except Exception as exc:
            await self._emit(
                "error",
                VoiceAgentErrorEvent(
                    message=f"Failed to send audio: {exc}",
                    fatal=False,
                    code="audio_send_failed",
                    source="transport",
                ),
                log_unhandled=False,
            )
            raise

    async def set_input_enabled(self, enabled: bool) -> None:
        transport = self._require_transport()
        try:
            await transport.set_input_enabled(enabled)
            self._input_enabled = enabled
        except Exception as exc:
            await self._emit(
                "error",
                VoiceAgentErrorEvent(
                    message=f"Failed to update audio input: {exc}",
                    fatal=False,
                    code="audio_input_update_failed",
                    source="transport",
                ),
                log_unhandled=False,
            )
            raise

    async def update(
        self,
        *,
        instructions: str | None = None,
        tools: list[Tool | FunctionHandler | dict[str, Any]] | None = None,
        turn: AudioTurnConfig | AudioTurnConfigTypedDict | None = None,
    ) -> VoiceAgentSessionUpdatedEvent:
        """Update the live session configuration.

        ``instructions`` and ``tools`` take effect at the next turn boundary;
        ``turn.allow_interruptions`` applies immediately. The returned event reflects
        the full committed config as confirmed by the server. Every participant,
        this one included, also receives it as a ``session_updated`` event.
        """
        transport = self._require_transport()
        # An update is a patch: omitted fields must not overwrite live values.
        payload: dict[str, Any] = {}
        if instructions is not None:
            payload["instructions"] = instructions
        if tools is not None:
            payload["tools"] = [
                tool.to_wire()
                if isinstance(tool, (FunctionHandler, VoiceAgentTool))
                else VoiceAgentTool.model_validate(tool).to_wire()
                for tool in tools
            ]
        if turn is not None:
            payload["turn"] = AudioTurnConfig.model_validate(turn).model_dump(
                mode="json", exclude_unset=True
            )
        handlers_by_name = {
            tool.name: tool for tool in tools or [] if isinstance(tool, FunctionHandler)
        }
        response = await transport.send_session_update(json.dumps(payload))
        try:
            result = VoiceAgentSessionUpdatedEvent.model_validate_json(response)
        except ValidationError as exc:
            raise VoiceAgentConnectionError(
                f"Invalid session update response: {exc}"
            ) from exc

        # The server may drop tools it cannot run, so trust its response over the request.
        confirmed_names = {
            tool.function.name
            for tool in result.session.tools or []
            if isinstance(tool, VoiceAgentFunctionTool)
        }
        transport.add_function_handlers(
            [tool for name, tool in handlers_by_name.items() if name in confirmed_names]
        )
        return result

    async def close(self, *, reason: DisconnectReason | None = None) -> None:
        """Idempotently close local resources and delete the remote session.

        Also releases a session that never connected.
        """
        if self._closing or self._closed.is_set():
            return
        self._closing = True

        if self._input_task is not None and self._input_task is not asyncio.current_task():
            self._input_task.cancel()
            try:
                await self._input_task
            except asyncio.CancelledError:
                pass

        if self._transport is not None:
            try:
                await self._transport.close()
            except Exception as exc:
                await self._emit_cleanup_error(
                    message=f"Failed to close the voice connection: {exc}",
                    code="transport_close_failed",
                    source="transport",
                )
        if self._audio_interface is not None:
            try:
                await self._audio_interface.stop()
            except Exception as exc:
                await self._emit_cleanup_error(
                    message=f"Failed to stop audio interface: {exc}",
                    code="audio_stop_failed",
                    source="audio_interface",
                )

        await self._delete_remote_session()
        try:
            if self._transport is not None:
                await self._emit(
                    "disconnected", DisconnectedEvent(session_id=self.id, reason=reason)
                )
        finally:
            self._closed.set()

    async def _pump_input_audio(self) -> None:
        assert self._audio_interface is not None
        assert self._transport is not None
        try:
            await self._transport.wait_for_agent()
            async for chunk in self._audio_interface.input_audio():
                if self._closing:
                    return
                if not self._input_enabled:
                    continue
                await self._transport.send_audio(chunk)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            try:
                await self._emit(
                    "error",
                    VoiceAgentErrorEvent(
                        message=str(exc),
                        fatal=True,
                        code="audio_input_error",
                        source="audio_interface",
                    ),
                )
            finally:
                if self._terminate_task is None:
                    self._terminate_task = asyncio.create_task(self.close(reason="audio_input_error"))

    async def _handle_transport_event(
        self, event: VoiceEventName, payload: VoiceEvent
    ) -> None:
        if event == "transcript" and isinstance(payload, VoiceAgentTranscriptEvent):
            self._transcript[payload.id] = payload
        if self._audio_interface is not None:
            if event == "audio" and isinstance(payload, bytes):
                try:
                    await self._audio_interface.output_audio(payload)
                except Exception as exc:
                    try:
                        await self._emit(
                            "error",
                            VoiceAgentErrorEvent(
                                message=f"Failed to play agent audio: {exc}",
                                fatal=True,
                                code="audio_output_error",
                                source="audio_interface",
                            ),
                        )
                    finally:
                        if self._terminate_task is None:
                            self._terminate_task = asyncio.create_task(
                                self.close(reason="audio_output_error")
                            )
                    return
        close_on_error = (
            event == "error"
            and isinstance(payload, VoiceAgentErrorEvent)
            and payload.fatal
            and not self._closing
            and not self._closed.is_set()
            and self._terminate_task is None
        )
        try:
            await self._emit(event, payload)
        finally:
            if (
                close_on_error
                and not self._closing
                and not self._closed.is_set()
                and self._terminate_task is None
            ):
                self._terminate_task = asyncio.create_task(self.close(reason="error"))

    async def _emit(
        self,
        event: VoiceEventName,
        payload: VoiceEvent,
        *,
        log_unhandled: bool = True,
    ) -> None:
        if (
            event == "error" and isinstance(payload, VoiceAgentErrorEvent)
            and payload.fatal and self._fatal_error is None
        ):
            self._fatal_error = VoiceAgentConnectionError(payload.message, error_event=payload)
        handlers = list(self._handlers.get(event, []))
        if log_unhandled and not handlers and event == "error":
            log = logger.error if isinstance(payload, VoiceAgentErrorEvent) and payload.fatal else logger.warning
            log("voice agent error: %s", getattr(payload, "message", payload))
        for handler in handlers:
            try:
                result = handler(payload)
                if inspect.isawaitable(result):
                    await result
            except Exception:
                logger.exception("voice agent %s handler failed", event)

    async def _delete_remote_session(self) -> None:
        try:
            await self._delete_remote_session_callback(self.id)
        except Exception as exc:
            await self._emit_cleanup_error(
                message=f"Failed to delete remote voice session: {exc}",
                code="session_delete_failed",
                source="rest",
            )

    async def _emit_cleanup_error(
        self,
        *,
        message: str,
        code: str,
        source: Literal["audio_interface", "transport", "rest"],
    ) -> None:
        try:
            await self._emit(
                "error",
                VoiceAgentErrorEvent(
                    message=message,
                    fatal=False,
                    code=code,
                    source=source,
                ),
            )
        except Exception:
            logger.exception(
                "voice agent cleanup error handler failed",
                extra={"error_code": code},
            )

    async def __aenter__(self) -> VoiceAgentSession:
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()
