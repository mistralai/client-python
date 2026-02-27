"""Tests for asynchronous chat.complete_async() endpoint."""

import json

import httpx
import pytest

from mistralai.client import models

from .conftest import CHAT_COMPLETION_RESPONSE, user_msg


class TestBasicCompletionAsync:
    @pytest.mark.asyncio
    async def test_basic_completion_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        result = await mistral_client.chat.complete_async(
            model="mistral-small-latest", messages=user_msg()
        )

        assert isinstance(result, models.ChatCompletionResponse)
        assert result.id == "test-001"
        assert result.model == "mistral-small-latest"
        assert result.choices is not None
        assert len(result.choices) == 1
        assert result.choices[0].message.content == "Hello."
        assert result.choices[0].finish_reason == "stop"


class TestRequestBodySerializationAsync:
    @pytest.mark.asyncio
    async def test_request_body_serialization_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        await mistral_client.chat.complete_async(
            model="mistral-small-latest", messages=user_msg("Hi")
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["model"] == "mistral-small-latest"
        assert len(body["messages"]) == 1
        assert body["messages"][0]["role"] == "user"
        assert body["messages"][0]["content"] == "Hi"


class TestAuthorizationHeaderAsync:
    @pytest.mark.asyncio
    async def test_authorization_header_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        await mistral_client.chat.complete_async(model="m", messages=user_msg())

        auth = mock_router.calls.last.request.headers.get("authorization")
        assert auth == "Bearer test-key"


class TestTemperatureAsync:
    @pytest.mark.asyncio
    async def test_temperature_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        await mistral_client.chat.complete_async(
            model="m", messages=user_msg(), temperature=0.7
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["temperature"] == 0.7


class TestMaxTokensAsync:
    @pytest.mark.asyncio
    async def test_max_tokens_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        await mistral_client.chat.complete_async(
            model="m", messages=user_msg(), max_tokens=512
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["max_tokens"] == 512


class TestResponseFormatAsync:
    @pytest.mark.asyncio
    async def test_response_format_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        await mistral_client.chat.complete_async(
            model="m",
            messages=user_msg(),
            response_format={"type": "json_object"},
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["response_format"]["type"] == "json_object"
