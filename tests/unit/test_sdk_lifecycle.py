"""Tests for Mistral SDK constructor, context manager, lazy loading, and client injection."""

import asyncio

import httpx
import pytest

from mistralai.client.sdk import Mistral
from mistralai.client.sdkconfiguration import SERVER_EU, SERVERS
from mistralai.client.utils.retries import BackoffStrategy, RetryConfig


# -------------------------------------------------------------------------
# 1. Default server URL
# -------------------------------------------------------------------------


class TestDefaultServerUrl:
    def test_default_server_url(self):
        m = Mistral(api_key="k")
        url, _ = m.sdk_configuration.get_server_details()
        assert url == "https://api.mistral.ai"


# -------------------------------------------------------------------------
# 2. Custom server URL
# -------------------------------------------------------------------------


class TestCustomServerUrl:
    def test_custom_server_url(self):
        m = Mistral(api_key="k", server_url="https://custom.api")
        url, _ = m.sdk_configuration.get_server_details()
        assert url == "https://custom.api"


# -------------------------------------------------------------------------
# 3. Server enum selects predefined
# -------------------------------------------------------------------------


class TestServerEnumSelectsPredefined:
    def test_server_enum_selects_predefined(self):
        m = Mistral(api_key="k", server="eu")
        url, _ = m.sdk_configuration.get_server_details()
        assert url == SERVERS[SERVER_EU]
        assert url == "https://api.mistral.ai"


# -------------------------------------------------------------------------
# 4. API key string sets security
# -------------------------------------------------------------------------


class TestApiKeyStringSetsSecurityy:
    def test_api_key_string_sets_security(self):
        m = Mistral(api_key="my-secret-key")
        security = m.sdk_configuration.security
        # When api_key is a plain string, security is a Security object (not callable)
        assert not callable(security)
        assert security.api_key == "my-secret-key"


# -------------------------------------------------------------------------
# 5. API key callable
# -------------------------------------------------------------------------


class TestApiKeyCallable:
    def test_api_key_callable(self):
        m = Mistral(api_key=lambda: "dynamic-key")
        # When api_key is callable, security is a callable (lambda)
        assert callable(m.sdk_configuration.security)
        security_obj = m.sdk_configuration.security()
        assert security_obj.api_key == "dynamic-key"


# -------------------------------------------------------------------------
# 6. Timeout ms stored
# -------------------------------------------------------------------------


class TestTimeoutMsStored:
    def test_timeout_ms_stored(self):
        m = Mistral(api_key="k", timeout_ms=5000)
        assert m.sdk_configuration.timeout_ms == 5000


# -------------------------------------------------------------------------
# 7. Retry config stored
# -------------------------------------------------------------------------


class TestRetryConfigStored:
    def test_retry_config_stored(self):
        rc = RetryConfig(
            strategy="backoff",
            backoff=BackoffStrategy(
                initial_interval=500,
                max_interval=60000,
                exponent=1.5,
                max_elapsed_time=300000,
            ),
            retry_connection_errors=False,
        )
        m = Mistral(api_key="k", retry_config=rc)
        assert m.sdk_configuration.retry_config is rc
        assert m.sdk_configuration.retry_config.strategy == "backoff"


# -------------------------------------------------------------------------
# 8. Injected sync client used
# -------------------------------------------------------------------------


class TestInjectedSyncClientUsed:
    def test_injected_sync_client_used(self):
        custom_client = httpx.Client(follow_redirects=True)
        try:
            m = Mistral(api_key="k", client=custom_client)
            assert m.sdk_configuration.client is custom_client
            assert m.sdk_configuration.client_supplied is True
        finally:
            custom_client.close()


# -------------------------------------------------------------------------
# 9. Injected async client used
# -------------------------------------------------------------------------


class TestInjectedAsyncClientUsed:
    @pytest.mark.asyncio
    async def test_injected_async_client_used(self):
        custom_async_client = httpx.AsyncClient(follow_redirects=True)
        try:
            m = Mistral(api_key="k", async_client=custom_async_client)
            assert m.sdk_configuration.async_client is custom_async_client
            assert m.sdk_configuration.async_client_supplied is True
        finally:
            await custom_async_client.aclose()


# -------------------------------------------------------------------------
# 10. Default client created
# -------------------------------------------------------------------------


class TestDefaultClientCreated:
    def test_default_client_created(self):
        m = Mistral(api_key="k")
        assert m.sdk_configuration.client is not None
        assert m.sdk_configuration.client_supplied is False
        assert isinstance(m.sdk_configuration.client, httpx.Client)


# -------------------------------------------------------------------------
# 11. Sync context manager
# -------------------------------------------------------------------------


class TestSyncContextManager:
    def test_sync_context_manager(self):
        with Mistral(api_key="k") as m:
            assert isinstance(m, Mistral)
            assert m.sdk_configuration.client is not None


# -------------------------------------------------------------------------
# 12. Async context manager
# -------------------------------------------------------------------------


class TestAsyncContextManager:
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with Mistral(api_key="k") as m:
            assert isinstance(m, Mistral)
            assert m.sdk_configuration.async_client is not None


# -------------------------------------------------------------------------
# 13. Context manager closes default client
# -------------------------------------------------------------------------


class TestContextManagerClosesDefaultClient:
    def test_context_manager_closes_default_client(self):
        m = Mistral(api_key="k")
        assert m.sdk_configuration.client is not None
        assert m.sdk_configuration.client_supplied is False

        m.__enter__()
        m.__exit__(None, None, None)

        # After exit, client should be set to None for non-supplied clients
        assert m.sdk_configuration.client is None


# -------------------------------------------------------------------------
# 14. Context manager does not close supplied client
# -------------------------------------------------------------------------


class TestContextManagerDoesNotCloseSuppliedClient:
    def test_context_manager_does_not_close_supplied_client(self):
        custom_client = httpx.Client(follow_redirects=True)
        try:
            m = Mistral(api_key="k", client=custom_client)
            assert m.sdk_configuration.client_supplied is True

            m.__enter__()
            m.__exit__(None, None, None)

            # Supplied clients are NOT closed by the context manager.
            # The client reference is still set to None, but the client
            # object itself should not have been closed.
            assert not custom_client.is_closed
        finally:
            custom_client.close()


# -------------------------------------------------------------------------
# 15. Lazy load chat
# -------------------------------------------------------------------------


class TestLazyLoadChat:
    def test_lazy_load_chat(self):
        m = Mistral(api_key="k")
        chat = m.chat
        from mistralai.client.chat import Chat

        assert isinstance(chat, Chat)


# -------------------------------------------------------------------------
# 16. Lazy load agents
# -------------------------------------------------------------------------


class TestLazyLoadAgents:
    def test_lazy_load_agents(self):
        m = Mistral(api_key="k")
        agents = m.agents
        from mistralai.client.agents import Agents

        assert isinstance(agents, Agents)


# -------------------------------------------------------------------------
# 17. Lazy load caches
# -------------------------------------------------------------------------


class TestLazyLoadCaches:
    def test_lazy_load_caches(self):
        m = Mistral(api_key="k")
        chat1 = m.chat
        chat2 = m.chat
        assert chat1 is chat2


# -------------------------------------------------------------------------
# 18. Invalid attribute raises
# -------------------------------------------------------------------------


class TestInvalidAttributeRaises:
    def test_invalid_attribute_raises(self):
        m = Mistral(api_key="k")
        with pytest.raises(AttributeError, match="nonexistent"):
            _ = m.nonexistent


# -------------------------------------------------------------------------
# 19. dir includes sub SDKs
# -------------------------------------------------------------------------


class TestDirIncludesSubSdks:
    def test_dir_includes_sub_sdks(self):
        m = Mistral(api_key="k")
        d = dir(m)
        for name in ("chat", "agents", "fim", "embeddings", "models"):
            assert name in d, f"{name} not found in dir(m)"


# -------------------------------------------------------------------------
# 20. dir includes all sub SDK names
# -------------------------------------------------------------------------


class TestDirIncludesAllSubSdkNames:
    def test_dir_includes_all_sub_sdk_names(self):
        m = Mistral(api_key="k")
        d = dir(m)
        for name in m._sub_sdk_map:
            assert name in d, f"{name} from _sub_sdk_map not found in dir(m)"
