"""Tests for synchronous chat.complete() endpoint."""

import json

import httpx
import pytest

from mistralai.client import models

from .conftest import CHAT_COMPLETION_RESPONSE, user_msg


class TestBasicCompletion:
    def test_basic_completion(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        result = mistral_client.chat.complete(model="mistral-small-latest", messages=user_msg())

        assert isinstance(result, models.ChatCompletionResponse)
        assert result.id == "test-001"
        assert result.model == "mistral-small-latest"
        assert result.choices is not None
        assert len(result.choices) == 1
        assert result.choices[0].message.content == "Hello."
        assert result.choices[0].finish_reason == "stop"
        assert result.usage is not None
        assert result.usage.prompt_tokens == 10
        assert result.usage.completion_tokens == 5
        assert result.usage.total_tokens == 15


class TestRequestBodySerialization:
    def test_request_body_serialization(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="mistral-small-latest", messages=user_msg("Hi"))

        body = json.loads(mock_router.calls.last.request.content)
        assert body["model"] == "mistral-small-latest"
        assert len(body["messages"]) == 1
        assert body["messages"][0]["role"] == "user"
        assert body["messages"][0]["content"] == "Hi"


class TestAuthorizationHeader:
    def test_authorization_header(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg())

        auth = mock_router.calls.last.request.headers.get("authorization")
        assert auth == "Bearer test-key"


class TestCustomHttpHeaders:
    def test_custom_http_headers(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(
            model="m",
            messages=user_msg(),
            http_headers={"x-custom": "value123"},
        )

        headers = mock_router.calls.last.request.headers
        assert headers.get("x-custom") == "value123"
        # Default headers like authorization should still be present
        assert headers.get("authorization") == "Bearer test-key"


class TestTemperatureParameter:
    def test_temperature_parameter(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), temperature=0.3)

        body = json.loads(mock_router.calls.last.request.content)
        assert body["temperature"] == 0.3


class TestMaxTokensParameter:
    def test_max_tokens_parameter(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), max_tokens=256)

        body = json.loads(mock_router.calls.last.request.content)
        assert body["max_tokens"] == 256


class TestStopAsString:
    def test_stop_as_string(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), stop="END")

        body = json.loads(mock_router.calls.last.request.content)
        assert body["stop"] == "END"


class TestStopAsList:
    def test_stop_as_list(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), stop=["END", "STOP"])

        body = json.loads(mock_router.calls.last.request.content)
        assert body["stop"] == ["END", "STOP"]


class TestRandomSeed:
    def test_random_seed(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), random_seed=42)

        body = json.loads(mock_router.calls.last.request.content)
        assert body["random_seed"] == 42
        assert isinstance(body["random_seed"], int)


class TestNParameter:
    def test_n_parameter(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), n=2)

        body = json.loads(mock_router.calls.last.request.content)
        assert body["n"] == 2


class TestPresenceFrequencyPenalty:
    def test_presence_frequency_penalty(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(
            model="m",
            messages=user_msg(),
            presence_penalty=0.5,
            frequency_penalty=0.8,
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["presence_penalty"] == 0.5
        assert body["frequency_penalty"] == 0.8


class TestResponseFormatJsonObject:
    def test_response_format_json_object(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(
            model="m",
            messages=user_msg(),
            response_format={"type": "json_object"},
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["response_format"]["type"] == "json_object"


class TestUserAgentHeader:
    def test_user_agent_header(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg())

        headers = mock_router.calls.last.request.headers
        assert "user-agent" in headers


class TestToolCallingSerialization:
    def test_tool_calling_serialization(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather",
                    "parameters": {
                        "type": "object",
                        "properties": {"city": {"type": "string"}},
                    },
                },
            }
        ]
        mistral_client.chat.complete(model="m", messages=user_msg(), tools=tools)

        body = json.loads(mock_router.calls.last.request.content)
        assert "tools" in body
        assert len(body["tools"]) == 1
        assert body["tools"][0]["type"] == "function"
        assert body["tools"][0]["function"]["name"] == "get_weather"


class TestToolChoiceAuto:
    def test_tool_choice_auto(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), tool_choice="auto")

        body = json.loads(mock_router.calls.last.request.content)
        assert body["tool_choice"] == "auto"


class TestToolChoiceAny:
    def test_tool_choice_any(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )
        mistral_client.chat.complete(model="m", messages=user_msg(), tool_choice="any")

        body = json.loads(mock_router.calls.last.request.content)
        assert body["tool_choice"] == "any"
