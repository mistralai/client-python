import asyncio
import json
import logging
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest
from livekit import rtc
from pydantic import ValidationError

from mistralai.client.models import (
    AudioSessionCreateResponse,
    AudioTurnConfig,
    VoiceAgentFunctionTool,
)
from mistralai.client.models import AudioSessionCreateResponse as SessionCreateResponse
from mistralai.extra.voice_agents import transport as transport_module
from mistralai.extra.voice_agents.errors import (
    VoiceAgentConfigurationError,
    VoiceAgentConnectionError,
)
from mistralai.extra.voice_agents.events import (
    DisconnectedEvent,
    UnknownVoiceAgentEvent,
    VoiceAgentErrorEvent,
    VoiceAgentSessionUpdatedEvent,
    VoiceAgentStateChangedEvent,
    VoiceAgentToolCallEndedEvent,
    VoiceAgentTranscriptEvent,
    parse_voice_agent_event,
)
from mistralai.extra.voice_agents.session import VoiceAgentSession
from mistralai.extra.voice_agents.tools import FunctionHandler, function_tool
from mistralai.extra.voice_agents.transport import LiveKitTransport


class FakeTransport:
    def __init__(
        self,
        *,
        start_error: Exception | None = None,
        close_error: Exception | None = None,
    ) -> None:
        self.start_error = start_error
        self.close_error = close_error
        self.close_calls = 0
        self.agent_present = asyncio.Event()
        self.sent: list[bytes] = []

    async def start(self) -> None:
        if self.start_error is not None:
            raise self.start_error

    async def wait_for_agent(self) -> None:
        await self.agent_present.wait()

    async def send_audio(self, audio: bytes) -> None:
        self.sent.append(audio)

    async def set_input_enabled(self, enabled: bool) -> None:
        return None

    async def close(self) -> None:
        self.close_calls += 1
        if self.close_error is not None:
            raise self.close_error


def make_session(*, transport: FakeTransport | None = None) -> VoiceAgentSession:
    now = datetime(2026, 9, 15, tzinfo=timezone.utc)
    session = VoiceAgentSession(
        SessionCreateResponse(
            id="vs_test",
            participant_token="token",
            server_url="wss://livekit.example.com",
            created_at=now,
            expires_at=now,
        ),
        delete_remote_session=AsyncMock(),
        audio_interface=None,
    )
    session._started = True
    session._transport = cast(Any, transport or FakeTransport())
    return session


@pytest.mark.asyncio
async def test_agent_state_change_emits_agent_state_changed_event():
    events: list[tuple[str, VoiceAgentStateChangedEvent]] = []

    async def emit(name, event):
        events.append((name, event))

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    participant = SimpleNamespace(kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT)
    transport._rtc = rtc
    transport._on_data_received(
        SimpleNamespace(
            data=b'{"type":"agent.state.changed","old_state":"idle","state":"listening","ts":1}',
            topic="voice_agent.events",
            participant=participant,
        )
    )
    await asyncio.sleep(0)

    assert events == [
        (
            "agent_state_changed",
            VoiceAgentStateChangedEvent(old_state="idle", state="listening", ts=1),
        ),
    ]


@pytest.mark.asyncio
async def test_recoverable_error_does_not_close_session():
    transport = FakeTransport()
    session = make_session(transport=transport)

    await session._handle_transport_event(
        "error",
        VoiceAgentErrorEvent(
            source="transport", message="retrying", fatal=False, code="llm_error"
        ),
    )
    await asyncio.sleep(0)

    assert not session._closed.is_set()
    assert transport.close_calls == 0

    await session.close()


@pytest.mark.asyncio
async def test_fatal_error_closes_session():
    transport = FakeTransport()
    session = make_session(transport=transport)

    await session._handle_transport_event(
        "error",
        VoiceAgentErrorEvent(
            source="transport", message="terminal", fatal=True, code="llm_error"
        ),
    )
    with pytest.raises(VoiceAgentConnectionError, match="terminal"):
        await asyncio.wait_for(session.wait(), timeout=1)

    assert transport.close_calls == 1


@pytest.mark.asyncio
async def test_fatal_error_closes_session_when_handler_raises():
    session = make_session()

    def raise_from_handler(_event: VoiceAgentErrorEvent) -> None:
        raise RuntimeError("handler failed")

    seen: list[VoiceAgentErrorEvent] = []
    session.on("error", raise_from_handler)
    session.on("error", seen.append)

    await session._handle_transport_event(
        "error",
        VoiceAgentErrorEvent(
            source="transport", code="test_error", message="terminal", fatal=True
        ),
    )
    with pytest.raises(VoiceAgentConnectionError, match="terminal"):
        await asyncio.wait_for(session.wait(), timeout=1)

    assert [event.message for event in seen] == ["terminal"]


@pytest.mark.asyncio
async def test_malformed_wire_error_is_unknown_not_a_fabricated_fatal_error():
    events = []

    async def emit(name, event):
        events.append((name, event))

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._rtc = rtc
    participant = SimpleNamespace(kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT)
    transport._on_data_received(
        b'{"type":"error","message":"missing fields"}',
        participant=participant,
        topic="voice_agent.events",
    )
    await asyncio.sleep(0)
    assert events[0][0] == "unknown"


_EXPIRED_TOKEN = (
    "engine: signal failure: client error: 401 Unauthorized - invalid "
    "authorization token: token has invalid claims: token is expired"
)
_BAD_SIGNATURE = (
    "engine: signal failure: client error: 401 Unauthorized - invalid "
    "authorization token: token signature is invalid: signature is invalid"
)
_MISSING_ROOM = "engine: signal failure: client error: 404 Not Found - requested room does not exist"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "detail,expected",
    [
        (_EXPIRED_TOKEN, "its participant token expired"),
        (_MISSING_ROOM, "has ended: its room was closed"),
        (_BAD_SIGNATURE, "rejected its participant token: .*signature is invalid"),
        ("engine: connection timeout", "Failed to connect .*connection timeout"),
    ],
    ids=["expired_token", "missing_room", "invalid_token", "other"],
)
async def test_rejected_join_raises_connection_error(monkeypatch, detail, expected):
    class RejectingRoom(rtc.Room):
        async def connect(self, *_args, **_kwargs):
            raise rtc.ConnectError(detail)

    monkeypatch.setattr(transport_module.rtc, "Room", RejectingRoom)
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())

    with pytest.raises(VoiceAgentConnectionError, match=expected) as exc_info:
        await transport.start()

    assert isinstance(exc_info.value.__cause__, rtc.ConnectError)


@pytest.mark.asyncio
async def test_room_disconnect_emits_fatal_error():
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(
        make_session()._session_response,
        emit=emit,
    )
    transport._on_disconnected(rtc.DisconnectReason.AGENT_ERROR)
    await asyncio.sleep(0)

    assert events[0].fatal is True
    assert events[0].code == "session_disconnected"
    assert events[0].source == "transport"
    assert events[0].payload == {"reason": "agent_error"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raw,expected",
    [
        (rtc.DisconnectReason.SIP_TRUNK_FAILURE, "network_failure"),
        (rtc.DisconnectReason.ROOM_DELETED, "session_ended"),
        (rtc.DisconnectReason.CONNECTION_TIMEOUT, "timeout"),
        (rtc.DisconnectReason.UNKNOWN_REASON, "unknown"),
        (9999, "unknown"),
        (None, "unknown"),
    ],
    ids=["sip_trunk", "room_deleted", "timeout", "upstream_unknown", "future", "absent"],
)
async def test_disconnect_reason_never_leaks_the_livekit_enum(raw, expected):
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._on_disconnected(raw)
    await asyncio.sleep(0)

    assert events[0].payload == {"reason": expected}
    assert expected in events[0].message


@pytest.mark.asyncio
async def test_intentional_room_disconnect_does_not_emit_error():
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(
        make_session()._session_response,
        emit=emit,
    )

    async def disconnect():
        transport._on_disconnected(rtc.DisconnectReason.CLIENT_INITIATED)

    transport._room = SimpleNamespace(disconnect=disconnect)
    await transport.close()

    assert events == []


@pytest.mark.asyncio
async def test_close_releases_livekit_handles(monkeypatch):
    """Native handles must not wait for interpreter exit, where LiveKit's
    finalizers fail with `assert dropped` once its FFI is torn down."""
    room = rtc.Room()
    room.connect = AsyncMock()
    monkeypatch.setattr(transport_module.rtc, "Room", lambda: room)
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    transport._register_function_handlers = lambda: None
    transport._publish_input_track = AsyncMock()
    await transport.start()
    audio_source = SimpleNamespace(aclose=AsyncMock())
    transport._audio_source = audio_source

    await transport.close()

    assert all(not listeners for listeners in room._events.values())
    audio_source.aclose.assert_awaited_once()
    assert transport._room is None and transport._audio_source is None


@pytest.mark.asyncio
async def test_close_releases_callers_waiting_for_the_agent():
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    waiter = asyncio.create_task(transport.wait_for_agent())
    await asyncio.sleep(0)
    assert not waiter.done()

    await transport.close()

    await asyncio.wait_for(waiter, timeout=1)


@pytest.mark.asyncio
async def test_session_update_on_a_closed_transport_fails_without_waiting():
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    await transport.close()

    with pytest.raises(VoiceAgentConnectionError, match="Voice session is not connected"):
        await asyncio.wait_for(transport.send_session_update("{}"), timeout=1)


@pytest.mark.asyncio
async def test_agent_disconnect_emits_fatal_error_and_closes_session():
    session = VoiceAgentSession(
        make_session()._session_response,
        delete_remote_session=AsyncMock(),
        audio_interface=None,
    )
    errors: list[VoiceAgentErrorEvent] = []
    disconnected: list[DisconnectedEvent] = []
    session.on("error", errors.append)
    session.on("disconnected", disconnected.append)

    session._transport = LiveKitTransport(
        session._session_response, emit=session._handle_transport_event
    )
    session._transport._rtc = rtc
    session._transport._on_participant_disconnected(
        SimpleNamespace(
            identity="agent-worker",
            kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT,
            disconnect_reason=rtc.DisconnectReason.AGENT_ERROR,
        )
    )
    with pytest.raises(VoiceAgentConnectionError, match="disconnected"):
        await asyncio.wait_for(session.wait(), timeout=1)

    assert len(errors) == 1
    assert errors[0].fatal is True
    assert errors[0].code == "agent_disconnected"
    assert errors[0].source == "transport"
    assert errors[0].payload == {"reason": "agent_error"}
    assert disconnected == [DisconnectedEvent(session_id="vs_test", reason="error")]


@pytest.mark.asyncio
async def test_agent_disconnect_during_reconnect_is_ignored_when_agent_returns():
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(
        make_session()._session_response,
        emit=emit,
    )
    transport._rtc = rtc
    agent = SimpleNamespace(
        identity="agent-worker",
        kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT,
        disconnect_reason=rtc.DisconnectReason.UNKNOWN_REASON,
    )

    # Browser LiveKit reports participant removal before the reconnect event.
    transport._on_participant_disconnected(agent)
    transport._on_reconnecting()
    await asyncio.sleep(0)
    assert events == []

    # LiveKit's participant map is authoritative after a full reconnect,
    # even when no participant_connected callback is emitted.
    transport._room = SimpleNamespace(
        remote_participants={"agent-worker": agent},
    )
    transport._on_reconnected()
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert events == []


@pytest.mark.asyncio
async def test_agent_disconnect_becomes_fatal_when_agent_does_not_return():
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(
        make_session()._session_response,
        emit=emit,
    )
    transport._rtc = rtc
    agent = SimpleNamespace(
        identity="agent-worker",
        kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT,
        disconnect_reason=rtc.DisconnectReason.UNKNOWN_REASON,
    )

    transport._on_reconnecting()
    transport._on_participant_disconnected(agent)
    await asyncio.sleep(0)
    assert events == []

    transport._on_reconnected()
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert len(events) == 1
    assert events[0].fatal is True
    assert events[0].code == "agent_disconnected"


@pytest.mark.asyncio
async def test_non_agent_disconnect_is_ignored():
    events: list[VoiceAgentErrorEvent] = []

    async def emit(name, event):
        if name == "error":
            events.append(event)

    transport = LiveKitTransport(
        make_session()._session_response,
        emit=emit,
    )
    transport._rtc = rtc
    transport._on_participant_disconnected(
        SimpleNamespace(
            identity="another-user",
            kind=rtc.ParticipantKind.PARTICIPANT_KIND_STANDARD,
            disconnect_reason=rtc.DisconnectReason.CLIENT_INITIATED,
        )
    )
    await asyncio.sleep(0)

    assert events == []


@pytest.mark.asyncio
async def test_transport_disconnects_room_before_cancelling_track_readers():
    events: list[str] = []

    async def emit(_name, _event):
        pass

    async def read_track():
        try:
            await asyncio.Future()
        finally:
            events.append("reader_closed")

    async def disconnect():
        events.append("room_disconnected")

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._room = SimpleNamespace(disconnect=disconnect)
    reader = asyncio.create_task(read_track())
    transport._tasks.add(reader)
    await asyncio.sleep(0)

    await transport.close()

    assert events == ["room_disconnected", "reader_closed"]


@pytest.mark.asyncio
async def test_transport_close_ignores_audio_reader_teardown_error():
    errors: list[VoiceAgentErrorEvent] = []
    disconnecting = asyncio.Event()

    async def emit(name, event):
        if name == "error":
            errors.append(event)

    class FailingStream:
        def __aiter__(self):
            return self

        async def __anext__(self):
            await disconnecting.wait()
            raise RuntimeError("stream closed during disconnect")

        async def aclose(self):
            return None

    async def disconnect():
        disconnecting.set()
        await asyncio.sleep(0)

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._room = SimpleNamespace(disconnect=disconnect)
    reader = asyncio.create_task(
        transport._read_track_into(
            FailingStream(), cast(Any, SimpleNamespace(push=lambda _samples: None))
        )
    )
    transport._tasks.add(reader)
    await asyncio.sleep(0)

    await transport.close()

    assert errors == []


@pytest.mark.asyncio
async def test_cleanup_error_handler_cannot_abort_remaining_teardown():
    transport = FakeTransport(close_error=RuntimeError("transport close failed"))
    session = make_session(transport=transport)
    stop_audio = AsyncMock()
    delete_session = AsyncMock()
    session._audio_interface = cast(Any, SimpleNamespace(stop=stop_audio))
    session._delete_remote_session_callback = delete_session

    def raise_from_cleanup_error(event: VoiceAgentErrorEvent) -> None:
        if event.code == "transport_close_failed":
            raise RuntimeError("handler failed")

    session.on("error", raise_from_cleanup_error)

    await session.close()
    await asyncio.wait_for(session.wait(), timeout=1)

    stop_audio.assert_awaited_once()
    delete_session.assert_awaited_once()


@pytest.mark.asyncio
async def test_disconnected_handler_cannot_prevent_wait_completion():
    session = make_session()

    def raise_from_disconnected(_event: DisconnectedEvent) -> None:
        raise RuntimeError("handler failed")

    seen: list[DisconnectedEvent] = []
    session.on("disconnected", raise_from_disconnected)
    session.on("disconnected", seen.append)

    await session.close()
    await asyncio.wait_for(session.wait(), timeout=1)

    assert [event.session_id for event in seen] == ["vs_test"]


def make_turn(
    turn_id: str, role: str, content: str, final: bool
) -> VoiceAgentTranscriptEvent:
    return VoiceAgentTranscriptEvent(
        id=turn_id,
        role=cast(Any, role),
        content=content,
        final=final,
        ts=datetime(2026, 9, 15, tzinfo=timezone.utc).timestamp(),
    )


@pytest.mark.asyncio
async def test_transcript_keeps_the_latest_turn_per_id_and_survives_close():
    session = make_session()

    await session._handle_transport_event(
        "transcript", make_turn("t1", "user", "hel", False)
    )
    await session._handle_transport_event(
        "transcript", make_turn("t2", "assistant", "hi there", True)
    )
    await session._handle_transport_event(
        "transcript", make_turn("t1", "user", "hello", True)
    )

    await session.close()

    assert [(turn.id, turn.content) for turn in session.transcript] == [
        ("t1", "hello"),
        ("t2", "hi there"),
    ]


@pytest.mark.parametrize(
    "status,result",
    [("done", '{"a": 1}'), ("error", "boom"), ("cancelled", None)],
)
def test_tool_call_ended_carries_status_and_text_result(status, result):
    payload = {
        "type": "tool_call.ended",
        "id": "c1",
        "name": "x",
        "phase": "ended",
        "ts": 1.0,
        "arguments": "{}",
        "status": status,
        "result": result,
    }
    name, event = parse_voice_agent_event(payload)
    assert name == "tool_call_ended"
    assert isinstance(event, VoiceAgentToolCallEndedEvent)
    assert event.model_dump(mode="json") == payload


@pytest.mark.asyncio
async def test_session_update_rpc_targets_agent_participant():
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    transport._rtc = rtc
    perform_rpc = AsyncMock(return_value="{}")
    transport._room = SimpleNamespace(
        remote_participants={
            "human": SimpleNamespace(
                kind=rtc.ParticipantKind.PARTICIPANT_KIND_STANDARD, attributes={}
            ),
            "agent-worker": SimpleNamespace(
                kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT, attributes={}
            ),
        },
        local_participant=SimpleNamespace(perform_rpc=perform_rpc),
    )
    transport._agent_present.set()

    await transport.send_session_update("{}")

    assert perform_rpc.await_args is not None
    assert perform_rpc.await_args.kwargs["destination_identity"] == "agent-worker"


@pytest.mark.asyncio
async def test_session_update_times_out_when_the_agent_never_joins(monkeypatch):
    monkeypatch.setattr(transport_module, "AGENT_JOIN_TIMEOUT_S", 0.01)
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    transport._rtc = rtc
    transport._room = SimpleNamespace(
        remote_participants={
            "human": SimpleNamespace(
                kind=rtc.ParticipantKind.PARTICIPANT_KIND_STANDARD, attributes={}
            ),
        },
    )

    with pytest.raises(VoiceAgentConnectionError, match="did not join within"):
        await transport.send_session_update("{}")


@pytest.mark.asyncio
async def test_session_update_waits_for_an_agent_joining_after_connect():
    transport = LiveKitTransport(make_session()._session_response, emit=AsyncMock())
    transport._rtc = rtc
    perform_rpc = AsyncMock(return_value="{}")
    transport._room = SimpleNamespace(
        remote_participants={},
        local_participant=SimpleNamespace(perform_rpc=perform_rpc),
    )

    updating = asyncio.create_task(transport.send_session_update("{}"))
    await asyncio.sleep(0)
    assert not updating.done()

    agent = SimpleNamespace(
        kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT, attributes={}
    )
    transport._room.remote_participants["agent-worker"] = agent
    transport._on_participant_connected(agent)
    await asyncio.wait_for(updating, timeout=1)

    assert perform_rpc.await_args is not None
    assert perform_rpc.await_args.kwargs["destination_identity"] == "agent-worker"


def make_update_session(
    *function_handlers: FunctionHandler, server_tools: list[dict[str, Any]]
) -> VoiceAgentSession:
    session = make_session()
    transport = LiveKitTransport(
        session._session_response, emit=AsyncMock(), function_handlers=list(function_handlers)
    )
    cast(Any, transport).send_session_update = AsyncMock(
        return_value=json.dumps(session_updated_payload(server_tools))
    )
    session._transport = transport
    return session


def session_updated_payload(tools: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "type": "session.updated",
        "ts": 1.0,
        "session": {
            "instructions": "",
            "tools": tools,
            "turn": {"allow_interruptions": True},
            "llm": {"model": "mistral-medium"},
            "stt": {
                "model": "voxtral-mini",
                "language": None,
                "context_bias": None,
                "target_streaming_delay_ms": None,
                "turn_detection": None,
            },
            "tts": {"model": "voxtral-tts", "voice_id": "alloy"},
            "welcome_message": None,
        },
    }


def call_payload(name: str) -> str:
    return json.dumps({"name": name, "arguments": {}})


@function_tool
def get_weather() -> str:
    return "sunny"


@function_tool
def get_time() -> str:
    return "noon"


@pytest.mark.asyncio
async def test_update_keeps_handlers_for_removed_tools_for_in_flight_calls():
    session = make_update_session(get_weather, server_tools=[get_time.to_wire()])

    await session.update(tools=[get_time])

    transport = cast(Any, session._transport)
    assert (
        await transport._dispatch_function_call(call_payload("get_weather")) == "sunny"
    )
    assert await transport._dispatch_function_call(call_payload("get_time")) == "noon"


@pytest.mark.asyncio
async def test_update_with_dict_declared_function_tool_keeps_existing_handler():
    session = make_update_session(get_weather, server_tools=[get_weather.to_wire()])

    await session.update(tools=[get_weather.to_wire()])

    transport = cast(Any, session._transport)
    assert (
        await transport._dispatch_function_call(call_payload("get_weather")) == "sunny"
    )


@pytest.mark.asyncio
async def test_update_only_registers_function_handlers_confirmed_by_server():
    session = make_update_session(server_tools=[{"type": "web_search"}])

    await session.update(tools=[get_time])

    with pytest.raises(rtc.RpcError) as raised:
        await cast(Any, session._transport)._dispatch_function_call(call_payload("get_time"))

    assert raised.value.code == transport_module.FUNCTION_CALL_NO_HANDLER_CODE


@pytest.mark.asyncio
async def test_malformed_function_call_is_rejected_as_a_bad_request():
    emit = AsyncMock()
    transport = LiveKitTransport(make_session()._session_response, emit=emit)

    with pytest.raises(rtc.RpcError) as raised:
        await transport._dispatch_function_call(json.dumps({"arguments": {}}))

    assert raised.value.code == transport_module.FUNCTION_CALL_INVALID_PAYLOAD_CODE
    emit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_sends_nested_turn_and_parses_nested_response():
    session = make_update_session(get_time, server_tools=[get_time.to_wire()])

    result = await session.update(
        instructions="Be brief.",
        tools=[get_time],
        turn={"allow_interruptions": False},
    )

    sent = json.loads(cast(Any, session._transport).send_session_update.await_args.args[0])
    assert sent == {
        "instructions": "Be brief.",
        "tools": [get_time.to_wire()],
        "turn": {"allow_interruptions": False},
    }
    assert isinstance(result, VoiceAgentSessionUpdatedEvent)
    config = result.session
    assert config.turn.allow_interruptions is True
    assert config.llm.model == "mistral-medium"
    assert config.stt.model == "voxtral-mini"
    assert (config.tts.model, config.tts.voice_id) == ("voxtral-tts", "alloy")
    assert [
        tool.model_dump(mode="json", exclude_unset=True) for tool in cast(Any, config.tools)
    ] == [get_time.to_wire()]


@pytest.mark.asyncio
async def test_update_does_not_emit_locally():
    # The server broadcasts session.updated to every participant, the caller
    # included, so emitting here too would deliver it twice.
    session = make_update_session(server_tools=[])
    emitted = []
    session.on("session_updated", emitted.append)

    await session.update(instructions="Be brief.")

    assert emitted == []


@pytest.mark.asyncio
async def test_update_wraps_a_malformed_server_reply():
    session = make_update_session(server_tools=[])
    cast(Any, session._transport).send_session_update = AsyncMock(
        return_value='{"type": "session.updated"}'
    )

    with pytest.raises(
        VoiceAgentConnectionError, match="Invalid session update response"
    ) as raised:
        await session.update(instructions="Be brief.")

    assert isinstance(raised.value.__cause__, ValidationError)


@pytest.mark.asyncio
async def test_session_updated_event_is_delivered_as_generated_model():
    session = make_session()
    seen = []
    session.on("session_updated", seen.append)

    name, event = parse_voice_agent_event(
        session_updated_payload([{"type": "hang_up"}])
    )

    assert name == "session_updated"
    assert isinstance(event, VoiceAgentSessionUpdatedEvent)
    await session._handle_transport_event(name, event)
    assert seen == [event]


@pytest.mark.asyncio
async def test_update_omits_unset_fields_from_payload():
    session = make_update_session(server_tools=[])

    await session.update(instructions="Be brief.")

    sent = json.loads(cast(Any, session._transport).send_session_update.await_args.args[0])
    assert sent == {"instructions": "Be brief."}


@pytest.mark.asyncio
@pytest.mark.parametrize("turn", [{}, AudioTurnConfig()])
async def test_update_empty_turn_does_not_send_defaults(turn):
    session = make_update_session(server_tools=[])

    await session.update(turn=turn)

    sent = json.loads(cast(Any, session._transport).send_session_update.await_args.args[0])
    assert sent == {"turn": {}}


@pytest.mark.asyncio
@pytest.mark.parametrize("fatal", [False, True])
async def test_backend_error_is_delivered_as_generated_model(fatal):
    session = make_session()
    seen = []
    session.on("error", seen.append)
    payload = {
        "type": "error",
        "source": "llm",
        "code": "llm_error",
        "message": "backend failure",
        "fatal": fatal,
        "payload": None,
    }
    name, event = parse_voice_agent_event(payload)
    assert isinstance(event, VoiceAgentErrorEvent)
    assert event.model_dump(mode="json") == payload
    await session._handle_transport_event(name, event)
    assert seen == [event]
    if fatal:
        with pytest.raises(VoiceAgentConnectionError) as raised:
            await asyncio.wait_for(session.wait(), timeout=1)
        assert raised.value.error_event is event
    else:
        assert not session._closed.is_set()
        await session.close()


@pytest.mark.asyncio
async def test_cleanup_errors_and_later_fatal_error_preserve_original_failure():
    session = make_session(
        transport=FakeTransport(close_error=RuntimeError("cleanup failed"))
    )
    first = VoiceAgentErrorEvent(
        source="llm", code="llm_error", message="original failure", fatal=True
    )
    later = VoiceAgentErrorEvent(
        source="transport", code="test_error", message="secondary failure", fatal=True
    )
    seen = []
    session.on("error", seen.append)
    await session._handle_transport_event("error", first)
    await session._handle_transport_event("error", later)
    with pytest.raises(VoiceAgentConnectionError) as raised:
        await asyncio.wait_for(session.wait(), timeout=1)
    assert raised.value.error_event is first
    assert any(event.code == "transport_close_failed" for event in seen)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        b"not json",
        b'{"type":"future.event","value":42}',
        b'{"type":"transcription.segment","id":"missing-fields"}',
    ],
)
async def test_unknown_protocol_payload_is_retained(payload):
    events = []

    async def emit(name, event):
        events.append((name, event))

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._rtc = rtc
    transport._on_data_received(
        SimpleNamespace(
            data=payload,
            topic="voice_agent.events",
            participant=SimpleNamespace(
                kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT
            ),
        )
    )
    await asyncio.sleep(0)
    assert len(events) == 1
    name, event = events[0]
    assert name == "unknown" and isinstance(event, UnknownVoiceAgentEvent)
    import json

    expected = json.loads(payload) if payload.startswith(b"{") else payload.decode()
    assert event.content == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "topic,kind",
    [
        ("tool_call", rtc.ParticipantKind.PARTICIPANT_KIND_AGENT),
        ("voice_agent.events", rtc.ParticipantKind.PARTICIPANT_KIND_STANDARD),
    ],
)
async def test_unrelated_topics_and_non_agent_protocol_packets_are_ignored(topic, kind):
    events = []

    async def emit(name, event):
        events.append((name, event))

    transport = LiveKitTransport(make_session()._session_response, emit=emit)
    transport._rtc = rtc
    transport._on_data_received(
        SimpleNamespace(
            data=b'{"type":"agent.state.changed","old_state":"idle","state":"listening","ts":1}',
            topic=topic,
            # A user-set lk.agent.state attribute is not proof of an agent.
            # rtc/participant.py:Participant.permissions is server-issued instead.
            participant=SimpleNamespace(
                kind=kind, attributes={"lk.agent.state": "speaking"}
            ),
        )
    )
    await asyncio.sleep(0)
    assert events == []


@pytest.mark.asyncio
async def test_error_handler_can_close_session_without_cancelling_itself():
    delete_session = AsyncMock()
    session = VoiceAgentSession(
        make_session()._session_response,
        delete_remote_session=delete_session,
        audio_interface=None,
    )

    async def close_on_error(_event):
        await session.close()

    session.on("error", close_on_error)
    session._transport = LiveKitTransport(
        session._session_response, emit=session._handle_transport_event
    )
    session._transport._rtc = rtc
    session._transport._on_data_received(
        SimpleNamespace(
            data=b'{"type":"error","source":"llm","code":"llm_error","message":"terminal","fatal":true}',
            topic="voice_agent.events",
            participant=SimpleNamespace(
                kind=rtc.ParticipantKind.PARTICIPANT_KIND_AGENT
            ),
        )
    )
    with pytest.raises(VoiceAgentConnectionError, match="terminal"):
        await asyncio.wait_for(session.wait(), timeout=1)
    delete_session.assert_awaited_once()


@pytest.mark.parametrize("source", ["llm", "transport", "audio_interface", "rest"])
def test_unified_error_parser_preserves_diagnostics(source):
    payload = {
        "type": "error",
        "source": source,
        "code": "connection_failed",
        "message": "failure",
        "fatal": True,
        "payload": {"reason": "server_shutdown", "details": {"attempts": 2}},
    }
    name, event = parse_voice_agent_event(payload)
    assert name == "error"
    assert isinstance(event, VoiceAgentErrorEvent)
    assert event.model_dump(mode="json") == payload


def test_error_export_is_the_generated_model():
    from mistralai.client.models import VoiceAgentErrorEvent as GeneratedErrorEvent
    from mistralai.extra.voice_agents import VoiceAgentErrorEvent as ExportedErrorEvent

    assert VoiceAgentErrorEvent is GeneratedErrorEvent is ExportedErrorEvent


# Connecting, cancellation, and cleanup.
@pytest.fixture
def response():
    now = datetime.now(timezone.utc)
    return AudioSessionCreateResponse(
        id="session",
        participant_token="token",
        server_url="ws://localhost",
        created_at=now,
        expires_at=now,
    )


@pytest.fixture
def runtime(monkeypatch, response):
    transport = AsyncMock()
    monkeypatch.setattr(
        transport_module, "LiveKitTransport", lambda *args, **kwargs: transport
    )
    delete = AsyncMock()
    session = VoiceAgentSession(
        response, delete_remote_session=delete, audio_interface=None
    )
    return session, delete, transport


@pytest.mark.asyncio
async def test_connect_is_idempotent_and_context_cleans_up(runtime):
    session, delete, transport = runtime
    connected = []
    session.on("connected", connected.append)
    assert session.id == "session"
    async with session:
        await asyncio.gather(session.connect(), session.connect())
    await session.close()
    await session.wait()
    transport.start.assert_awaited_once()
    transport.close.assert_awaited_once()
    delete.assert_awaited_once_with("session")
    assert len(connected) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("with_audio_handler", [False, True])
async def test_connect_warns_when_no_audio_path_is_configured(
    runtime, caplog, with_audio_handler
):
    session, _, _ = runtime
    if with_audio_handler:
        session.on("audio", lambda _chunk: None)

    with caplog.at_level(logging.WARNING):
        await session.connect()

    warned = any(
        "can neither hear nor speak" in record.getMessage()
        for record in caplog.records
    )
    assert warned is not with_audio_handler
    await session.close()


@pytest.mark.asyncio
async def test_transport_start_failure_deletes_remote_session(runtime):
    session, delete, transport = runtime
    transport.start.side_effect = RuntimeError("connection refused")
    seen = []
    session.on("error", seen.append)
    with pytest.raises(VoiceAgentConnectionError, match="connection refused"):
        await session.connect()
    delete.assert_awaited_once_with("session")
    transport.close.assert_awaited_once()
    assert seen[0].source == "transport" and seen[0].fatal
    with pytest.raises(VoiceAgentConnectionError):
        await session.wait()


@pytest.mark.asyncio
async def test_rejected_join_surfaces_from_connect(runtime):
    session, delete, transport = runtime
    transport.start.side_effect = VoiceAgentConnectionError(
        "Voice session session can no longer be joined: its participant token expired."
    )
    with pytest.raises(VoiceAgentConnectionError, match="participant token expired"):
        await session.connect()
    delete.assert_awaited_once_with("session")


@pytest.mark.asyncio
async def test_failed_partial_audio_start_is_stopped(runtime):
    session, delete, transport = runtime
    audio = AsyncMock()
    audio.start.side_effect = RuntimeError("audio failed")
    session._audio_interface = audio
    with pytest.raises(VoiceAgentConnectionError, match="audio failed"):
        await session.connect()
    audio.stop.assert_awaited_once()
    transport.close.assert_awaited_once()
    delete.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["transport", "audio_interface"])
async def test_cancelled_connect_closes_session(runtime, stage):
    session, delete, transport = runtime
    audio = AsyncMock()
    session._audio_interface = audio
    entered = asyncio.Event()

    async def hang():
        entered.set()
        await asyncio.Event().wait()

    (transport if stage == "transport" else audio).start.side_effect = hang
    connecting = asyncio.create_task(session.connect())
    await entered.wait()
    connecting.cancel()
    with pytest.raises(asyncio.CancelledError):
        await connecting
    transport.close.assert_awaited_once()
    audio.stop.assert_awaited_once()
    delete.assert_awaited_once_with("session")
    with pytest.raises(VoiceAgentConnectionError, match="closed"):
        await session.connect()


@pytest.mark.asyncio
async def test_close_without_connecting_deletes_remote_session(runtime):
    session, delete, transport = runtime
    disconnected = []
    session.on("disconnected", disconnected.append)
    await session.close()
    await session.wait()
    delete.assert_awaited_once_with("session")
    transport.start.assert_not_awaited()
    assert disconnected == []
    with pytest.raises(VoiceAgentConnectionError, match="closed"):
        await session.connect()


LIFECYCLE_CALLS = [
    lambda session: session.send_audio(b"\x00\x00"),
    lambda session: session.set_input_enabled(False),
    lambda session: session.update(instructions="Be brief."),
]
LIFECYCLE_IDS = ["send_audio", "set_input_enabled", "update"]


@pytest.mark.asyncio
@pytest.mark.parametrize("call", LIFECYCLE_CALLS, ids=LIFECYCLE_IDS)
async def test_closed_session_raises_a_typed_lifecycle_error(call):
    session = make_session()
    await session.close()

    with pytest.raises(VoiceAgentConnectionError, match="not running"):
        await call(session)


@pytest.mark.asyncio
@pytest.mark.parametrize("call", LIFECYCLE_CALLS, ids=LIFECYCLE_IDS)
async def test_unconnected_session_raises_a_typed_lifecycle_error(call):
    session = make_session()
    session._started = False

    with pytest.raises(VoiceAgentConnectionError, match=r"call connect\(\) first"):
        await call(session)


@pytest.mark.asyncio
async def test_input_pump_stops_as_soon_as_close_starts():
    transport = FakeTransport()
    transport.agent_present.set()
    session = make_session(transport=transport)

    async def chunks():
        yield b"\x00"
        session._closing = True
        yield b"\x01"

    session._audio_interface = cast(Any, SimpleNamespace(input_audio=chunks))
    await session._pump_input_audio()

    assert transport.sent == [b"\x00"]


def test_session_property_exposes_the_created_remote_session():
    session = make_session()

    assert session.session.id == session.id
    assert session.session.expires_at == datetime(2026, 9, 15, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_close_without_connecting_reports_delete_failure(runtime):
    session, delete, _ = runtime
    delete.side_effect = RuntimeError("gateway down")
    seen = []
    session.on("error", seen.append)
    await session.close()
    assert [event.code for event in seen] == ["session_delete_failed"]
    assert not seen[0].fatal
    await session.wait()


@pytest.mark.asyncio
async def test_cleanup_errors_do_not_replace_start_failure(runtime):
    session, delete, transport = runtime
    transport.start.side_effect = RuntimeError("original failure")
    transport.close.side_effect = RuntimeError("cleanup failed")
    seen = []
    session.on("error", seen.append)
    with pytest.raises(VoiceAgentConnectionError, match="original failure"):
        await session.connect()
    with pytest.raises(VoiceAgentConnectionError, match="original failure"):
        await session.wait()
    delete.assert_awaited_once()
    assert any(
        event.code == "transport_close_failed" and not event.fatal for event in seen
    )


@pytest.mark.asyncio
async def test_wait_cancellation_does_not_close_session(runtime):
    session, delete, _ = runtime
    await session.connect()
    waiting = asyncio.create_task(session.wait())
    await asyncio.sleep(0)
    waiting.cancel()
    with pytest.raises(asyncio.CancelledError):
        await waiting
    assert not session._closed.is_set()
    delete.assert_not_awaited()
    await session.close()


# Function handlers are checked against the session's function tools at connect().
def declare(name: str, *properties: str) -> VoiceAgentFunctionTool:
    return VoiceAgentFunctionTool.model_validate({
        "function": {
            "name": name,
            "parameters": {"type": "object", "properties": {p: {} for p in properties}},
        },
    })


@pytest.fixture
def lookup():
    @function_tool
    async def lookup(query: str) -> str:
        return query

    return lookup


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("declared", "handled", "message"),
    [
        (["unhandled"], False, "Function `unhandled` has no local handler"),
        ([], True, "Handler `lookup` has no function declaration"),
    ],
)
async def test_unpaired_handlers_emit_recoverable_error_and_connect(
    runtime, response, lookup, declared, handled, message
):
    session, delete, transport = runtime
    response.function_tools = [declare(name) for name in declared]
    session._function_handlers = [lookup] if handled else []
    seen, connected = [], []
    session.on("error", seen.append)
    session.on("connected", connected.append)
    await session.connect()
    assert [event.code for event in seen] == ["function_handler_configuration_error"]
    assert not seen[0].fatal and message in seen[0].message
    assert len(connected) == 1
    transport.start.assert_awaited_once()
    delete.assert_not_awaited()
    await session.close()


@pytest.mark.asyncio
async def test_matching_handlers_emit_nothing(runtime, response, lookup):
    session, _, _ = runtime
    response.function_tools = [declare("lookup", "query")]
    session._function_handlers = [lookup]
    seen = []
    session.on("error", seen.append)
    await session.connect()
    assert seen == []
    await session.close()


@pytest.mark.asyncio
async def test_handler_signature_mismatch_raises_and_closes(runtime, response, lookup):
    session, delete, transport = runtime
    response.function_tools = [declare("lookup", "q")]
    session._function_handlers = [lookup]
    with pytest.raises(VoiceAgentConfigurationError, match="does not accept q"):
        await session.connect()
    transport.start.assert_not_awaited()
    delete.assert_awaited_once_with("session")
