from __future__ import annotations

from typing import Literal

from mistralai.extra.exceptions import MistralClientException

StreamDisconnectReason = Literal["read_error", "stream_error", "internal_error"]


class StreamDisconnectedError(MistralClientException):
    """Raised when a workflow SSE stream is terminated by a server error frame.

    The server ends a stream by emitting an ``event: error`` SSE frame. The SDK
    surfaces this as a raised exception so consumers can wrap stream iteration in
    ``try`` / ``except`` instead of inspecting each event for ``event == "error"``.

    Both attributes are populated from the frame's ``data`` JSON payload.
    """

    def __init__(self, *, reason: StreamDisconnectReason, error: str) -> None:
        self.reason: StreamDisconnectReason = reason
        self.error = error
        super().__init__("Workflow stream disconnected by server")
