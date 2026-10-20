import importlib
import threading
from importlib.util import find_spec
from unittest import SkipTest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx2 as httpx
import pytest

# The worker wrapper needs an explicit livekit-agents install. Skip cleanly
# when it isn't installed (client-only environments).
if find_spec("livekit.agents") is None:
    raise SkipTest("Custom worker tests require livekit-agents")

from mistralai.extra.voice_agents.worker import (  # noqa: E402
    WorkerTokenClient,
    _build_managed_server,
    _is_agent_registration_grant,
    _patched_registration_token,
    _TokenProviderAccessToken,
)

api = importlib.import_module("livekit.api")

BASE_URL = "https://audio.example.com"
API_KEY = "sk-mistral-test"


def _fake_response(payload: dict) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json = MagicMock(return_value=payload)
    return resp


class TestWorkerTokenClient:
    def test_fetch_parses_response_and_sends_auth(self):
        payload = {
            "ws_url": "wss://livekit.example.com",
            "agent_name": "ws-123",
            "token": "reg-token-abc",
            "expires_at": "2026-07-07T10:10:00+00:00",
        }
        mock_post = MagicMock(return_value=_fake_response(payload))

        with patch.object(httpx, "post", mock_post):
            client = WorkerTokenClient(api_key=API_KEY, base_url=BASE_URL)
            token = client.fetch()

        assert token.ws_url == "wss://livekit.example.com"
        assert token.agent_name == "ws-123"
        assert token.token == "reg-token-abc"
        assert token.expires_at is not None

        call = mock_post.call_args
        assert call.args[0] == f"{BASE_URL}/v1/audio/workers/registration-token"
        assert call.kwargs["headers"] == {"Authorization": f"Bearer {API_KEY}"}
        assert call.kwargs["json"] == {}

    def test_requires_api_key_and_base_url(self):
        with pytest.raises(ValueError):
            WorkerTokenClient(api_key="", base_url=BASE_URL)
        with pytest.raises(ValueError):
            WorkerTokenClient(api_key=API_KEY, base_url="")


class TestBaseUrlValidation:
    """base_url carries the API key, so it must be https (http only for loopback)."""

    def test_rejects_plaintext_http_for_remote_host(self):
        with pytest.raises(ValueError, match="refusing insecure base_url"):
            WorkerTokenClient(api_key=API_KEY, base_url="http://audio.example.com")

    def test_rejects_non_http_scheme(self):
        # wss is the SFU scheme, not a valid POST target for the token endpoint.
        with pytest.raises(ValueError):
            WorkerTokenClient(api_key=API_KEY, base_url="wss://audio.example.com")

    def test_allows_http_loopback_for_local_dev(self):
        # Constructs without raising against a localhost gateway.
        WorkerTokenClient(api_key=API_KEY, base_url="http://localhost:8886")
        WorkerTokenClient(api_key=API_KEY, base_url="http://127.0.0.1:8886")


class TestWsUrlValidation:
    """The returned ws_url carries the minted registration token, so it must be
    wss (ws only for loopback)."""

    def _post_returning_ws_url(self, ws_url: str) -> MagicMock:
        payload = {"ws_url": ws_url, "agent_name": "ws-123", "token": "t"}
        return MagicMock(return_value=_fake_response(payload))

    def test_rejects_plaintext_ws_url_from_server(self):
        mock_post = self._post_returning_ws_url("ws://livekit.example.com")
        with patch.object(httpx, "post", mock_post):
            client = WorkerTokenClient(api_key=API_KEY, base_url=BASE_URL)
            with pytest.raises(ValueError, match="refusing insecure ws_url"):
                client.fetch()

    def test_allows_ws_loopback_ws_url(self):
        mock_post = self._post_returning_ws_url("ws://localhost:7880")
        with patch.object(httpx, "post", mock_post):
            client = WorkerTokenClient(api_key=API_KEY, base_url=BASE_URL)
            token = client.fetch()
        assert token.ws_url == "ws://localhost:7880"


class TestGrantDetection:
    def test_agent_only_grant_is_registration(self):
        assert _is_agent_registration_grant(api.VideoGrants(agent=True))

    def test_room_grant_is_not_registration(self):
        assert not _is_agent_registration_grant(
            api.VideoGrants(room_join=True, room="r")
        )

    def test_agent_plus_room_is_not_registration(self):
        # A token that also carries room access must NOT be substituted.
        assert not _is_agent_registration_grant(
            api.VideoGrants(agent=True, room_join=True, room="r")
        )


class TestTokenProviderAccessToken:
    def test_returns_provider_token_for_registration(self):
        tok = _TokenProviderAccessToken(api.AccessToken, lambda: "PROVIDED", "k", "s")
        jwt = tok.with_grants(api.VideoGrants(agent=True)).to_jwt()
        assert jwt == "PROVIDED"

    def test_delegates_for_non_registration(self):
        tok = _TokenProviderAccessToken(api.AccessToken, lambda: "PROVIDED", "k", "s")
        jwt = (
            tok.with_identity("u")
            .with_grants(api.VideoGrants(room_join=True, room="r"))
            .to_jwt()
        )
        assert jwt != "PROVIDED"
        assert jwt.count(".") == 2  # a real JWT


class TestOverrideSmoke:
    """Assert the override intercepts the *exact* mint expression the SDK uses
    (livekit/agents worker.py). If a version bump changes it, this fails."""

    def test_patched_registration_token_intercepts_sdk_mint(self):
        worker_module = importlib.import_module("livekit.agents.worker")

        original = worker_module.api.AccessToken
        with _patched_registration_token(lambda: "MY_TOKEN"):
            # Mirror worker.py's join_jwt construction exactly.
            join_jwt = (
                worker_module.api.AccessToken("k", "s")
                .with_grants(worker_module.api.VideoGrants(agent=True))
                .to_jwt()
            )
            assert join_jwt == "MY_TOKEN"

            # A room-scoped mint (if any) must not be hijacked.
            other = (
                worker_module.api.AccessToken("k", "s")
                .with_identity("u")
                .with_grants(worker_module.api.VideoGrants(room_join=True, room="r"))
                .to_jwt()
            )
            assert other != "MY_TOKEN"

        # Restored on exit.
        assert worker_module.api.AccessToken is original


class TestBuildManagedServer:
    def test_builds_agent_server_subclass_with_override(self):
        AgentServer = importlib.import_module("livekit.agents").AgentServer

        server = _build_managed_server(
            ws_url="wss://livekit.example.com",
            token_provider=lambda: "tok",
        )
        assert isinstance(server, AgentServer)
        # The override is present and distinct from the stock method.
        assert type(server)._connection_task is not AgentServer._connection_task

    @pytest.mark.asyncio
    async def test_connection_task_runs_token_provider_in_thread(self):
        """Token provider must run in a worker thread, not the event loop thread."""
        AgentServer = importlib.import_module("livekit.agents").AgentServer

        token_thread_ids: list[int] = []

        def provider() -> str:
            token_thread_ids.append(threading.get_ident())
            return "THREAD_TOKEN"

        server = _build_managed_server(
            ws_url="wss://livekit.example.com",
            token_provider=provider,
        )

        with patch.object(AgentServer, "_connection_task", AsyncMock()):
            await type(server)._connection_task(server)

        assert token_thread_ids, "token_provider was never called"
        assert token_thread_ids[0] != threading.main_thread().ident
