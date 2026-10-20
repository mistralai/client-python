from __future__ import annotations

from typing import TYPE_CHECKING

from mistralai.extra.exceptions import MistralClientException


if TYPE_CHECKING:
    from .events import VoiceAgentErrorEvent


class VoiceAgentError(MistralClientException):
    """Base voice agent SDK error."""


class VoiceAgentConnectionError(VoiceAgentError):
    """Raised when a voice session cannot connect or stream audio."""

    def __init__(
        self,
        message: str,
        *,
        error_event: VoiceAgentErrorEvent | None = None,
    ) -> None:
        super().__init__(message)
        self.error_event = error_event


class VoiceAgentDependencyError(VoiceAgentError):
    """Raised when an optional voice dependency is not installed."""


class VoiceAgentConfigurationError(VoiceAgentError):
    """Invalid tool overrides or incomplete saved-agent configuration."""
