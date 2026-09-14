from __future__ import annotations

from collections.abc import AsyncIterable
from typing import Any, Mapping
from urllib.parse import quote, unquote, urlsplit

import httpx

from mistralai.client import errors, models, utils
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.extra.exceptions import MCPException

_DEFAULT_TIMEOUT_MS = 300_000
_GATEWAY_PATH = "/v1/connectors-gateway"


class ConnectorGatewayProtocolError(MCPException):
    """Raised when the connectors gateway returns an invalid JSON-RPC response."""

    def __init__(
        self,
        message: str,
        *,
        code: int | None = None,
        data: Any = None,
    ) -> None:
        self.code = code
        self.data = data
        super().__init__(message)


def _request_headers(
    sdk_configuration: SDKConfiguration,
    *,
    credentials_name: str | None,
    headers: httpx.Headers | None = None,
) -> httpx.Headers:
    security_source = sdk_configuration.security
    if callable(security_source):
        security_source = security_source()
    security = utils.get_security_from_env(security_source, models.Security)
    security_headers, _ = utils.get_security(security)

    request_headers = httpx.Headers(
        {
            "user-agent": sdk_configuration.user_agent,
            **security_headers,
        }
    )
    if headers is not None:
        request_headers.update(headers)
    if credentials_name is not None:
        request_headers["x-credentials-name"] = credentials_name
    return request_headers


def _gateway_url(
    sdk_configuration: SDKConfiguration,
    connector_id_or_name: str,
    suffix: str,
    *,
    server_url: str | None,
) -> httpx.URL:
    if server_url is None:
        server_url, _ = sdk_configuration.get_server_details()
    connector_ref = quote(connector_id_or_name, safe="")
    return httpx.URL(
        f"{server_url.rstrip('/')}{_GATEWAY_PATH}/{connector_ref}/{suffix.lstrip('/')}"
    )


def _timeout(sdk_configuration: SDKConfiguration, timeout_ms: int | None) -> float:
    effective_timeout_ms = timeout_ms
    if effective_timeout_ms is None:
        effective_timeout_ms = sdk_configuration.timeout_ms
    if effective_timeout_ms is None:
        effective_timeout_ms = _DEFAULT_TIMEOUT_MS
    return effective_timeout_ms / 1000


def _parse_tool_result(response: httpx.Response) -> models.ConnectorToolCallResponse:
    if response.status_code != 200:
        raise errors.SDKError("Connector gateway error", response)

    try:
        envelope = response.json()
    except ValueError as exc:
        raise ConnectorGatewayProtocolError(
            "Connector gateway returned a non-JSON MCP response"
        ) from exc

    if (
        not isinstance(envelope, dict)
        or envelope.get("jsonrpc") != "2.0"
        or envelope.get("id") != 1
    ):
        raise ConnectorGatewayProtocolError(
            "Connector gateway returned an invalid JSON-RPC response"
        )

    error = envelope.get("error")
    if isinstance(error, dict):
        message = error.get("message", "Connector tool call failed")
        code = error.get("code")
        raise ConnectorGatewayProtocolError(
            str(message),
            code=code if isinstance(code, int) else None,
            data=error.get("data"),
        )

    result = envelope.get("result")
    if not isinstance(result, dict) or not isinstance(result.get("content"), list):
        raise ConnectorGatewayProtocolError(
            "Connector gateway response is missing an MCP tool result"
        )

    response_data: dict[str, Any] = {"content": result["content"]}
    if (
        result.get("isError", False)
        or result.get("structuredContent") is not None
        or result.get("_meta") is not None
    ):
        response_data["metadata"] = {
            "mcp_meta": {
                "isError": result.get("isError", False),
                "structuredContent": result.get("structuredContent"),
                "_meta": result.get("_meta"),
            }
        }
    return models.ConnectorToolCallResponse.model_validate(response_data)


async def call_mcp_tool_async(
    sdk_configuration: SDKConfiguration,
    *,
    connector_id_or_name: str,
    tool_name: str,
    arguments: Mapping[str, Any] | None = None,
    credentials_name: str | None = None,
    server_url: str | None = None,
    timeout_ms: int | None = None,
) -> models.ConnectorToolCallResponse:
    """Call an MCP connector tool directly through the stateless gateway."""
    client = sdk_configuration.async_client
    if client is None:
        raise ValueError("async client is required")

    request = client.build_request(
        "POST",
        _gateway_url(
            sdk_configuration,
            connector_id_or_name,
            "mcp",
            server_url=server_url,
        ),
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": dict(arguments or {}),
            },
        },
        headers=_request_headers(
            sdk_configuration,
            credentials_name=credentials_name,
            headers=httpx.Headers({"accept": "application/json, text/event-stream"}),
        ),
        timeout=_timeout(sdk_configuration, timeout_ms),
    )
    response = await client.send(request, auth=None, follow_redirects=False)
    return _parse_tool_result(response)


async def call_http_endpoint_async(
    sdk_configuration: SDKConfiguration,
    *,
    connector_id_or_name: str,
    request: httpx.Request,
    credentials_name: str | None = None,
    server_url: str | None = None,
    timeout_ms: int | None = None,
) -> httpx.Response:
    """Send a relative HTTP request through an HTTP connector gateway route."""
    target = urlsplit(str(request.url))
    if target.scheme or target.netloc:
        raise ValueError("HTTP connector request URL must be relative")
    if any(unquote(segment) in {".", ".."} for segment in target.path.split("/")):
        raise ValueError("HTTP connector request URL must not contain dot segments")

    client = sdk_configuration.async_client
    if client is None:
        raise ValueError("async client is required")

    try:
        body = request.content
    except httpx.RequestNotRead:
        if isinstance(request.stream, AsyncIterable):
            body = await request.aread()
        else:
            body = request.read()

    path = target.path.lstrip("/")
    gateway_url = _gateway_url(
        sdk_configuration,
        connector_id_or_name,
        f"http/{path}",
        server_url=server_url,
    )
    if target.query:
        gateway_url = gateway_url.copy_with(query=target.query.encode("ascii"))

    has_explicit_body = (
        bool(body)
        or "content-length" in request.headers
        or "transfer-encoding" in request.headers
    )
    extensions = dict(request.extensions)
    extensions.pop("timeout", None)
    gateway_request = client.build_request(
        request.method,
        gateway_url,
        content=body if has_explicit_body else None,
        headers=_request_headers(
            sdk_configuration,
            credentials_name=credentials_name,
            headers=request.headers,
        ),
        timeout=_timeout(sdk_configuration, timeout_ms),
        extensions=extensions,
    )
    return await client.send(gateway_request, auth=None, follow_redirects=False)
