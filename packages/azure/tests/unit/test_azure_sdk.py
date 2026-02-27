"""Tests for MistralAzure constructor and api-version injection."""

import warnings

import httpx
import pytest

from mistralai.azure.client.sdk import MistralAzure


# -------------------------------------------------------------------------
# 1. Default API version
# -------------------------------------------------------------------------


class TestDefaultApiVersion:
    def test_default_api_version(self):
        client = MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
        )

        # The default api_version should be "2024-05-01-preview"
        # It should be injected into the httpx client's params
        params = client.sdk_configuration.client.params
        assert "api-version" in dict(params)
        assert dict(params)["api-version"] == "2024-05-01-preview"


# -------------------------------------------------------------------------
# 2. Custom API version
# -------------------------------------------------------------------------


class TestCustomApiVersion:
    def test_custom_api_version(self):
        client = MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
            api_version="2025-01-01",
        )

        params = client.sdk_configuration.client.params
        assert dict(params)["api-version"] == "2025-01-01"


# -------------------------------------------------------------------------
# 3. API version in query params
# -------------------------------------------------------------------------


class TestApiVersionInQueryParams:
    def test_api_version_in_query_params(self):
        client = MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
        )

        # Both sync and async clients should have the param
        sync_params = dict(client.sdk_configuration.client.params)
        assert sync_params["api-version"] == "2024-05-01-preview"

        async_params = dict(client.sdk_configuration.async_client.params)
        assert async_params["api-version"] == "2024-05-01-preview"


# -------------------------------------------------------------------------
# 4. Context manager works
# -------------------------------------------------------------------------


class TestContextManager:
    def test_context_manager(self):
        with MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
        ) as m:
            assert isinstance(m, MistralAzure)
            assert m.sdk_configuration.client is not None


# -------------------------------------------------------------------------
# 5. dir() includes sub SDKs
# -------------------------------------------------------------------------


class TestDirIncludesSubSdks:
    def test_dir_includes_sub_sdks(self):
        client = MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
        )

        d = dir(client)
        assert "chat" in d
        assert "ocr" in d


# -------------------------------------------------------------------------
# 6. Warning when custom client + non-default api_version
# -------------------------------------------------------------------------


class TestApiVersionWarningWithCustomClient:
    def test_api_version_warning_with_custom_client(self):
        custom_client = httpx.Client()
        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = MistralAzure(
                    api_key="test-key",
                    server_url="https://test.azure.api",
                    client=custom_client,
                    api_version="2025-01-01",
                )
                assert len(w) >= 1
                assert "api_version is ignored" in str(w[0].message)
        finally:
            custom_client.close()


# -------------------------------------------------------------------------
# 7. Chat complete via respx verifies api-version in request
# -------------------------------------------------------------------------


class TestChatCompleteViaRespx:
    def test_chat_complete_sends_api_version(self):
        """Azure chat.complete() sends api-version query parameter."""
        import respx

        client = MistralAzure(
            api_key="test-key",
            server_url="https://test.azure.api",
        )

        chat_response = {
            "id": "test-001",
            "object": "chat.completion",
            "model": "mistral-small-latest",
            "created": 1700000000,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello."},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        }

        with respx.mock(base_url="https://test.azure.api") as router:
            # Azure SDK strips /v1/ prefix from paths
            route = router.post("/chat/completions").mock(
                return_value=httpx.Response(200, json=chat_response)
            )
            result = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

            assert result is not None
            assert result.id == "test-001"
            # Verify api-version was in the query params
            assert route.called
            request = route.calls.last.request
            assert "api-version" in str(request.url)
