import httpx
import pytest
from httpx._types import AsyncByteStream, SyncByteStream

from mistralai.client import Mistral
from mistralai.client._hooks.types import AfterSuccessContext, HookContext
from mistralai.extra.exceptions import StreamDisconnectedError
from mistralai.extra.workflows.stream_error_hook import WorkflowStreamErrorHook

STREAM_OPERATION_ID = "get_stream_events_v1_workflows_events_stream_get"
NON_STREAM_OPERATION_ID = "chat_completion_v1_chat_completions_post"

GOOD_FRAME = b'event: workflow.event\ndata: {"attributes": {}}\n\n'
ERROR_FRAME = b'event: error\ndata: {"error": "boom", "reason": "read_error"}\n\n'


class _SyncSource(SyncByteStream):
    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = chunks

    def __iter__(self):
        yield from self._chunks

    def close(self) -> None:
        pass


class _AsyncSource(AsyncByteStream):
    def __init__(self, chunks: list[bytes]) -> None:
        self._iter = iter(chunks)

    def __aiter__(self) -> "_AsyncSource":
        return self

    async def __anext__(self) -> bytes:
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

    async def aclose(self) -> None:
        pass


def _hook_ctx(operation_id: str) -> AfterSuccessContext:
    client = Mistral(api_key="test-key")
    return AfterSuccessContext(
        HookContext(
            config=client.sdk_configuration,
            base_url="https://api.example.com",
            operation_id=operation_id,
            oauth2_scopes=[],
            security_source=None,
        )
    )


def _sse_response(source, *, content_type: str = "text/event-stream") -> httpx.Response:
    return httpx.Response(
        status_code=200,
        headers={"content-type": content_type},
        stream=source,
        request=httpx.Request(
            "GET", "https://api.example.com/v1/workflows/events/stream"
        ),
    )


def test_hook_raises_stream_disconnected_error_and_passes_prior_events_through():
    response = _sse_response(_SyncSource([GOOD_FRAME, ERROR_FRAME]))
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(STREAM_OPERATION_ID), response
    )
    assert isinstance(result, httpx.Response)

    collected: list[bytes] = []
    with pytest.raises(StreamDisconnectedError) as exc_info:
        for chunk in result.iter_bytes():
            collected.append(chunk)

    assert exc_info.value.reason == "read_error"
    assert exc_info.value.error == "boom"
    assert b"workflow.event" in b"".join(collected)


@pytest.mark.asyncio
async def test_hook_raises_stream_disconnected_error_on_async_stream():
    response = _sse_response(_AsyncSource([GOOD_FRAME, ERROR_FRAME]))
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(STREAM_OPERATION_ID), response
    )
    assert isinstance(result, httpx.Response)

    collected: list[bytes] = []
    with pytest.raises(StreamDisconnectedError) as exc_info:
        async for chunk in result.aiter_bytes():
            collected.append(chunk)

    assert exc_info.value.reason == "read_error"
    assert exc_info.value.error == "boom"
    assert b"workflow.event" in b"".join(collected)


def test_hook_detects_error_frame_split_across_chunks():
    chunks = [
        b"event: er",
        b'ror\ndata: {"error": "x", "reason": "internal_error"}\n\n',
    ]
    response = _sse_response(_SyncSource(chunks))
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(STREAM_OPERATION_ID), response
    )
    assert isinstance(result, httpx.Response)

    with pytest.raises(StreamDisconnectedError) as exc_info:
        list(result.iter_bytes())

    assert exc_info.value.reason == "internal_error"
    assert exc_info.value.error == "x"


def test_hook_defaults_reason_when_missing_or_invalid():
    frame = b'event: error\ndata: {"error": "no reason given"}\n\n'
    response = _sse_response(_SyncSource([frame]))
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(STREAM_OPERATION_ID), response
    )
    assert isinstance(result, httpx.Response)

    with pytest.raises(StreamDisconnectedError) as exc_info:
        list(result.iter_bytes())

    assert exc_info.value.reason == "stream_error"
    assert exc_info.value.error == "no reason given"


def test_hook_passes_normal_stream_through_without_raising():
    response = _sse_response(_SyncSource([GOOD_FRAME, GOOD_FRAME]))
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(STREAM_OPERATION_ID), response
    )
    assert isinstance(result, httpx.Response)

    body = b"".join(result.iter_bytes())
    assert body.count(b"workflow.event") == 2


def test_hook_ignores_non_stream_operations():
    source = _SyncSource([ERROR_FRAME])
    response = _sse_response(source)
    result = WorkflowStreamErrorHook().after_success(
        _hook_ctx(NON_STREAM_OPERATION_ID), response
    )

    # Response is returned untouched: same object, original stream not wrapped.
    assert result is response
    assert response.stream is source
