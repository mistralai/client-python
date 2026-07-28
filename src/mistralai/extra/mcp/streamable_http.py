import logging
from contextlib import AsyncExitStack
from typing import Any

import httpx
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp.client.streamable_http import streamable_http_client  # pyright: ignore[reportMissingImports]
from mcp.shared.message import SessionMessage  # pyright: ignore[reportMissingImports]

from mistralai.extra.mcp.base import (
    MCPClientBase,
)

from mistralai.client.types import BaseModel

logger = logging.getLogger(__name__)


class StreamableHTTPServerParams(BaseModel):
    """Parameters required for a MCPClient with Streamable HTTP transport"""

    url: str
    headers: dict[str, Any] | None = None
    timeout: float = 30
    # Whether the httpx client trusts the ambient environment (HTTP(S)_PROXY,
    # SSL_CERT_FILE/DIR, .netrc). Defaults to httpx's default (True). Set False to
    # reach the endpoint directly without an ambient egress proxy, e.g. for an
    # in-cluster URL on a host whose external egress is proxied.
    trust_env: bool = True
    # Whether httpx follows HTTP redirects (3xx). Defaults to False (also httpx's
    # default). On a redirect httpx only strips Authorization on cross-origin hops,
    # so the ``headers`` above (e.g. a per-request integration token) would be resent
    # verbatim to the redirect target, letting a compromised or open-redirecting
    # server exfiltrate them. Set True only if the server relies on redirects and
    # every host it can redirect to is trusted.
    follow_redirects: bool = False


class MCPClientStreamableHTTP(MCPClientBase):
    """MCP client that uses the Streamable HTTP transport for communication.

    Credentials (for example a bearer token, or a per-request integration token)
    are provided as ``headers`` and set as the default headers of the underlying
    ``httpx.AsyncClient``, so they are sent on every request including the
    initialize call. Recent ``mcp`` releases deprecate and ignore the transport's
    own ``headers`` argument, so configuring them on the client is required.
    """

    _params: StreamableHTTPServerParams

    def __init__(
        self,
        params: StreamableHTTPServerParams,
        name: str | None = None,
    ):
        super().__init__(name=name)
        self._params = params

    async def _get_transport(
        self, exit_stack: AsyncExitStack
    ) -> tuple[
        MemoryObjectReceiveStream[SessionMessage | Exception],
        MemoryObjectSendStream[SessionMessage],
    ]:
        # trust_env controls whether the client inherits the ambient
        # HTTP(S)_PROXY / cert / netrc env. Set it False (see params) to reach an
        # in-cluster endpoint directly, bypassing a proxy meant for external
        # traffic that would make the connection hang.
        #
        # follow_redirects defaults False (see params): the secret default headers
        # would otherwise be resent to a redirect target on same-origin hops.
        http_client = await exit_stack.enter_async_context(
            httpx.AsyncClient(
                headers=self._params.headers,
                timeout=self._params.timeout,
                follow_redirects=self._params.follow_redirects,
                trust_env=self._params.trust_env,
            )
        )
        read_stream, write_stream, _ = await exit_stack.enter_async_context(
            streamable_http_client(url=self._params.url, http_client=http_client)
        )
        return read_stream, write_stream
