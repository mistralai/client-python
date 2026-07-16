"""Tests for the Streamable HTTP MCP client."""

import unittest
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any
from unittest import mock

from mistralai.extra.mcp.streamable_http import (
    MCPClientStreamableHTTP,
    StreamableHTTPServerParams,
)


class TestMCPClientStreamableHTTP(unittest.IsolatedAsyncioTestCase):
    async def test_headers_are_set_on_the_http_client(self) -> None:
        """Credentials must live on the httpx client (the transport's own headers
        argument is deprecated/ignored), so they are sent on every request."""
        captured: dict[str, Any] = {}

        @asynccontextmanager
        async def fake_streamable_http_client(url: str, http_client: Any) -> AsyncIterator[Any]:
            captured["url"] = url
            captured["headers"] = dict(http_client.headers)
            yield object(), object(), lambda: None

        client = MCPClientStreamableHTTP(
            params=StreamableHTTPServerParams(
                url="http://mcp.example/mcp",
                headers={"Authorization": "Bearer gate", "Notion-Token": "ntn_x"},
            ),
            name="test",
        )

        with mock.patch(
            "mistralai.extra.mcp.streamable_http.streamable_http_client",
            fake_streamable_http_client,
        ):
            async with AsyncExitStack() as stack:
                read_stream, write_stream = await client._get_transport(stack)

        self.assertIsNotNone(read_stream)
        self.assertIsNotNone(write_stream)
        self.assertEqual(captured["url"], "http://mcp.example/mcp")
        # httpx normalizes header names to lower case
        self.assertEqual(captured["headers"]["authorization"], "Bearer gate")
        self.assertEqual(captured["headers"]["notion-token"], "ntn_x")

    async def test_follow_redirects_defaults_false_and_is_configurable(self) -> None:
        """Redirects are not followed by default (secret headers would be resent to
        the redirect target); the flag is forwarded to the httpx client when set."""
        captured: dict[str, Any] = {}

        @asynccontextmanager
        async def fake_streamable_http_client(url: str, http_client: Any) -> AsyncIterator[Any]:
            captured["follow_redirects"] = http_client.follow_redirects
            yield object(), object(), lambda: None

        with mock.patch(
            "mistralai.extra.mcp.streamable_http.streamable_http_client",
            fake_streamable_http_client,
        ):
            default_client = MCPClientStreamableHTTP(
                params=StreamableHTTPServerParams(url="http://mcp.example/mcp"),
                name="test",
            )
            async with AsyncExitStack() as stack:
                await default_client._get_transport(stack)
            self.assertFalse(captured["follow_redirects"])

            opted_in_client = MCPClientStreamableHTTP(
                params=StreamableHTTPServerParams(url="http://mcp.example/mcp", follow_redirects=True),
                name="test",
            )
            async with AsyncExitStack() as stack:
                await opted_in_client._get_transport(stack)
            self.assertTrue(captured["follow_redirects"])


if __name__ == "__main__":
    unittest.main()
