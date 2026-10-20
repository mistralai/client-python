"""Run a *custom* LiveKit worker authenticated with only a Mistral API key."""

from __future__ import annotations

import asyncio
import contextlib
import importlib
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from ipaddress import ip_address
from typing import Any, Callable, Iterator
from urllib.parse import urlparse

import httpx2 as httpx

logger = logging.getLogger(__name__)

# livekit-agents versions this override has been verified against. Other versions
# still run — the smoke test is the real guard — but log a warning so an
# unverified bump is visible.
_VERIFIED_LIVEKIT_AGENTS_VERSIONS = frozenset({"1.5.17", "1.6.4"})

_REGISTRATION_TOKEN_PATH = "/v1/audio/workers/registration-token"

TokenProvider = Callable[[], str]


def _is_loopback_host(host: str | None) -> bool:
    """True for ``localhost`` or any loopback IP (127.0.0.0/8, ::1)."""
    if not host:
        return False
    if host.lower() == "localhost":
        return True
    try:
        return ip_address(host).is_loopback
    except ValueError:
        return False


def _require_secure_url(url: str, *, secure: str, insecure: str, what: str) -> str:
    """Return ``url`` if it is safe to carry a credential, else raise.

    ``base_url`` carries the Mistral API key and the server-returned ``ws_url``
    carries the minted ``agent=True`` registration token, so both must be
    encrypted: a config typo must not send either over cleartext or to an
    unintended scheme/host. The ``insecure`` scheme (``http``/``ws``) is tolerated
    only for a loopback host, for local dev against a gateway on localhost. This
    mirrors the repo's https-unless-loopback idiom (editorial ``resolve_base_url``,
    vibe ``_is_loopback_host``).
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.hostname:
        raise ValueError(f"{what} must be an absolute {secure}:// URL, got: {url!r}")
    if parsed.scheme == secure:
        return url
    if parsed.scheme == insecure and _is_loopback_host(parsed.hostname):
        return url
    raise ValueError(
        f"refusing insecure {what} (use {secure}://): {url} — "
        f"{insecure}:// is only allowed for localhost."
    )


@dataclass(frozen=True)
class WorkerToken:
    ws_url: str
    agent_name: str
    token: str
    expires_at: datetime | None = None


class WorkerTokenClient:
    """Fetches worker registration tokens from the control plane.

    Auth is the Mistral API key only — the LiveKit secret never reaches the
    client. ``ws_url`` and ``agent_name`` are stable for a client, so callers
    typically fetch once for setup and then call :meth:`fetch_token` per connect.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout: float = 10.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required (set MISTRAL_API_KEY)")
        if not base_url:
            raise ValueError("base_url is required (the audio control-plane URL)")
        self._api_key = api_key
        self._base_url = _require_secure_url(
            base_url.rstrip("/"), secure="https", insecure="http", what="base_url"
        )
        self._timeout = timeout

    def fetch(self) -> WorkerToken:
        """Fetch a fresh registration token plus ws_url / agent_name."""
        resp = httpx.post(
            f"{self._base_url}{_REGISTRATION_TOKEN_PATH}",
            json={},
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=self._timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        expires_at = None
        if data.get("expires_at"):
            expires_at = datetime.fromisoformat(
                data["expires_at"].replace("Z", "+00:00")
            )
        ws_url = _require_secure_url(
            data["ws_url"], secure="wss", insecure="ws", what="ws_url"
        )
        return WorkerToken(
            ws_url=ws_url,
            agent_name=data["agent_name"],
            token=data["token"],
            expires_at=expires_at,
        )

    def fetch_token(self) -> str:
        """Fetch just the registration token (used as the per-connect provider)."""
        return self.fetch().token


def _is_agent_registration_grant(grants: Any) -> bool:
    """True iff ``grants`` is the worker registration grant (agent=True, no room).

    Guards the override so it substitutes our token *only* for the registration
    mint and never for any other AccessToken produced in-process.
    """
    if not bool(getattr(grants, "agent", False)):
        return False
    for room_field in ("room_join", "room_create", "room_admin", "room_list", "room"):
        if getattr(grants, room_field, None):
            return False
    return True


class _TokenProviderAccessToken:
    """Drop-in for ``api.AccessToken`` that returns a pre-minted registration
    token for the worker's ``agent=True`` join JWT and delegates everything else
    to the real class, so no other token minting is affected."""

    def __init__(
        self,
        real_cls: Any,
        token_provider: TokenProvider,
        api_key: str = "",
        api_secret: str = "",
    ) -> None:
        self._real = real_cls(api_key, api_secret)
        self._token_provider = token_provider
        self._is_registration = False

    def with_grants(self, grants: Any) -> "_TokenProviderAccessToken":
        self._real = self._real.with_grants(grants)
        self._is_registration = _is_agent_registration_grant(grants)
        return self

    def with_identity(self, *args: Any, **kwargs: Any) -> "_TokenProviderAccessToken":
        self._real = self._real.with_identity(*args, **kwargs)
        return self

    def with_ttl(self, *args: Any, **kwargs: Any) -> "_TokenProviderAccessToken":
        self._real = self._real.with_ttl(*args, **kwargs)
        return self

    def to_jwt(self) -> str:
        if self._is_registration:
            return self._token_provider()
        return self._real.to_jwt()


@contextlib.contextmanager
def _patched_registration_token(token_provider: TokenProvider) -> Iterator[None]:
    """Swap ``AccessToken`` on the livekit worker module for the shim."""
    worker_module = importlib.import_module("livekit.agents.worker")

    real_cls = worker_module.api.AccessToken

    def _factory(api_key: str = "", api_secret: str = "") -> _TokenProviderAccessToken:
        return _TokenProviderAccessToken(real_cls, token_provider, api_key, api_secret)

    # Deliberate shadowing of the AccessToken class with our shim factory
    # (reassigning a class attribute that is itself a type; mypy flags both the
    # incompatible type and can't-assign-to-a-type — intentional here).
    worker_module.api.AccessToken = _factory  # type: ignore
    try:
        yield
    finally:
        worker_module.api.AccessToken = real_cls  # type: ignore


def _build_managed_server(
    *,
    ws_url: str,
    token_provider: TokenProvider,
    api_key: str = "managed",
    api_secret: str = "managed",
    **server_kwargs: Any,
) -> Any:
    """Construct an AgentServer subclass whose registration token comes from
    ``token_provider``. ``api_key``/``api_secret`` are non-secret placeholders
    only to satisfy construction — they are never used to mint a real token."""
    AgentServer = importlib.import_module("livekit.agents").AgentServer

    class _ManagedAgentServer(AgentServer):  # type: ignore[misc, valid-type]
        async def _connection_task(self) -> None:
            # Run the blocking HTTP fetch in a thread so the event loop stays
            # free during the 10 s timeout window on every (re)connect.
            token = await asyncio.to_thread(token_provider)
            with _patched_registration_token(lambda: token):
                await super()._connection_task()

    return _ManagedAgentServer(
        ws_url=ws_url,
        api_key=api_key,
        api_secret=api_secret,
        **server_kwargs,
    )


def _warn_on_unverified_version() -> None:
    try:
        lk_version = importlib.import_module("livekit.agents").__version__
    except Exception:  # pragma: no cover - defensive
        return
    if lk_version not in _VERIFIED_LIVEKIT_AGENTS_VERSIONS:
        logger.warning(
            "Unverified livekit-agents version %s (verified: %s); the "
            "registration-token override is version-sensitive — run the worker "
            "smoke test after upgrading.",
            lk_version,
            sorted(_VERIFIED_LIVEKIT_AGENTS_VERSIONS),
        )


def run_worker(
    entrypoint: Callable[..., Any],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    setup_fnc: Callable[..., Any] | None = None,
    **server_kwargs: Any,
) -> None:
    """Run a custom LiveKit worker authenticated with only a Mistral API key.

    ``entrypoint`` is a standard ``livekit.agents`` job entrypoint owned by the
    engineer. ``api_key`` defaults to ``MISTRAL_API_KEY``; ``base_url`` to
    ``MISTRAL_AUDIO_BASE_URL`` and then to ``https://api.mistral.ai``. ``base_url``
    must be ``https`` (``http`` only for localhost) since it carries the API key.
    """
    cli = importlib.import_module("livekit.agents").cli

    _warn_on_unverified_version()

    resolved_api_key = api_key or os.environ.get("MISTRAL_API_KEY")
    if not resolved_api_key:
        raise ValueError("api_key or MISTRAL_API_KEY is required")
    base_url = (
        base_url
        or os.environ.get("MISTRAL_AUDIO_BASE_URL", "")
        or "https://api.mistral.ai"
    )
    client = WorkerTokenClient(api_key=resolved_api_key, base_url=base_url)

    # Initial fetch resolves ws_url + agent_name (stable); token is re-fetched
    # per connect via the provider so a short TTL never blocks reconnection.
    initial = client.fetch()
    logger.info(
        "Starting custom worker: ws_url=%s agent_name=%s",
        initial.ws_url,
        initial.agent_name,
    )

    server = _build_managed_server(
        ws_url=initial.ws_url,
        token_provider=client.fetch_token,
        **server_kwargs,
    )
    if setup_fnc is not None:
        server.setup_fnc = setup_fnc
    server.rtc_session(agent_name=initial.agent_name)(entrypoint)

    cli.run_app(server)
