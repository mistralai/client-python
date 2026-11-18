"""Tests for the SSE MCP client and its OAuth helpers."""

import json
import unittest
from unittest import mock

import httpx2 as httpx

from mistralai.extra.mcp.auth import build_oauth_params, get_oauth_server_metadata
from mistralai.extra.mcp.sse import MCPClientSSE, SSEServerParams


class TestMCPClientSSEBaseUrl(unittest.TestCase):
    def test_base_url_removes_only_the_sse_suffix(self) -> None:
        cases = {
            "https://mcp.example.services/sse": "https://mcp.example.services",
            "https://example.com/mcp/events": "https://example.com/mcp/events",
            "https://example.com/sse": "https://example.com",
            "https://example.com/sse/": "https://example.com",
            "https://example.com/mcp": "https://example.com/mcp",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                client = MCPClientSSE(sse_params=SSEServerParams(url=url))
                self.assertEqual(client.base_url, expected)


class TestOAuthFallbackMetadata(unittest.IsolatedAsyncioTestCase):
    async def test_fallback_registers_the_client_at_the_default_endpoint(self) -> None:
        server_url = "https://mcp.example"
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                201, json={"client_id": "cid", "client_secret": "csecret"}
            )

        with mock.patch(
            "mistralai.extra.mcp.auth.get_well_known_authorization_server_metadata",
            mock.AsyncMock(return_value=None),
        ):
            metadata = await get_oauth_server_metadata(server_url)
            self.assertEqual(metadata.registration_endpoint, f"{server_url}/register")
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(handler)
            ) as async_client:
                params = await build_oauth_params(
                    server_url,
                    redirect_url="http://localhost/callback",
                    async_client=async_client,
                )

        self.assertEqual(params.client_id, "cid")
        self.assertEqual(params.client_secret, "csecret")
        self.assertEqual(len(requests), 1)
        self.assertEqual(str(requests[0].url), f"{server_url}/register")
        self.assertEqual(
            json.loads(requests[0].content)["redirect_uris"],
            ["http://localhost/callback"],
        )
