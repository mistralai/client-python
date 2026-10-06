from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any, Awaitable, Callable, TYPE_CHECKING
from urllib.parse import quote, unquote

import httpx2 as httpx

from mistralai.client import models, utils
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.extra.connectors_gateway_errors import (
    ConnectorsGatewayError as ConnectorsGatewayError,
    raise_connectors_gateway_error,
    single_connectors_gateway_error,
)

if TYPE_CHECKING:
    from mcp import ClientSession

MCPClientContext = AbstractAsyncContextManager["ClientSession"]

_DEFAULT_TIMEOUT_MS = 300_000
_MCP_SSE_READ_TIMEOUT = 60 * 5
_GATEWAY_PATH = "/v1/connectors-gateway"


def _request_headers(
    sdk_configuration: SDKConfiguration,
    *,
    credentials_name: str | None,
) -> httpx.Headers:
    request_headers = httpx.Headers({"user-agent": sdk_configuration.user_agent})
    if credentials_name is not None:
        request_headers["x-credentials-name"] = credentials_name
    return request_headers


def _security_request_hook(
    sdk_configuration: SDKConfiguration,
) -> Callable[[httpx.Request], Awaitable[None]]:
    async def add_security_headers(request: httpx.Request) -> None:
        security_source = sdk_configuration.security
        if callable(security_source):
            security_source = security_source()
        security = utils.get_security_from_env(security_source, models.Security)
        security_headers, _ = utils.get_security(security)
        for name, value in security_headers.items():
            request.headers.setdefault(name, value)

    return add_security_headers


def _gateway_url(
    sdk_configuration: SDKConfiguration,
    connector_id_or_name: str,
    suffix: str,
) -> httpx.URL:
    server_url, _ = sdk_configuration.get_server_details()
    connector_ref = quote(connector_id_or_name, safe="")
    return httpx.URL(
        f"{server_url.rstrip('/')}{_GATEWAY_PATH}/{connector_ref}/{suffix.lstrip('/')}"
    )


def _timeout(sdk_configuration: SDKConfiguration) -> float:
    effective_timeout_ms = sdk_configuration.timeout_ms
    if effective_timeout_ms is None:
        effective_timeout_ms = _DEFAULT_TIMEOUT_MS
    return effective_timeout_ms / 1000


def _ensure_allowed_url(url: httpx.URL, allowed_base_url: httpx.URL) -> None:
    same_origin = (
        url.scheme == allowed_base_url.scheme
        and url.host == allowed_base_url.host
        and url.port == allowed_base_url.port
    )
    base_path = allowed_base_url.raw_path.rstrip(b"/")
    request_path = url.raw_path.split(b"?", 1)[0]
    is_subpath = request_path == base_path or request_path.startswith(base_path + b"/")
    relative_path = request_path[len(base_path) :].lstrip(b"/")
    has_dot_segments = any(
        unquote(segment.decode("ascii")) in {".", ".."}
        for segment in relative_path.split(b"/")
    )
    if not same_origin or not is_subpath or has_dot_segments:
        raise ValueError(
            "HTTP connector client requests must target the configured connector"
        )


def _new_httpx_client(**kwargs: Any) -> httpx.AsyncClient:
    return httpx.AsyncClient(**kwargs)


def _create_mcp_http_client(
    sdk_configuration: SDKConfiguration,
    *,
    credentials_name: str | None,
) -> httpx.AsyncClient:
    return _new_httpx_client(
        headers=_request_headers(
            sdk_configuration,
            credentials_name=credentials_name,
        ),
        timeout=httpx.Timeout(
            _timeout(sdk_configuration),
            read=_MCP_SSE_READ_TIMEOUT,
        ),
        follow_redirects=False,
        event_hooks={
            "request": [_security_request_hook(sdk_configuration)],
            "response": [raise_connectors_gateway_error],
        },
    )


@asynccontextmanager
async def mcp_client(
    sdk_configuration: SDKConfiguration,
    *,
    connector_id_or_name: str,
    credentials_name: str | None = None,
) -> AsyncIterator["ClientSession"]:
    """Open an official MCP client session through the connectors gateway."""
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
    except ImportError as exc:
        raise ImportError(
            "MCP support requires the 'mistralai[mcp]' optional dependency."
        ) from exc

    http_client = _create_mcp_http_client(
        sdk_configuration,
        credentials_name=credentials_name,
    )
    gateway_url = _gateway_url(
        sdk_configuration,
        connector_id_or_name,
        "mcp",
    )

    caller_error: Exception | None = None
    try:
        async with http_client:
            async with streamable_http_client(
                str(gateway_url),
                http_client=http_client,
            ) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    try:
                        yield session
                    except Exception as exc:
                        # Close the session normally and re-raise below, so MCP's
                        # task groups do not wrap the caller's error in an ExceptionGroup.
                        caller_error = exc
    except Exception as exc:
        gateway_error = single_connectors_gateway_error(exc)
        if gateway_error is not None:
            raise gateway_error from None
        raise
    if caller_error is not None:
        raise caller_error


def http_client(
    sdk_configuration: SDKConfiguration,
    *,
    connector_id_or_name: str,
    credentials_name: str | None = None,
) -> httpx.AsyncClient:
    """Create an HTTP client targeting a connector through the gateway."""
    gateway_url = _gateway_url(
        sdk_configuration,
        connector_id_or_name,
        "http",
    )
    base_url = httpx.URL(f"{str(gateway_url).rstrip('/')}/")

    async def ensure_allowed_request(request: httpx.Request) -> None:
        _ensure_allowed_url(request.url, gateway_url)

    return _new_httpx_client(
        base_url=base_url,
        headers=_request_headers(
            sdk_configuration,
            credentials_name=credentials_name,
        ),
        timeout=_timeout(sdk_configuration),
        follow_redirects=False,
        event_hooks={
            "request": [
                ensure_allowed_request,
                _security_request_hook(sdk_configuration),
            ],
            "response": [raise_connectors_gateway_error],
        },
    )
