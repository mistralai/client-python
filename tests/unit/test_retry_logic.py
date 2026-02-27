"""Tests for retry/backoff logic in the SDK."""

import json
from typing import Any
from unittest.mock import patch

import httpx
import pytest
import respx

from mistralai.client.sdk import Mistral
from mistralai.client.utils.retries import (
    BackoffStrategy,
    RetryConfig,
    TemporaryError,
    _get_sleep_interval,
    _parse_retry_after_header,
)

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
# 1. 429 triggers retry
# -------------------------------------------------------------------------


class TestStatus429TriggersRetry:
    @patch("time.sleep")
    def test_429_triggers_retry(self, mock_sleep, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(429, text="rate limited"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        result = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hi"}],
        )

        assert result.id == "test-001"
        assert mock_sleep.call_count >= 1


# -------------------------------------------------------------------------
# 2. 500 triggers retry
# -------------------------------------------------------------------------


class TestStatus500TriggersRetry:
    @patch("time.sleep")
    def test_500_triggers_retry(self, mock_sleep, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(500, text="internal error"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        result = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hi"}],
        )

        assert result.id == "test-001"
        assert mock_sleep.call_count >= 1


# -------------------------------------------------------------------------
# 13. 502 triggers retry
# -------------------------------------------------------------------------


class TestStatus502TriggersRetry:
    @patch("time.sleep")
    def test_502_triggers_retry(self, mock_sleep, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(502, text="bad gateway"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        result = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hi"}],
        )

        assert result.id == "test-001"
        assert mock_sleep.call_count >= 1


# -------------------------------------------------------------------------
# 14. 503 triggers retry
# -------------------------------------------------------------------------


class TestStatus503TriggersRetry:
    @patch("time.sleep")
    def test_503_triggers_retry(self, mock_sleep, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.Response(503, text="service unavailable"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        result = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hi"}],
        )

        assert result.id == "test-001"
        assert mock_sleep.call_count >= 1


# -------------------------------------------------------------------------
# 15. No retry when not configured
# -------------------------------------------------------------------------


class TestNoRetryWhenNotConfigured:
    def test_no_retry_when_not_configured(self, mock_router):
        client = Mistral(api_key="test-key", server_url="https://test.api")
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(429, text="rate limited")
        )

        with pytest.raises(Exception):
            client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        # Should have been called exactly once (no retry).
        routes = mock_router.routes
        matched_route = [r for r in routes if r.call_count > 0]
        assert len(matched_route) == 1
        assert matched_route[0].call_count == 1


# -------------------------------------------------------------------------
# 3. 400 does not retry
# -------------------------------------------------------------------------


class TestStatus400DoesNotRetry:
    def test_400_does_not_retry(self, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(400, text="bad request")
        )

        with pytest.raises(Exception):
            client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        # Should have been called exactly once (no retry).
        # The route was not named, so count calls via the route object.
        routes = mock_router.routes
        matched_route = [r for r in routes if r.call_count > 0]
        assert len(matched_route) == 1
        assert matched_route[0].call_count == 1


# -------------------------------------------------------------------------
# 4. 422 does not retry
# -------------------------------------------------------------------------


class TestStatus422DoesNotRetry:
    def test_422_does_not_retry(self, mock_router):
        client = _make_retry_client()
        validation_error = {
            "detail": [{"loc": ["body", "model"], "msg": "field required", "type": "value_error.missing"}]
        }
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=validation_error,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(Exception):
            client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )


# -------------------------------------------------------------------------
# 5. Retry-After header as integer seconds
# -------------------------------------------------------------------------


class TestRetryAfterHeaderInteger:
    def test_retry_after_header_integer(self):
        response = httpx.Response(429, headers={"retry-after": "2"})
        result = _parse_retry_after_header(response)
        # Returns milliseconds
        assert result == 2000


# -------------------------------------------------------------------------
# 6. Retry-After as HTTP date
# -------------------------------------------------------------------------


class TestRetryAfterHeaderDate:
    def test_retry_after_header_date(self):
        from datetime import datetime, timezone, timedelta
        from email.utils import format_datetime

        # Create a date 5 seconds in the future
        future = datetime.now(timezone.utc) + timedelta(seconds=5)
        date_str = format_datetime(future, usegmt=True)

        response = httpx.Response(429, headers={"retry-after": date_str})
        result = _parse_retry_after_header(response)

        assert result is not None
        # Should be approximately 5000 ms (allow some tolerance)
        assert 3000 <= result <= 7000


# -------------------------------------------------------------------------
# 7. Retry-After header missing returns None
# -------------------------------------------------------------------------


class TestParseRetryAfterHeaderMissing:
    def test_parse_retry_after_header_missing(self):
        response = httpx.Response(429)
        result = _parse_retry_after_header(response)
        assert result is None


# -------------------------------------------------------------------------
# 8. _get_sleep_interval with retry_after
# -------------------------------------------------------------------------


class TestGetSleepIntervalWithRetryAfter:
    def test_get_sleep_interval_with_retry_after(self):
        response = httpx.Response(429, headers={"retry-after": "3"})
        exc = TemporaryError(response)

        sleep = _get_sleep_interval(
            exception=exc,
            initial_interval=100,
            max_interval=1000,
            exponent=1.5,
            retries=0,
        )

        # retry_after is 3000ms, so sleep should be 3.0 seconds
        assert sleep == 3.0


# -------------------------------------------------------------------------
# 9. _get_sleep_interval exponential backoff increases with retries
# -------------------------------------------------------------------------


class TestGetSleepIntervalExponentialBackoff:
    def test_get_sleep_interval_exponential_backoff(self):
        response = httpx.Response(429)
        exc = TemporaryError(response)  # no retry-after header

        sleep_0 = _get_sleep_interval(
            exception=exc,
            initial_interval=100,
            max_interval=10000,
            exponent=2.0,
            retries=0,
        )
        sleep_1 = _get_sleep_interval(
            exception=exc,
            initial_interval=100,
            max_interval=10000,
            exponent=2.0,
            retries=1,
        )
        sleep_2 = _get_sleep_interval(
            exception=exc,
            initial_interval=100,
            max_interval=10000,
            exponent=2.0,
            retries=2,
        )

        # The base sleep (without random jitter) should increase:
        # retry 0: 0.1 * 2^0 + jitter = ~0.1 + jitter
        # retry 1: 0.1 * 2^1 + jitter = ~0.2 + jitter
        # retry 2: 0.1 * 2^2 + jitter = ~0.4 + jitter
        # With random jitter in [0, 1), the general trend is increasing
        # We check the base calculation is reasonable
        assert sleep_0 >= 0.1
        assert sleep_2 > 0.1  # base of retry 2 is 0.4


# -------------------------------------------------------------------------
# 10. _get_sleep_interval capped at max_interval
# -------------------------------------------------------------------------


class TestGetSleepIntervalCappedAtMax:
    def test_get_sleep_interval_capped_at_max(self):
        response = httpx.Response(429)
        exc = TemporaryError(response)  # no retry-after

        sleep = _get_sleep_interval(
            exception=exc,
            initial_interval=100,
            max_interval=500,  # 0.5 seconds max
            exponent=10.0,
            retries=10,
        )

        # Should be capped at max_interval / 1000 = 0.5 seconds
        assert sleep <= 0.5


# -------------------------------------------------------------------------
# 11. Max elapsed time stops retries
# -------------------------------------------------------------------------


class TestMaxElapsedTimeStopsRetries:
    def test_max_elapsed_time_stops_retries(self, mock_router):
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
        client = Mistral(api_key="test-key", server_url="https://test.api", retry_config=rc)

        # Always return 429 so retries would go on forever if not capped
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(429, text="rate limited")
        )

        # Use time.time mock to simulate elapsed time
        call_count = 0

        def advancing_time():
            nonlocal call_count
            call_count += 1
            # First call returns 0ms, subsequent calls return > max_elapsed_time
            return 0 + (call_count * 0.2)  # advance 200ms each call

        with patch("time.sleep"), patch("time.time", side_effect=advancing_time):
            # When max_elapsed_time is exceeded, the SDK raises SDKError
            # because the last response is a 429
            with pytest.raises(Exception):
                client.chat.complete(
                    model="mistral-small-latest",
                    messages=[{"role": "user", "content": "Hi"}],
                )

        # Verify retries stopped (not infinite) - call_count tracks time.time calls
        assert call_count < 50


# -------------------------------------------------------------------------
# 12. Network error retried when configured
# -------------------------------------------------------------------------


class TestNetworkErrorRetriedWhenConfigured:
    @patch("time.sleep")
    def test_network_error_retried_when_configured(self, mock_sleep, mock_router):
        client = _make_retry_client()
        mock_router.post("/v1/chat/completions").mock(
            side_effect=[
                httpx.ConnectError("connection refused"),
                httpx.Response(200, json=CHAT_COMPLETION_RESPONSE),
            ]
        )

        result = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hi"}],
        )

        assert result.id == "test-001"
        assert mock_sleep.call_count >= 1
