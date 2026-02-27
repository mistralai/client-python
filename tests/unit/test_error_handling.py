"""Tests for HTTP error status codes and exception mapping."""

import httpx
import pytest

from mistralai.client.errors import HTTPValidationError, SDKError

from .conftest import VALIDATION_ERROR_RESPONSE, user_msg


# ---------------------------------------------------------------------------
# Sync error tests
# ---------------------------------------------------------------------------


class TestSync422RaisesHttpValidationError:
    def test_422_raises_http_validation_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=VALIDATION_ERROR_RESPONSE,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(HTTPValidationError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 422
        assert exc_info.value.data.detail is not None
        assert len(exc_info.value.data.detail) == 1
        assert exc_info.value.data.detail[0].msg == "field required"


class TestSync400RaisesSDKError:
    def test_400_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                400, text="Bad Request", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 400


class TestSync401RaisesSDKError:
    def test_401_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                401, text="Unauthorized", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 401


class TestSync403RaisesSDKError:
    def test_403_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                403, text="Forbidden", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 403


class TestSync404RaisesSDKError:
    def test_404_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                404, text="Not Found", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 404


class TestSync429RaisesSDKErrorWithoutRetry:
    def test_429_raises_sdk_error_without_retry(self, mock_router, mistral_client):
        """Without retry config, 429 should raise SDKError immediately."""
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                429, text="Too Many Requests", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 429


class TestSync500RaisesSDKError:
    def test_500_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                500,
                text="Internal Server Error",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 500


class TestSync502RaisesSDKError:
    def test_502_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                502, text="Bad Gateway", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 502


class TestSync503RaisesSDKError:
    def test_503_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                503,
                text="Service Unavailable",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 503


class TestSDKErrorHasStatusCode:
    def test_sdk_error_has_status_code(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                418,
                text="I'm a teapot",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert exc_info.value.status_code == 418


class TestSDKErrorHasBody:
    def test_sdk_error_has_body(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                400,
                text="detailed error body",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert "detailed error body" in exc_info.value.body


class TestSDKErrorHasRawResponse:
    def test_sdk_error_has_raw_response(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                500, text="error", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        assert isinstance(exc_info.value.raw_response, httpx.Response)
        assert exc_info.value.raw_response.status_code == 500


class TestBodyTruncation:
    def test_body_truncation(self, mock_router, mistral_client):
        """Body longer than 10000 characters should be truncated in the error message."""
        long_body = "x" * 15_000
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                400, text=long_body, headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            mistral_client.chat.complete(model="m", messages=user_msg())

        message = str(exc_info.value)
        assert "...and 5000 more chars" in message


# ---------------------------------------------------------------------------
# Async error tests
# ---------------------------------------------------------------------------


class TestAsync422RaisesHttpValidationError:
    @pytest.mark.asyncio
    async def test_async_422_raises_http_validation_error(
        self, mock_router, mistral_client
    ):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=VALIDATION_ERROR_RESPONSE,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(HTTPValidationError) as exc_info:
            await mistral_client.chat.complete_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 422
        assert exc_info.value.data.detail is not None


class TestAsync400RaisesSDKError:
    @pytest.mark.asyncio
    async def test_async_400_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                400, text="Bad Request", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            await mistral_client.chat.complete_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 400


class TestAsync500RaisesSDKError:
    @pytest.mark.asyncio
    async def test_async_500_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                500,
                text="Internal Server Error",
                headers={"content-type": "text/plain"},
            )
        )

        with pytest.raises(SDKError) as exc_info:
            await mistral_client.chat.complete_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 500


class TestAsync429RaisesSDKError:
    @pytest.mark.asyncio
    async def test_async_429_raises_sdk_error(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                429, text="Too Many Requests", headers={"content-type": "text/plain"}
            )
        )

        with pytest.raises(SDKError) as exc_info:
            await mistral_client.chat.complete_async(model="m", messages=user_msg())

        assert exc_info.value.status_code == 429


# ---------------------------------------------------------------------------
# Stream error test
# ---------------------------------------------------------------------------


class TestStream422RaisesHttpValidationError:
    def test_stream_422_raises_http_validation_error(
        self, mock_router, mistral_client
    ):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                422,
                json=VALIDATION_ERROR_RESPONSE,
                headers={"content-type": "application/json"},
            )
        )

        with pytest.raises(HTTPValidationError) as exc_info:
            mistral_client.chat.stream(model="m", messages=user_msg())

        assert exc_info.value.status_code == 422
        assert exc_info.value.data.detail is not None
