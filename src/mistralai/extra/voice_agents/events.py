"""Generated backend messages plus SDK-local lifecycle notifications."""

from typing import Any, Literal, Union

from mistralai.client.models import State as AgentState
from mistralai.client.models import (
    VoiceAgentErrorEvent,
    VoiceAgentSessionUpdatedEvent,
    VoiceAgentStateChangedEvent,
    VoiceAgentToolCallEndedEvent,
    VoiceAgentToolCallStartedEvent,
    VoiceAgentTranscriptEvent,
)
from pydantic import BaseModel

__all__ = [
    "AgentState",
    "VoiceAgentToolCallStartedEvent",
    "VoiceAgentToolCallEndedEvent",
    "VoiceAgentErrorEvent",
    "VoiceAgentTranscriptEvent",
    "VoiceAgentStateChangedEvent",
    "VoiceAgentSessionUpdatedEvent",
    "ConnectedEvent",
    "DisconnectedEvent",
    "UnhandledToolEvent",
    "UnknownVoiceAgentEvent",
    "VoiceEvent",
    "VoiceEventName",
    "DisconnectReason",
    "TransportDisconnectReason",
]

DisconnectReason = Literal[
    "user_interrupt",
    "start_failed",
    "audio_input_error",
    "audio_output_error",
    "error",
]

# Why the media plane dropped, not why the session stopped (DisconnectReason).
# Closed and ours so the media vendor's enum never becomes our contract.
TransportDisconnectReason = Literal[
    "client_closed",
    "server_closed",
    "session_ended",
    "agent_error",
    "timeout",
    "network_failure",
    "unknown",
]


class ConnectedEvent(BaseModel):
    session_id: str


class DisconnectedEvent(BaseModel):
    session_id: str
    reason: DisconnectReason | None = None


class UnhandledToolEvent(BaseModel):
    name: str
    arguments: str | dict[str, Any] | None = None


class UnknownVoiceAgentEvent(BaseModel):
    type: str | None
    content: Any
    error: str


VoiceEventName = Literal[
    "connected",
    "disconnected",
    "transcript",
    "audio",
    "tool_call_started",
    "tool_call_ended",
    "unhandled_tool",
    "agent_state_changed",
    "error",
    "session_updated",
    "unknown",
]
VoiceEvent = Union[
    bytes,
    ConnectedEvent,
    DisconnectedEvent,
    UnhandledToolEvent,
    UnknownVoiceAgentEvent,
    VoiceAgentToolCallStartedEvent,
    VoiceAgentToolCallEndedEvent,
    VoiceAgentErrorEvent,
    VoiceAgentTranscriptEvent,
    VoiceAgentStateChangedEvent,
    VoiceAgentSessionUpdatedEvent,
]

_MESSAGE_MODELS: dict[
    str,
    type[VoiceAgentToolCallStartedEvent]
    | type[VoiceAgentToolCallEndedEvent]
    | type[VoiceAgentErrorEvent]
    | type[VoiceAgentTranscriptEvent]
    | type[VoiceAgentStateChangedEvent]
    | type[VoiceAgentSessionUpdatedEvent],
] = {
    "tool_call.started": VoiceAgentToolCallStartedEvent,
    "tool_call.ended": VoiceAgentToolCallEndedEvent,
    "error": VoiceAgentErrorEvent,
    "transcription.segment": VoiceAgentTranscriptEvent,
    "agent.state.changed": VoiceAgentStateChangedEvent,
    "session.updated": VoiceAgentSessionUpdatedEvent,
}
_EVENT_NAMES: dict[str, VoiceEventName] = {
    "tool_call.started": "tool_call_started",
    "tool_call.ended": "tool_call_ended",
    "error": "error",
    "transcription.segment": "transcript",
    "agent.state.changed": "agent_state_changed",
    "session.updated": "session_updated",
}


def parse_voice_agent_event(payload: Any) -> tuple[VoiceEventName, VoiceEvent]:
    """Preserve known wire models exactly; unknown/invalid messages remain inspectable."""
    if not isinstance(payload, dict):
        return "unknown", UnknownVoiceAgentEvent(
            type=None, content=payload, error="expected JSON object"
        )
    kind = payload.get("type")
    if not isinstance(kind, str) or kind not in _MESSAGE_MODELS:
        return "unknown", UnknownVoiceAgentEvent(
            type=kind if isinstance(kind, str) else None,
            content=payload,
            error="unknown event type",
        )
    try:
        event = _MESSAGE_MODELS[kind].model_validate(payload)
    except ValueError as exc:
        return "unknown", UnknownVoiceAgentEvent(
            type=kind, content=payload, error=str(exc)
        )
    return _EVENT_NAMES[kind], event
