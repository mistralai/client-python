"""Tests for RealtimeTranscription URL building."""

import pytest

from mistralai.extra.realtime.transcription import RealtimeTranscription
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils.logger import get_default_logger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_rt(server_url: str = "https://api.mistral.ai") -> RealtimeTranscription:
    config = SDKConfiguration(
        client=None,
        client_supplied=False,
        async_client=None,
        async_client_supplied=False,
        debug_logger=get_default_logger(),
        server_url=server_url,
    )
    return RealtimeTranscription(config)


# -------------------------------------------------------------------------
# 1. HTTPS server URL converted to WSS in connect flow
# -------------------------------------------------------------------------


class TestBuildUrlHttpsToWss:
    def test_build_url_https_to_wss(self):
        rt = _make_rt("https://api.mistral.ai")
        url = rt._build_url("mistral-small-latest", server_url=None, query_params={})

        # _build_url produces the HTTPS URL; the WSS conversion happens in connect().
        # Verify the URL is HTTPS-based (connect() replaces https -> wss)
        assert url.startswith("https://api.mistral.ai")
        assert "/v1/audio/transcriptions/realtime" in url


# -------------------------------------------------------------------------
# 2. HTTP -> WS (via _build_url producing http URL)
# -------------------------------------------------------------------------


class TestBuildUrlHttpToWs:
    def test_build_url_http_to_ws(self):
        rt = _make_rt("http://localhost:8080")
        url = rt._build_url("mistral-small-latest", server_url=None, query_params={})

        assert url.startswith("http://localhost:8080")
        assert "/v1/audio/transcriptions/realtime" in url


# -------------------------------------------------------------------------
# 3. Model included in query params
# -------------------------------------------------------------------------


class TestBuildUrlIncludesModel:
    def test_build_url_includes_model(self):
        rt = _make_rt()
        url = rt._build_url("mistral-large-latest", server_url=None, query_params={})

        assert "model=mistral-large-latest" in url


# -------------------------------------------------------------------------
# 4. Custom server_url overrides config
# -------------------------------------------------------------------------


class TestBuildUrlWithCustomServer:
    def test_build_url_with_custom_server(self):
        rt = _make_rt("https://api.mistral.ai")
        url = rt._build_url(
            "mistral-small-latest",
            server_url="https://custom.server.com",
            query_params={},
        )

        assert url.startswith("https://custom.server.com")
        assert "model=mistral-small-latest" in url


# -------------------------------------------------------------------------
# 5. Connect error raises RealtimeTranscriptionException
# -------------------------------------------------------------------------


class TestConnectErrorRaises:
    @pytest.mark.asyncio
    async def test_connect_error_raises(self):
        from mistralai.extra.exceptions import RealtimeTranscriptionException

        rt = _make_rt("https://nonexistent.server.invalid")

        with pytest.raises(RealtimeTranscriptionException):
            await rt.connect(
                model="mistral-small-latest",
                timeout_ms=1000,
            )


# -------------------------------------------------------------------------
# 6. Additional query params merged
# -------------------------------------------------------------------------


class TestUrlBuildingWithQueryParams:
    def test_url_building_with_query_params(self):
        rt = _make_rt()
        url = rt._build_url(
            "mistral-small-latest",
            server_url=None,
            query_params={"language": "en", "custom_key": "custom_value"},
        )

        assert "model=mistral-small-latest" in url
        assert "language=en" in url
        assert "custom_key=custom_value" in url
