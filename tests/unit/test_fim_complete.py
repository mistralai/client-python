"""Tests for fim.complete() and fim.complete_async()."""

import json
from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

FIM_COMPLETION_RESPONSE: dict[str, Any] = {
    "id": "fim-001",
    "object": "chat.completion",
    "model": "codestral-latest",
    "created": 1700000000,
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "def hello():"},
            "finish_reason": "stop",
        }
    ],
    "usage": {
        "prompt_tokens": 5,
        "completion_tokens": 3,
        "total_tokens": 8,
    },
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFimCompleteReturnsResponse:
    def test_fim_complete_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(200, json=FIM_COMPLETION_RESPONSE)
        )

        result = mistral_client.fim.complete(
            model="codestral-latest", prompt="def hello():"
        )

        assert result is not None
        assert result.id == "fim-001"
        assert result.choices[0].message.content == "def hello():"


class TestFimPromptAndSuffixInBody:
    def test_fim_prompt_and_suffix_in_body(self, mock_router, mistral_client):
        route = mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(200, json=FIM_COMPLETION_RESPONSE)
        )

        mistral_client.fim.complete(
            model="codestral-latest",
            prompt="def hello():",
            suffix="    return 'hello'",
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["prompt"] == "def hello():"
        assert body["suffix"] == "    return 'hello'"


class TestFimCompleteAsync:
    @pytest.mark.asyncio
    async def test_fim_complete_async(self, mock_router, mistral_client):
        mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(200, json=FIM_COMPLETION_RESPONSE)
        )

        result = await mistral_client.fim.complete_async(
            model="codestral-latest", prompt="def hello():"
        )

        assert result is not None
        assert result.id == "fim-001"


class TestFimWithOptionalParams:
    def test_fim_with_optional_params(self, mock_router, mistral_client):
        route = mock_router.post("/v1/fim/completions").mock(
            return_value=httpx.Response(200, json=FIM_COMPLETION_RESPONSE)
        )

        mistral_client.fim.complete(
            model="codestral-latest",
            prompt="def hello():",
            temperature=0.5,
            max_tokens=100,
            min_tokens=10,
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["temperature"] == 0.5
        assert body["max_tokens"] == 100
        assert body["min_tokens"] == 10
