"""Tests for structured outputs: chat.parse(), response_format_from_pydantic_model()."""

import json
from typing import Optional

import httpx
import pytest
from pydantic import BaseModel

from mistralai.client import models
from mistralai.client.utils.eventstreaming import EventStream, EventStreamAsync
from mistralai.extra.struct_chat import (
    ParsedChatCompletionResponse,
    convert_to_parsed_chat_completion_response,
)
from mistralai.extra.utils.response_format import response_format_from_pydantic_model

from .conftest import CHAT_COMPLETION_RESPONSE, make_sse_body, make_stream_chunk, user_msg


# ---------------------------------------------------------------------------
# Test Pydantic models
# ---------------------------------------------------------------------------


class WeatherResponse(BaseModel):
    temperature: float
    description: str


class Location(BaseModel):
    city: str
    country: str


class NestedResponse(BaseModel):
    location: Location
    temperature: float


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _chat_response_with_content(content_str):
    """Build a chat completion response payload with custom message content."""
    resp = {**CHAT_COMPLETION_RESPONSE}
    resp["choices"] = [
        {
            "index": 0,
            "message": {"role": "assistant", "content": content_str},
            "finish_reason": "stop",
        }
    ]
    return resp


def _chat_response_with_none_content():
    """Build a chat completion response payload with None message content."""
    resp = {**CHAT_COMPLETION_RESPONSE}
    resp["choices"] = [
        {
            "index": 0,
            "message": {"role": "assistant", "content": None},
            "finish_reason": "stop",
        }
    ]
    return resp


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestParseReturnsParsedResponse:
    def test_parse_returns_parsed_response(self, mock_router, mistral_client):
        content = json.dumps({"temperature": 72.5, "description": "Sunny"})
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        result = mistral_client.chat.parse(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("What is the weather?"),
        )

        assert isinstance(result, ParsedChatCompletionResponse)
        assert result.choices is not None
        assert len(result.choices) == 1
        parsed = result.choices[0].message.parsed
        assert isinstance(parsed, WeatherResponse)
        assert parsed.temperature == 72.5
        assert parsed.description == "Sunny"


class TestParseRequestHasJsonSchemaFormat:
    def test_parse_request_has_json_schema_format(self, mock_router, mistral_client):
        content = json.dumps({"temperature": 72.5, "description": "Sunny"})
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        mistral_client.chat.parse(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("What is the weather?"),
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["response_format"]["type"] == "json_schema"
        assert body["response_format"]["json_schema"]["strict"] is True
        assert body["response_format"]["json_schema"]["name"] == "WeatherResponse"


class TestParseNestedModel:
    def test_parse_nested_model(self, mock_router, mistral_client):
        content = json.dumps(
            {
                "location": {"city": "Paris", "country": "France"},
                "temperature": 18.0,
            }
        )
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        result = mistral_client.chat.parse(
            response_format=NestedResponse,
            model="m",
            messages=user_msg("Weather in Paris?"),
        )

        parsed = result.choices[0].message.parsed
        assert isinstance(parsed, NestedResponse)
        assert isinstance(parsed.location, Location)
        assert parsed.location.city == "Paris"
        assert parsed.location.country == "France"
        assert parsed.temperature == 18.0


class TestParseNoneContent:
    def test_parse_none_content(self, mock_router, mistral_client):
        response_payload = _chat_response_with_none_content()
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        result = mistral_client.chat.parse(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("Hello"),
        )

        assert result.choices[0].message.parsed is None


class TestParseAsync:
    @pytest.mark.asyncio
    async def test_parse_async(self, mock_router, mistral_client):
        content = json.dumps({"temperature": 25.0, "description": "Cloudy"})
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        result = await mistral_client.chat.parse_async(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("Weather?"),
        )

        assert isinstance(result, ParsedChatCompletionResponse)
        parsed = result.choices[0].message.parsed
        assert isinstance(parsed, WeatherResponse)
        assert parsed.temperature == 25.0
        assert parsed.description == "Cloudy"


class TestParseStreamReturnsEventStream:
    def test_parse_stream_returns_event_stream(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk('{"temperature":'),
            make_stream_chunk(" 72.5}", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = mistral_client.chat.parse_stream(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("Weather?"),
        )

        assert isinstance(stream, EventStream)
        results = list(stream)
        assert len(results) == 2


class TestResponseFormatFromPydanticModel:
    def test_response_format_from_pydantic_model(self):
        fmt = response_format_from_pydantic_model(WeatherResponse)

        assert fmt.type == "json_schema"
        assert fmt.json_schema is not None
        assert fmt.json_schema.strict is True
        assert fmt.json_schema.name == "WeatherResponse"
        # The schema should contain the model's properties
        schema = fmt.json_schema.schema_definition
        assert "properties" in schema
        assert "temperature" in schema["properties"]
        assert "description" in schema["properties"]


class TestParseInvalidJsonRaises:
    def test_parse_invalid_json_raises(self, mock_router, mistral_client):
        """If the model returns content that is not valid JSON, parsing should fail."""
        response_payload = _chat_response_with_content("this is not json")
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        with pytest.raises((json.JSONDecodeError, Exception)):
            mistral_client.chat.parse(
                response_format=WeatherResponse,
                model="m",
                messages=user_msg("Weather?"),
            )


class TestParseStreamAsyncReturnsEventStream:
    @pytest.mark.asyncio
    async def test_parse_stream_async_returns_event_stream(self, mock_router, mistral_client):
        chunks = [
            make_stream_chunk('{"temperature":'),
            make_stream_chunk(" 72.5}", finish_reason="stop"),
        ]
        sse = make_sse_body(chunks)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200, content=sse, headers={"content-type": "text/event-stream"}
            )
        )

        stream = await mistral_client.chat.parse_stream_async(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("Weather?"),
        )

        assert isinstance(stream, EventStreamAsync)
        results = []
        async for event in stream:
            results.append(event)
        assert len(results) == 2


class TestParseWithOptionalFields:
    def test_parse_with_optional_fields(self, mock_router, mistral_client):
        class PartialWeather(BaseModel):
            temperature: float
            description: Optional[str] = None

        content = json.dumps({"temperature": 65.0})
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        result = mistral_client.chat.parse(
            response_format=PartialWeather,
            model="m",
            messages=user_msg("Weather?"),
        )

        parsed = result.choices[0].message.parsed
        assert isinstance(parsed, PartialWeather)
        assert parsed.temperature == 65.0
        assert parsed.description is None


class TestResponseFormatSchemaHasRequiredFields:
    def test_response_format_schema_has_required_fields(self):
        fmt = response_format_from_pydantic_model(WeatherResponse)

        schema = fmt.json_schema.schema_definition
        assert "required" in schema
        assert "temperature" in schema["required"]
        assert "description" in schema["required"]


class TestParseRequestIncludesModelName:
    def test_parse_request_includes_model_name(self, mock_router, mistral_client):
        content = json.dumps({"temperature": 72.5, "description": "Sunny"})
        response_payload = _chat_response_with_content(content)
        mock_router.post("/v1/chat/completions").mock(
            return_value=httpx.Response(200, json=response_payload)
        )

        mistral_client.chat.parse(
            response_format=WeatherResponse,
            model="m",
            messages=user_msg("Weather?"),
        )

        body = json.loads(mock_router.calls.last.request.content)
        assert body["response_format"]["json_schema"]["name"] == "WeatherResponse"
