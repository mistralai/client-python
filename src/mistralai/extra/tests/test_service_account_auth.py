"""Tests for service-account auth over HTTP and the realtime handshake."""

import asyncio
from pathlib import Path
from typing import Callable, Optional, Union

import httpx2 as httpx
import pytest

from mistralai.client import Mistral
from mistralai.client.models import UserMessage
from mistralai.client._hooks.service_account_auth import (
    ServiceAccountTokenError,
    read_service_account_token,
)
from mistralai.extra.exceptions import RealtimeTranscriptionException
from mistralai.extra.realtime import transcription


class _StopHandshake(Exception):
    """Aborts connect() once the headers have been captured, so no socket is opened."""


CHAT_RESPONSE = {
    "id": "cmpl-test",
    "object": "chat.completion",
    "model": "mistral-small-latest",
    "created": 0,
    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "ok"},
            "finish_reason": "stop",
        }
    ],
}

MESSAGES = [UserMessage(content="hi")]


@pytest.fixture(autouse=True)
def clean_auth_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    monkeypatch.delenv("MISTRAL_SA_TOKEN_PATH", raising=False)


@pytest.fixture
def sa_token(tmp_path: Path) -> Path:
    token_file = tmp_path / "token"
    token_file.write_text("sa-token-v1\n")
    return token_file


def sent_authorization(
    api_key: Optional[Union[str, Callable[[], Optional[str]]]] = None,
    http_headers: Optional[dict[str, str]] = None,
) -> Optional[str]:
    """Drive one chat request through a mock transport and return the Authorization header."""
    seen: list[Optional[str]] = []

    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request.headers.get("Authorization"))
        return httpx.Response(200, json=CHAT_RESPONSE)

    client = Mistral(
        api_key=api_key,
        server_url="https://api.mistral.ai",
        client=httpx.Client(transport=httpx.MockTransport(handle)),
    )
    client.chat.complete(
        model="mistral-small-latest", messages=MESSAGES, http_headers=http_headers
    )
    return seen[-1]


class TestReadServiceAccountToken:
    def test_unset_path_reads_nothing(self) -> None:
        assert read_service_account_token() is None

    def test_rereads_the_file_on_every_call(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))
        assert read_service_account_token() == "sa-token-v1"

        sa_token.write_text("sa-token-v2\n")

        assert read_service_account_token() == "sa-token-v2"

    def test_missing_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(tmp_path / "absent"))

        with pytest.raises(ServiceAccountTokenError, match="Failed to read"):
            read_service_account_token()

    def test_empty_file(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        token_file = tmp_path / "token"
        token_file.write_text("   \n")
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(token_file))

        with pytest.raises(ServiceAccountTokenError, match="is empty"):
            read_service_account_token()


class TestServiceAccountAuthHook:
    def test_explicit_api_key_is_not_overridden(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "env-key")
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        assert sent_authorization(api_key="explicit-key") == "Bearer explicit-key"

    def test_callable_api_key_is_not_overridden(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        assert (
            sent_authorization(api_key=lambda: "from-callable")
            == "Bearer from-callable"
        )

    def test_sa_token_is_injected_over_the_api_key(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "env-key")
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        assert sent_authorization() == "Bearer sa-token-v1"

    def test_rotated_token_is_picked_up_by_a_live_client(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))
        seen: list[Optional[str]] = []

        def handle(request: httpx.Request) -> httpx.Response:
            seen.append(request.headers.get("Authorization"))
            return httpx.Response(200, json=CHAT_RESPONSE)

        client = Mistral(
            server_url="https://api.mistral.ai",
            client=httpx.Client(transport=httpx.MockTransport(handle)),
        )
        client.chat.complete(model="mistral-small-latest", messages=MESSAGES)
        sa_token.write_text("sa-token-v2\n")
        client.chat.complete(model="mistral-small-latest", messages=MESSAGES)

        assert seen == ["Bearer sa-token-v1", "Bearer sa-token-v2"]

    def test_api_key_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "env-key")

        assert sent_authorization() == "Bearer env-key"

    def test_api_key_already_carrying_the_bearer_prefix(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "Bearer env-key")

        assert sent_authorization() == "Bearer env-key"

    def test_no_credentials_sends_no_header(self) -> None:
        assert sent_authorization() is None

    def test_unreadable_sa_token_surfaces_the_error(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(tmp_path / "absent"))

        with pytest.raises(ServiceAccountTokenError):
            sent_authorization()


class TestCallerHeaderOverride:
    """A per-request http_headers Authorization outranks the ambient provider on both transports.

    http_headers is applied at request-build time, before hooks run, so the hook has to recognise
    it and step aside.
    """

    def test_beats_the_sa_token(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        sent = sent_authorization(http_headers={"Authorization": "Bearer caller"})

        assert sent == "Bearer caller"

    def test_beats_the_env_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "env-key")

        sent = sent_authorization(http_headers={"Authorization": "Bearer caller"})

        assert sent == "Bearer caller"

    def test_an_unrelated_header_does_not_suppress_the_sa_token(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        sent = sent_authorization(http_headers={"X-Trace": "abc"})

        assert sent == "Bearer sa-token-v1"

    def test_survives_a_missing_token_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(tmp_path / "absent"))

        sent = sent_authorization(http_headers={"Authorization": "Bearer caller"})

        assert sent == "Bearer caller"


class TestRealtimeHandshake:
    """The websocket handshake bypasses before_request hooks, so it resolves auth on its own."""

    @staticmethod
    def handshake_headers(
        monkeypatch: pytest.MonkeyPatch,
        api_key: Optional[str] = None,
        http_headers: Optional[dict[str, str]] = None,
    ) -> dict[str, str]:
        captured: dict[str, str] = {}

        async def fake_connect(
            _url: str, *, additional_headers: dict[str, str], **_: object
        ) -> None:
            captured.update(additional_headers)
            raise _StopHandshake

        monkeypatch.setattr(transcription, "connect", fake_connect)
        client = Mistral(api_key=api_key, server_url="https://api.mistral.ai")
        with pytest.raises(RealtimeTranscriptionException):
            asyncio.run(
                client.audio.realtime.connect(
                    model="voxtral-mini-latest", http_headers=http_headers
                )
            )
        return captured

    def test_sa_token_is_used_over_the_api_key(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_API_KEY", "env-key")
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        headers = self.handshake_headers(monkeypatch)

        assert headers["Authorization"] == "Bearer sa-token-v1"

    def test_explicit_api_key_wins(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))

        headers = self.handshake_headers(monkeypatch, api_key="explicit-key")

        assert headers["Authorization"] == "Bearer explicit-key"

    def test_no_credentials_sends_no_header(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        assert "Authorization" not in self.handshake_headers(monkeypatch)

    def test_matches_the_http_path_on_a_caller_override(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))
        override = {"Authorization": "Bearer caller"}

        handshake = self.handshake_headers(monkeypatch, http_headers=override)

        assert handshake["Authorization"] == sent_authorization(http_headers=override)

    def test_caller_override_survives_a_missing_token_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(tmp_path / "absent"))

        headers = self.handshake_headers(
            monkeypatch, http_headers={"authorization": "Bearer caller"}
        )

        assert headers["authorization"] == "Bearer caller"


@pytest.mark.asyncio
async def test_async_requests_use_the_sa_token(
    monkeypatch: pytest.MonkeyPatch, sa_token: Path
) -> None:
    monkeypatch.setenv("MISTRAL_API_KEY", "env-key")
    monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(sa_token))
    seen: list[Optional[str]] = []

    async def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request.headers.get("Authorization"))
        return httpx.Response(200, json=CHAT_RESPONSE)

    client = Mistral(
        server_url="https://api.mistral.ai",
        async_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
    )
    await client.chat.complete_async(model="mistral-small-latest", messages=MESSAGES)

    assert seen == ["Bearer sa-token-v1"]
