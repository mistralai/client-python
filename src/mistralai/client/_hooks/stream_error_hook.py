import json
import re
from typing import Any, AsyncIterator, Dict, Iterator, Optional, Tuple, Union, get_args

import httpx
from httpx._types import AsyncByteStream, SyncByteStream

from .types import AfterSuccessContext, AfterSuccessHook
from mistralai.extra.exceptions import (
    StreamDisconnectReason,
    StreamDisconnectedError,
)

# Operation IDs of the SSE-backed workflow stream endpoints that can emit a
# terminal ``event: error`` frame (event, execution, and logs streams).
STREAM_OPERATIONS_WITH_ERROR_EVENT = {
    "get_stream_events_v1_workflows_events_stream_get",
    "stream_v1_workflows_executions__execution_id__stream_get",
    "stream_deployment_logs",
    "stream_workflow_execution_logs",
}

_ERROR_EVENT = "error"
_VALID_REASONS = get_args(StreamDisconnectReason)
_DEFAULT_REASON: StreamDisconnectReason = "stream_error"

# SSE frame boundaries (blank line), longest first so the full separator is consumed.
_BOUNDARIES = [
    b"\r\n\r\n",
    b"\r\n\r",
    b"\r\n\n",
    b"\r\r\n",
    b"\n\r\n",
    b"\r\r",
    b"\n\r",
    b"\n\n",
]


def _find_boundary(buffer: bytearray) -> Optional[Tuple[int, int]]:
    """Return (index, length) of the earliest frame boundary, or None if incomplete."""
    best: Optional[Tuple[int, int]] = None
    for boundary in _BOUNDARIES:
        idx = buffer.find(boundary)
        if idx == -1:
            continue
        if (
            best is None
            or idx < best[0]
            or (idx == best[0] and len(boundary) > best[1])
        ):
            best = (idx, len(boundary))
    return best


def _parse_error_payload(data: str) -> Tuple[str, StreamDisconnectReason]:
    payload: Dict[str, Any] = {}
    try:
        # strict=False: SSE joins multi-line data with "\n", so a value spanning
        # several data: lines contains literal newlines that strict JSON rejects.
        parsed = json.loads(data.strip(), strict=False)
        if isinstance(parsed, dict):
            payload = parsed
    except json.JSONDecodeError:
        pass
    error = str(payload.get("error", data.strip()))
    reason = payload.get("reason", _DEFAULT_REASON)
    if reason not in _VALID_REASONS:
        reason = _DEFAULT_REASON
    return error, reason


def _raise_if_error_frame(block: bytes) -> None:
    """Raise StreamDisconnectedError if the SSE frame is an ``event: error`` frame."""
    event_name: Optional[str] = None
    data = ""
    for line in re.split(r"\r?\n|\r", block.decode("utf-8", errors="replace")):
        if not line or line.startswith(":"):
            continue
        field, _, value = line.partition(":")
        if value.startswith(" "):
            value = value[1:]
        if field == "event":
            event_name = value
        elif field == "data":
            data += value + "\n"

    if event_name != _ERROR_EVENT:
        return

    error, reason = _parse_error_payload(data)
    raise StreamDisconnectedError(reason=reason, error=error)


class _FrameScanner:
    """Buffers raw SSE bytes, raising on error frames and passing others through."""

    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> Iterator[bytes]:
        self._buffer += chunk
        while True:
            found = _find_boundary(self._buffer)
            if found is None:
                return
            idx, length = found
            block = bytes(self._buffer[:idx])
            frame = bytes(self._buffer[: idx + length])
            del self._buffer[: idx + length]
            _raise_if_error_frame(block)
            yield frame

    def flush(self) -> Iterator[bytes]:
        if not self._buffer:
            return
        block = bytes(self._buffer)
        self._buffer.clear()
        _raise_if_error_frame(block)
        yield block


class _ErrorDetectingSyncByteStream(SyncByteStream):
    def __init__(self, original: SyncByteStream) -> None:
        self._original = original
        self._scanner = _FrameScanner()

    def __iter__(self) -> Iterator[bytes]:
        for chunk in self._original:
            yield from self._scanner.feed(chunk)
        yield from self._scanner.flush()

    def close(self) -> None:
        self._original.close()


class _ErrorDetectingAsyncByteStream(AsyncByteStream):
    def __init__(self, original: AsyncByteStream) -> None:
        self._original = original
        self._scanner = _FrameScanner()

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self._original:
            for frame in self._scanner.feed(chunk):
                yield frame
        for frame in self._scanner.flush():
            yield frame

    async def aclose(self) -> None:
        await self._original.aclose()


class WorkflowStreamErrorHook(AfterSuccessHook):
    """Raise StreamDisconnectedError when a workflow SSE stream sends an error frame.

    Wraps the response byte stream for the workflow SSE operations so that an
    ``event: error`` frame raises during iteration, terminating the consumer's
    ``for event in stream`` loop instead of yielding the error as a normal event.
    """

    def after_success(
        self,
        hook_ctx: AfterSuccessContext,
        response: httpx.Response,
    ) -> Union[httpx.Response, Exception]:
        if hook_ctx.operation_id not in STREAM_OPERATIONS_WITH_ERROR_EVENT:
            return response
        if "text/event-stream" not in response.headers.get("content-type", ""):
            return response

        stream = response.stream
        wrapped: Union[SyncByteStream, AsyncByteStream]
        if isinstance(stream, AsyncByteStream):
            wrapped = _ErrorDetectingAsyncByteStream(stream)
        elif isinstance(stream, SyncByteStream):
            wrapped = _ErrorDetectingSyncByteStream(stream)
        else:
            return response

        # Keep the original headers: this hook forwards the raw stream unchanged,
        # so httpx still applies any Content-Encoding when the consumer iterates.
        return httpx.Response(
            status_code=response.status_code,
            headers=response.headers,
            stream=wrapped,
            request=response.request,
            extensions=response.extensions,
        )
