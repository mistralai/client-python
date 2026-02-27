"""Tests for agents.complete() and agents.complete_async()."""

import json
from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers (from conftest, which cannot be directly imported)
# ---------------------------------------------------------------------------

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


def _user_msg(content: str = "Hello") -> list[dict[str, str]]:
    return [{"role": "user", "content": content}]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAgentsCompleteReturnsResponse:
    def test_agents_complete_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )

        result = mistral_client.agents.complete(
            agent_id="agent-123", messages=_user_msg()
        )

        assert result is not None
        assert result.id == "test-001"
        assert result.choices[0].message.content == "Hello."


class TestAgentIdInRequestBody:
    def test_agent_id_in_request_body(self, mock_router, mistral_client):
        route = mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )

        mistral_client.agents.complete(agent_id="agent-123", messages=_user_msg())

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["agent_id"] == "agent-123"


class TestAgentsCompleteAsync:
    @pytest.mark.asyncio
    async def test_agents_complete_async(self, mock_router, mistral_client):
        mock_router.post("/v1/agents/completions").mock(
            return_value=httpx.Response(200, json=CHAT_COMPLETION_RESPONSE)
        )

        result = await mistral_client.agents.complete_async(
            agent_id="agent-123", messages=_user_msg()
        )

        assert result is not None
        assert result.id == "test-001"
        assert result.choices[0].message.content == "Hello."


class TestAgentsCompleteWithTools:
    def test_agents_complete_with_tools(self, mock_router, mistral_client):
        route = mock_router.post("/v1/agents/completions").mock(
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
                        "required": ["city"],
                    },
                },
            }
        ]

        result = mistral_client.agents.complete(
            agent_id="agent-123", messages=_user_msg(), tools=tools
        )

        assert result is not None
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["tools"] is not None
        assert body["tools"][0]["function"]["name"] == "get_weather"
