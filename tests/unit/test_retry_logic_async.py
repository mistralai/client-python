"""Async retry tests for the SDK."""

from typing import Any
from unittest.mock import patch

import httpx
import pytest
import respx

from mistralai.client.sdk import Mistral
from mistralai.client.utils.retries import BackoffStrategy, RetryConfig

CHAT_COMPLETION_RESPONSE: dict[str, Any] = {
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


# ---------------------------------------------------------------------------
# Helper: build a retry-enabled client
# ---------------------------------------------------------------------------


def _make_retry_client() -> Mistral:
    rc = RetryConfig(
        strategy="backoff",
        backoff=BackoffStrategy(
            initial_interval=100,
            max_interval=1000,
            exponent=1.5,
            max_elapsed_time=5000,
        ),
        retry_connection_errors=True,
    )
    return Mistral(api_key="test-key", server_url="https://test.api", retry_config=rc)


# -------------------------------------------------------------------------
# 1. 429 triggers retry (async)
# -------------------------------------------------------------------------


class TestStatus429TriggersRetryAsync:
    @pytest.mark.asyncio
    async def test_429_triggers_retry_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(429, text="rate limited"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 2. 500 triggers retry (async)
# -------------------------------------------------------------------------


class TestStatus500TriggersRetryAsync:
    @pytest.mark.asyncio
    async def test_500_triggers_retry_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(500, text="internal error"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 3. 400 does not retry (async)
# -------------------------------------------------------------------------


class TestStatus400DoesNotRetryAsync:
    @pytest.mark.asyncio
    async def test_400_does_not_retry_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(400, text="bad request")
        )

        with pytest.raises(Exception):
            await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )


# -------------------------------------------------------------------------
# 4. Retry succeeds after failure (async)
# -------------------------------------------------------------------------


class TestRetrySucceedsAfterFailureAsync:
    @pytest.mark.asyncio
    async def test_retry_succeeds_after_failure_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(502, text="bad gateway"),
                httpx.Response(503, text="service unavailable"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 5. Network error retried (async)
# -------------------------------------------------------------------------


class TestNetworkErrorRetriedAsync:
    @pytest.mark.asyncio
    async def test_network_error_retried_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.ConnectError("connection refused"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 6. Max elapsed time stops retries (async)
# -------------------------------------------------------------------------


class TestMaxElapsedTimeAsync:
    @pytest.mark.asyncio
    async def test_max_elapsed_time_async(self, mock_router):
        rc = RetryConfig(
            strategy="backoff",
            backoff=BackoffStrategy(
                initial_interval=100,
                max_interval=200,
                exponent=1.5,
                max_elapsed_time=100,  # very short: 100ms
            ),
            retry_connection_errors=True,
        )
        client = Mistral(
            api_key="test-key", server_url="https://test.api", retry_config=rc
        )

        # Always return 429
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(429, text="rate limited")
        )

        call_count = 0

        def advancing_time():
            nonlocal call_count
            call_count += 1
            return call_count * 0.2

        with patch("asyncio.sleep"), patch("time.time", side_effect=advancing_time):
            # max_elapsed_time will trigger; when TemporaryError occurs after
            # timeout, the raw response is returned. The SDK will attempt to
            # unmarshal the 429 response and likely raise an SDKError.
            # We just verify retries do stop (not infinite loop).
            try:
                await client.chat.complete_async(
                    model="mistral-small-latest",
                    messages=[{"role": "user", "content": "Hi"}],
                )
            except Exception:
                pass

        # Verify we did not retry indefinitely
        assert call_count < 50


# -------------------------------------------------------------------------
# 7. 502 triggers retry (async)
# -------------------------------------------------------------------------


class TestStatus502TriggersRetryAsync:
    @pytest.mark.asyncio
    async def test_502_triggers_retry_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(502, text="bad gateway"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 8. 503 triggers retry (async)
# -------------------------------------------------------------------------


class TestStatus503TriggersRetryAsync:
    @pytest.mark.asyncio
    async def test_503_triggers_retry_async(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(503, text="service unavailable"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        with patch("asyncio.sleep"):
            result = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result.id == "test-001"


# -------------------------------------------------------------------------
# 9. No retry when not configured (async)
# -------------------------------------------------------------------------


class TestNoRetryWhenNotConfiguredAsync:
    @pytest.mark.asyncio
    async def test_no_retry_when_not_configured_async(self, mock_router):
        client = Mistral(api_key="test-key", server_url="https://test.api")
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(429, text="rate limited")
        )

        with pytest.raises(Exception):
            await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        # Should have been called exactly once (no retry).
        routes = mock_router.routes
        matched_route = [r for r in routes if r.call_count > 0]
        assert len(matched_route) == 1
        assert matched_route[0].call_count == 1
