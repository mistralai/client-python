from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union, TYPE_CHECKING
import typing

from mistralai.client.models import (
    FunctionCallEntryArguments,
    FunctionResultEntry,
    FunctionCallEntry,
)

if TYPE_CHECKING:
    from mistralai.client.models import RealtimeTranscriptionError
    from mistralai.extra.run.result import RunOutputEntries


class MistralClientException(Exception):
    """Base exception for client errors."""


class RunException(MistralClientException):
    """Conversation run errors."""


class MCPException(MistralClientException):
    """MCP operation errors."""


class MCPAuthException(MCPException):
    """MCP authentication errors."""


class DeferralReason(str, Enum):
    """Reason why a tool call was deferred."""

    CONFIRMATION_REQUIRED = "confirmation_required"
    SERVER_SIDE_CONFIRMATION_REQUIRED = "server_side_confirmation_required"


@dataclass
class DeferredToolCallConfirmation:
    """Response indicating the tool call is approved for execution."""

    tool_call_id: str
    tool_name: str
    function_call: FunctionCallEntry
    override_args: Optional[dict[str, Any]] = None
    deferral_reason: Optional[DeferralReason] = None


@dataclass
class DeferredToolCallRejection:
    """Response indicating tool should not be executed."""

    tool_call_id: str
    message: str = "Rejected by user"
    deferral_reason: Optional[DeferralReason] = None


DeferredToolCallResponse = Union[
    DeferredToolCallConfirmation, DeferredToolCallRejection
]


class FunctionCallSchema(typing.TypedDict):
    id: str | None
    tool_call_id: str
    name: str
    arguments: FunctionCallEntryArguments


class DeferredToolCallEntrySchema(typing.TypedDict):
    tool_call_id: str
    tool_name: str
    arguments: FunctionCallEntryArguments
    reason: str
    metadata: dict[str, Any]
    function_call: FunctionCallSchema


class DeferredToolCallEntry:
    """Represents a tool call that requires confirmation."""

    def __init__(
        self,
        function_call: FunctionCallEntry,
        reason: DeferralReason = DeferralReason.CONFIRMATION_REQUIRED,
        metadata: Optional[dict[str, Any]] = None,
    ):
        self.function_call = function_call
        self.tool_call_id = function_call.tool_call_id
        self.tool_name = function_call.name
        self.arguments = function_call.arguments
        self.reason = reason
        self.metadata = metadata or {}

    def to_function_result(self, result: str) -> dict[str, str]:
        """Convert to function result dict for use as input."""
        return {
            "tool_call_id": self.tool_call_id,
            "result": result,
        }

    def confirm(
        self, override_args: Optional[dict[str, str]] = None
    ) -> DeferredToolCallConfirmation:
        """Create a confirmation response for this tool call."""
        return DeferredToolCallConfirmation(
            tool_call_id=self.tool_call_id,
            tool_name=self.tool_name,
            function_call=self.function_call,
            override_args=override_args,
            deferral_reason=self.reason,
        )

    def reject(self, message: str = "Rejected by user") -> DeferredToolCallRejection:
        """Create a rejection response for this tool call."""
        return DeferredToolCallRejection(
            tool_call_id=self.tool_call_id,
            message=message,
            deferral_reason=self.reason,
        )

    def to_dict(self) -> DeferredToolCallEntrySchema:
        """Serialize to a JSON-serializable dictionary for stateless scenarios."""
        return {
            "tool_call_id": self.tool_call_id,
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "reason": self.reason.value,
            "metadata": self.metadata,
            "function_call": {
                "id": self.function_call.id,
                "tool_call_id": self.function_call.tool_call_id,
                "name": self.function_call.name,
                "arguments": self.function_call.arguments,
            },
        }

    @classmethod
    def from_dict(cls, data: DeferredToolCallEntrySchema) -> DeferredToolCallEntry:
        """Deserialize from a dictionary."""
        function_call = FunctionCallEntry(
            id=data["function_call"].get("id"),
            tool_call_id=data["function_call"]["tool_call_id"],
            name=data["function_call"]["name"],
            arguments=data["function_call"]["arguments"],
        )
        return cls(
            function_call=function_call,
            reason=DeferralReason(
                data.get("reason", DeferralReason.CONFIRMATION_REQUIRED.value)
            ),
            metadata=data.get("metadata", {}),
        )


class DeferredToolCallsExceptionSchema(typing.TypedDict):
    conversation_id: str | None
    deferred_calls: list[DeferredToolCallEntrySchema]
    outputs: list[dict[str, Any]]
    executed_results: list[dict[str, Any]]


class DeferredToolCallsException(RunException):
    """Exception raised when tool calls require human confirmation."""

    def __init__(
        self,
        conversation_id: str | None,
        deferred_calls: list[DeferredToolCallEntry],
        outputs: list[RunOutputEntries] | None = None,
        executed_results: list[FunctionResultEntry] | None = None,
    ):
        self.conversation_id = conversation_id
        self.deferred_calls = deferred_calls
        self.outputs = outputs or []
        self.executed_results = executed_results or []
        super().__init__(
            f"Deferred tool calls requiring confirmation: {[dc.tool_name for dc in deferred_calls]}"
        )

    def to_dict(self) -> DeferredToolCallsExceptionSchema:
        """Serialize to a JSON-serializable dictionary for stateless scenarios."""
        return {
            "conversation_id": self.conversation_id,
            "deferred_calls": [dc.to_dict() for dc in self.deferred_calls],
            "outputs": [entry.model_dump(mode="json") for entry in self.outputs],
            "executed_results": [
                entry.model_dump(mode="json") for entry in self.executed_results
            ],
        }

    @classmethod
    def from_dict(
        cls, data: DeferredToolCallsExceptionSchema
    ) -> DeferredToolCallsException:
        """Deserialize from a dictionary."""
        from pydantic import BaseModel
        from mistralai.client.models import (
            MessageOutputEntry,
            FunctionCallEntry,
            FunctionResultEntry,
            AgentHandoffEntry,
            ToolExecutionEntry,
        )

        output_entry_types: dict[str, type[BaseModel]] = {
            "message.output": MessageOutputEntry,
            "function.call": FunctionCallEntry,
            "function.result": FunctionResultEntry,
            "agent.handoff": AgentHandoffEntry,
            "tool.execution": ToolExecutionEntry,
        }

        deferred_calls = [
            DeferredToolCallEntry.from_dict(dc_data)
            for dc_data in data["deferred_calls"]
        ]

        outputs: list[RunOutputEntries] = []
        for entry_data in data.get("outputs", []):
            entry_type = entry_data.get("type")
            if isinstance(entry_type, str):
                model_cls = output_entry_types.get(entry_type)
                if model_cls is not None:
                    outputs.append(
                        typing.cast(
                            "RunOutputEntries", model_cls.model_validate(entry_data)
                        )
                    )

        executed_results = [
            FunctionResultEntry.model_validate(r)
            for r in data.get("executed_results", [])
        ]

        return cls(
            conversation_id=data["conversation_id"],
            deferred_calls=deferred_calls,
            outputs=outputs,
            executed_results=executed_results,
        )


class RealtimeTranscriptionException(MistralClientException):
    """Base realtime transcription exception."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[int] = None,
        payload: Optional[object] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.payload = payload


class RealtimeTranscriptionWSError(RealtimeTranscriptionException):
    def __init__(
        self,
        message: str,
        *,
        payload: Optional["RealtimeTranscriptionError"] = None,
        raw: Optional[object] = None,
    ) -> None:
        code: Optional[int] = None
        if payload is not None:
            try:
                maybe_code = getattr(payload.error, "code", None)
                if isinstance(maybe_code, int):
                    code = maybe_code
            except Exception:
                code = None

        super().__init__(
            message, code=code, payload=payload if payload is not None else raw
        )
        self.payload_typed = payload
        self.payload_raw = raw
