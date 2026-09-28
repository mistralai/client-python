import json
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any

import anyio
import httpx2 as httpx
import pytest
from mcp import ClientSession
from mcp.types import TextContent

from mistralai.client import Mistral
from mistralai.extra import connectors_gateway
from mistralai.extra.connectors_gateway import ConnectorsGatewayError
from mistralai.extra.connectors_gateway_errors import (
    raise_connectors_gateway_error,
)

ConnectorClientHandler = Callable[[httpx.Request], Any]
ConnectorClientTransport = Callable[[ConnectorClientHandler], None]

# Contract source: connectors-gateway/connectors_gateway/helpers/proxy_status.py,
# proxy_status_headers(). Connector upstream values are stripped by
# connectors-gateway/connectors_gateway/helpers/http_headers.py.
CONNECTORS_GATEWAY_ERROR_HEADER = (
    "connectors-gateway; error=http_request_error; status-code=400; "
    'details="connector_protocol_mismatch"'
)


@pytest.fixture
def use_connector_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> ConnectorClientTransport:
    def install(handler: ConnectorClientHandler) -> None:
        def new_httpx_client(**kwargs: Any) -> httpx.AsyncClient:
            return httpx.AsyncClient(
                **kwargs,
                transport=httpx.MockTransport(handler),
            )

        monkeypatch.setattr(
            connectors_gateway,
            "_new_httpx_client",
            new_httpx_client,
        )

    return install


@asynccontextmanager
async def _mistral_client(
    handler: Callable[[httpx.Request], Any],
    *,
    api_key: Any = "test-api-key",
    auth: Any = None,
    timeout_ms: int | None = None,
) -> AsyncIterator[Mistral]:
    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        auth=auth,
        cookies={"sdk-cookie": "preserved"},
    )
    sync_client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(500, request=request)
        )
    )
    try:
        yield Mistral(
            api_key=api_key,
            server_url="https://api.example.test",
            client=sync_client,
            async_client=async_client,
            timeout_ms=timeout_ms,
        )
    finally:
        await async_client.aclose()
        sync_client.close()


@pytest.mark.asyncio
async def test_mcp_client_opens_official_session_through_gateway(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        payload = json.loads(request.content)
        method = payload["method"]
        result: dict[str, Any]

        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "initialize":
            result = {
                "protocolVersion": payload["params"]["protocolVersion"],
                "capabilities": {},
                "serverInfo": {"name": "connector-gateway", "version": "test"},
            }
        elif method == "tools/call":
            result = {
                "content": [{"type": "text", "text": "done"}],
                "isError": False,
                "structuredContent": {"answer": 42},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "search",
                        "inputSchema": {"type": "object"},
                        "outputSchema": {"type": "object"},
                    }
                ]
            }
        else:
            raise AssertionError(f"Unexpected MCP method: {method}")

        return httpx.Response(
            200,
            headers={"content-type": "application/json"},
            json={"jsonrpc": "2.0", "id": payload["id"], "result": result},
        )

    use_connector_transport(handler)

    async with _mistral_client(
        handler,
        auth=httpx.BasicAuth("client", "password"),
        timeout_ms=1_234,
    ) as mistral:
        async with mistral.beta.connectors.mcp_client(
            connector_id_or_name="my/connector",
            credentials_name="work",
        ) as client:
            assert type(client) is ClientSession
            result = await client.call_tool("search", {"query": "mistral"})

    assert isinstance(result.content[0], TextContent)
    assert result.content[0].text == "done"
    assert result.structured_content == {"answer": 42}
    assert [json.loads(request.content)["method"] for request in requests] == [
        "initialize",
        "notifications/initialized",
        "tools/call",
        "tools/list",
    ]
    for request in requests:
        assert request.url.raw_path == b"/v1/connectors-gateway/my%2Fconnector/mcp"
        assert request.headers["authorization"] == "Bearer test-api-key"
        assert request.headers["x-credentials-name"] == "work"
        assert request.headers["accept"] == "application/json, text/event-stream"
        assert request.extensions["timeout"] == {
            "connect": 1.234,
            "read": 300,
            "write": 1.234,
            "pool": 1.234,
        }


@pytest.mark.asyncio
async def test_mcp_client_raises_connectors_gateway_error_during_initialization(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            headers={"proxy-status": CONNECTORS_GATEWAY_ERROR_HEADER},
            json={"detail": "The connector does not support MCP"},
        )

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        with pytest.raises(ConnectorsGatewayError) as exc_info:
            with anyio.fail_after(1):
                async with mistral.beta.connectors.mcp_client(
                    connector_id_or_name="http-only",
                ):
                    pass

    error = exc_info.value
    assert isinstance(error, httpx.HTTPStatusError)
    assert error.response.status_code == 400
    assert error.response.json() == {"detail": "The connector does not support MCP"}
    assert error.proxy_status == CONNECTORS_GATEWAY_ERROR_HEADER
    assert error.proxy_error == "http_request_error"
    assert error.proxy_status_code == 400
    assert error.details == "connector_protocol_mismatch"


@pytest.mark.asyncio
async def test_mcp_client_raises_connectors_gateway_error_for_tool_call(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        method = payload["method"]
        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "initialize":
            return httpx.Response(
                200,
                headers={"content-type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": payload["id"],
                    "result": {
                        "protocolVersion": payload["params"]["protocolVersion"],
                        "capabilities": {},
                        "serverInfo": {
                            "name": "connector-gateway",
                            "version": "test",
                        },
                    },
                },
            )
        if method == "tools/call":
            return httpx.Response(
                502,
                headers={
                    "proxy-status": (
                        "connectors-gateway; error=destination_unavailable; "
                        'details="upstream_unavailable"'
                    )
                },
                json={"detail": "Upstream MCP server unavailable"},
            )
        if method == "tools/list":
            return httpx.Response(
                200,
                headers={"content-type": "application/json"},
                json={
                    "jsonrpc": "2.0",
                    "id": payload["id"],
                    "result": {"tools": []},
                },
            )
        raise AssertionError(f"Unexpected MCP method: {method}")

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        with pytest.raises(ConnectorsGatewayError) as exc_info:
            with anyio.fail_after(1):
                async with mistral.beta.connectors.mcp_client(
                    connector_id_or_name="unavailable",
                ) as client:
                    await client.call_tool("search", {"query": "mistral"})

    error = exc_info.value
    assert error.response.status_code == 502
    assert error.proxy_error == "destination_unavailable"
    assert error.proxy_status_code is None
    assert error.details == "upstream_unavailable"


@pytest.mark.asyncio
async def test_http_client_targets_connector_gateway(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    captured: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            418,
            content=b"upstream response",
            headers=[("set-cookie", "a=1"), ("set-cookie", "b=2")],
        )

    use_connector_transport(handler)

    async with _mistral_client(
        handler,
        auth=httpx.BasicAuth("client", "password"),
        timeout_ms=1_234,
    ) as mistral:
        sdk_http_client = mistral.sdk_configuration.async_client
        assert isinstance(sdk_http_client, httpx.AsyncClient)

        async with mistral.beta.connectors.http_client(
            connector_id_or_name="http connector",
            credentials_name="secondary",
        ) as client:
            assert isinstance(client, httpx.AsyncClient)
            assert client.base_url == httpx.URL(
                "https://api.example.test/v1/connectors-gateway/"
                "http%20connector/http/"
            )
            response = await client.post(
                "/items/search?q=hello%20world",
                headers={
                    "authorization": "Bearer caller-value",
                    "content-type": "application/json",
                    "x-upstream-header": "value",
                },
                json={"limit": 10},
            )
            assert client.cookies.get("a") == "1"
            assert client.cookies.get("b") == "2"

        assert not sdk_http_client.is_closed
        assert sdk_http_client.cookies.get("sdk-cookie") == "preserved"
        assert sdk_http_client.cookies.get("a") is None
        assert sdk_http_client.cookies.get("b") is None

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
async def test_http_client_raises_connectors_gateway_error(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            headers={"proxy-status": CONNECTORS_GATEWAY_ERROR_HEADER},
            json={"detail": "The connector does not support HTTP"},
        )

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="mcp-only",
        ) as client:
            with pytest.raises(ConnectorsGatewayError) as exc_info:
                await client.get("test")

    error = exc_info.value
    assert isinstance(error, httpx.HTTPStatusError)
    assert str(error) == (
        "Connectors Gateway request failed with status 400: "
        "connector_protocol_mismatch"
    )
    assert error.request.url.path.endswith("/mcp-only/http/test")
    assert error.response.json() == {"detail": "The connector does not support HTTP"}
    assert error.proxy_status == CONNECTORS_GATEWAY_ERROR_HEADER
    assert error.proxy_error == "http_request_error"
    assert error.proxy_status_code == 400
    assert error.details == "connector_protocol_mismatch"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("proxy_status", "expected"),
    [
        pytest.param(
            CONNECTORS_GATEWAY_ERROR_HEADER,
            ("http_request_error", 400, "connector_protocol_mismatch"),
            id="canonical",
        ),
        pytest.param(
            'connectors-gateway; details="rate_limit_reached"; '
            "error=http_request_denied",
            ("http_request_denied", None, "rate_limit_reached"),
            id="reordered",
        ),
        pytest.param(
            'connectors-gateway; error=destination_unavailable; next-hop="api.test"; '
            'details="upstream_unavailable"; received-status=503',
            ("destination_unavailable", None, "upstream_unavailable"),
            id="extra-parameters",
        ),
        pytest.param(
            "connectors-gateway; error=proxy_internal_error",
            ("proxy_internal_error", None, None),
            id="no-details",
        ),
        pytest.param(
            'cdn; error=dns_timeout, "edge proxy", '
            'connectors-gateway; error=connection_timeout; details="upstream_timeout"',
            ("connection_timeout", None, "upstream_timeout"),
            id="after-other-members",
        ),
        pytest.param(
            r'connectors-gateway; error=http_request_error; details="a \"b\" \\ c"',
            ("http_request_error", None, 'a "b" \\ c'),
            id="escaped-string",
        ),
        pytest.param(
            'upstream-proxy; error=connection_refused; details="origin"',
            None,
            id="other-proxy",
        ),
        pytest.param(
            'upstream; details="x, connectors-gateway; error=http_request_denied"',
            None,
            id="lookalike-inside-string",
        ),
        pytest.param(
            "connectors-gateway; received-status=200",
            None,
            id="no-error",
        ),
    ],
)
async def test_raise_connectors_gateway_error_parses_proxy_status(
    proxy_status: str,
    expected: tuple[str, int | None, str | None] | None,
) -> None:
    response = httpx.Response(
        502,
        headers={"proxy-status": proxy_status},
        request=httpx.Request("GET", "https://api.example.test"),
    )

    if expected is None:
        await raise_connectors_gateway_error(response)
        return
    with pytest.raises(ConnectorsGatewayError) as exc_info:
        await raise_connectors_gateway_error(response)

    error = exc_info.value
    assert (error.proxy_error, error.proxy_status_code, error.details) == expected


@pytest.mark.asyncio
async def test_http_client_ignores_other_proxy_status_members(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            502,
            headers={
                "proxy-status": (
                    'upstream-proxy; error=connection_refused; details="origin"'
                )
            },
        )

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="github",
        ) as client:
            response = await client.get("test")

    assert response.status_code == 502
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        response.raise_for_status()
    assert not isinstance(exc_info.value, ConnectorsGatewayError)


@pytest.mark.asyncio
async def test_http_client_does_not_follow_redirects_by_default(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(302, headers={"location": "/next"})

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="github",
        ) as client:
            response = await client.get("start")

    assert response.status_code == 302
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_http_client_rejects_absolute_urls(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="github",
        ) as client:
            with pytest.raises(
                ValueError,
                match="must target the configured connector",
            ):
                await client.get("https://api.github.com/user")

    assert requests == []


@pytest.mark.asyncio
@pytest.mark.parametrize("url", ["../models", "/items/%2e%2e/models"])
async def test_http_client_rejects_paths_outside_connector(
    url: str,
    use_connector_transport: ConnectorClientTransport,
) -> None:
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    use_connector_transport(handler)

    async with _mistral_client(handler) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="github",
        ) as client:
            with pytest.raises(
                ValueError,
                match="must target the configured connector",
            ):
                await client.get(url)

    assert requests == []


@pytest.mark.asyncio
async def test_http_client_resolves_callable_api_key_for_each_request(
    use_connector_transport: ConnectorClientTransport,
) -> None:
    authorization_headers: list[str] = []
    api_key = {"value": "first-key"}

    async def handler(request: httpx.Request) -> httpx.Response:
        authorization_headers.append(request.headers["authorization"])
        return httpx.Response(200)

    use_connector_transport(handler)

    async with _mistral_client(
        handler,
        api_key=lambda: api_key["value"],
    ) as mistral:
        async with mistral.beta.connectors.http_client(
            connector_id_or_name="github",
        ) as client:
            await client.get("first")
            api_key["value"] = "second-key"
            await client.get("second")

    assert authorization_headers == ["Bearer first-key", "Bearer second-key"]
