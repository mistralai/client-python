import json
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any

import httpx
import pytest

from mistralai.client import Mistral, errors, models
from mistralai.extra.connectors_gateway import ConnectorGatewayProtocolError


@asynccontextmanager
async def _mistral_client(
    handler: Callable[[httpx.Request], Any],
    *,
    auth: Any = None,
) -> AsyncIterator[Mistral]:
    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        auth=auth,
    )
    sync_client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(500, request=request)
        )
    )
    try:
        yield Mistral(
            api_key="test-api-key",
            server_url="https://api.example.test",
            client=sync_client,
            async_client=async_client,
        )
    finally:
        await async_client.aclose()
        sync_client.close()


@pytest.mark.asyncio
async def test_call_mcp_tool_async_calls_gateway_and_converts_result() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "content": [{"type": "text", "text": "done"}],
                    "isError": True,
                    "structuredContent": {"answer": 42},
                    "_meta": {"source": "test"},
                },
            },
        )

    async with _mistral_client(handler) as mistral:
        result = await mistral.beta.connectors.call_mcp_tool_async(
            connector_id_or_name="my/connector",
            tool_name="search",
            arguments={"query": "mistral"},
            credentials_name="work",
        )
        await mistral.beta.connectors.call_mcp_tool_async(
            connector_id_or_name="my/connector",
            tool_name="search",
        )

        assert mistral.sdk_configuration.async_client is not None

    assert len(requests) == 2
    request = requests[0]
    assert request.url.raw_path == b"/v1/connectors-gateway/my%2Fconnector/mcp"
    assert request.headers["authorization"] == "Bearer test-api-key"
    assert request.headers["x-credentials-name"] == "work"
    assert request.headers["accept"] == "application/json, text/event-stream"
    assert json.loads(request.content) == {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "search", "arguments": {"query": "mistral"}},
    }
    assert result.content[0].type == "text"
    assert result.content[0].text == "done"
    assert isinstance(result.metadata, models.ConnectorToolCallMetadata)
    assert isinstance(result.metadata.mcp_meta, models.ConnectorToolResultMetadata)
    assert result.metadata.mcp_meta.is_error is True
    assert result.metadata.mcp_meta.structured_content == {"answer": 42}
    assert result.metadata.mcp_meta.meta == {"source": "test"}


@pytest.mark.asyncio
async def test_call_mcp_tool_async_raises_sdk_error_for_http_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"detail": "Unauthorized"})

    async with _mistral_client(handler) as mistral:
        with pytest.raises(errors.SDKError) as exc_info:
            await mistral.beta.connectors.call_mcp_tool_async(
                connector_id_or_name="github",
                tool_name="search",
            )

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_call_mcp_tool_async_raises_protocol_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32602, "message": "Invalid arguments"},
            },
        )

    async with _mistral_client(handler) as mistral:
        with pytest.raises(ConnectorGatewayProtocolError) as exc_info:
            await mistral.beta.connectors.call_mcp_tool_async(
                connector_id_or_name="github",
                tool_name="search",
            )

    assert exc_info.value.code == -32602
    assert str(exc_info.value) == "Invalid arguments"


@pytest.mark.asyncio
async def test_call_http_endpoint_async_proxies_relative_request() -> None:
    captured: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            418,
            content=b"upstream response",
            headers=[("set-cookie", "a=1"), ("set-cookie", "b=2")],
        )

    connector_request = httpx.Request(
        "POST",
        "/items/search?q=hello%20world",
        headers={
            "authorization": "Bearer caller-value",
            "content-type": "application/json",
            "x-upstream-header": "value",
        },
        json={"limit": 10},
    )

    async with _mistral_client(
        handler,
        auth=httpx.BasicAuth("client", "password"),
    ) as mistral:
        response = await mistral.beta.connectors.call_http_endpoint_async(
            connector_id_or_name="http connector",
            request=connector_request,
            credentials_name="secondary",
            timeout_ms=1_234,
        )

    assert response.status_code == 418
    assert response.content == b"upstream response"
    assert response.headers.get_list("set-cookie") == ["a=1", "b=2"]

    request = captured[0]
    assert request.url.raw_path == (
        b"/v1/connectors-gateway/http%20connector/http/items/search?q=hello%20world"
    )
    assert request.headers["authorization"] == "Bearer caller-value"
    assert request.headers["x-credentials-name"] == "secondary"
    assert request.headers["x-upstream-header"] == "value"
    assert request.extensions["timeout"]["read"] == 1.234
    assert json.loads(request.content) == {"limit": 10}


@pytest.mark.asyncio
async def test_call_http_endpoint_async_does_not_follow_redirects() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(302, headers={"location": "/next"})

    async with _mistral_client(handler) as mistral:
        response = await mistral.beta.connectors.call_http_endpoint_async(
            connector_id_or_name="github",
            request=httpx.Request("GET", "/start"),
        )

    assert response.status_code == 302
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_call_http_endpoint_async_supports_sync_streaming_request() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    connector_request = httpx.Request(
        "POST",
        "/upload",
        content=iter([b"hello", b" world"]),
    )
    async with _mistral_client(handler) as mistral:
        await mistral.beta.connectors.call_http_endpoint_async(
            connector_id_or_name="files",
            request=connector_request,
        )

    assert requests[0].content == b"hello world"


@pytest.mark.asyncio
async def test_call_http_endpoint_async_rejects_absolute_url() -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    async with _mistral_client(handler) as mistral:
        with pytest.raises(
            ValueError,
            match="HTTP connector request URL must be relative",
        ):
            await mistral.beta.connectors.call_http_endpoint_async(
                connector_id_or_name="github",
                request=httpx.Request("GET", "https://api.github.com/user"),
            )

    assert requests == []


@pytest.mark.asyncio
@pytest.mark.parametrize("url", ["../models", "/items/%2e%2e/models"])
async def test_call_http_endpoint_async_rejects_dot_segments(url: str) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    async with _mistral_client(handler) as mistral:
        with pytest.raises(
            ValueError,
            match="HTTP connector request URL must not contain dot segments",
        ):
            await mistral.beta.connectors.call_http_endpoint_async(
                connector_id_or_name="github",
                request=httpx.Request("GET", url),
            )

    assert requests == []
