"""Tests for the Conversations SDK methods (CRUD, streaming, async)."""

import json
from typing import Any

import httpx
import pytest
import respx

from mistralai.client.sdk import Mistral

# ---------------------------------------------------------------------------
# Minimal valid response payloads
# ---------------------------------------------------------------------------

CONVERSATION_RESPONSE: dict[str, Any] = {
    "conversation_id": "conv-001",
    "outputs": [
        {
            "type": "message.output",
            "content": "Hello there!",
            "role": "assistant",
        }
    ],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 5,
        "total_tokens": 15,
    },
    "object": "conversation.response",
}

AGENT_CONVERSATION: dict[str, Any] = {
    "id": "conv-001",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "agent_id": "agent-001",
    "object": "conversation",
}

MODEL_CONVERSATION: dict[str, Any] = {
    "id": "conv-002",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "model": "mistral-small-latest",
    "object": "conversation",
}

CONVERSATION_HISTORY: dict[str, Any] = {
    "conversation_id": "conv-001",
    "entries": [],
    "object": "conversation.history",
}

CONVERSATION_MESSAGES: dict[str, Any] = {
    "conversation_id": "conv-001",
    "messages": [],
    "object": "conversation.messages",
}

USER_INPUTS = [{"role": "user", "content": "Hello"}]


# -------------------------------------------------------------------------
# SSE helpers
# -------------------------------------------------------------------------

def make_conversation_sse_body(events: list[dict[str, Any]]) -> bytes:
    """Build text/event-stream body from event dicts."""
    lines = [f"data: {json.dumps(e)}\n\n" for e in events]
    lines.append("data: [DONE]\n\n")
    return "".join(lines).encode()


# -------------------------------------------------------------------------
# 1. Start conversation
# -------------------------------------------------------------------------


class TestStartConversation:
    def test_start(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = mistral_client.beta.conversations.start(
            inputs=USER_INPUTS,
            model="mistral-small-latest",
        )

        assert result.conversation_id == "conv-001"
        assert result.object == "conversation.response"


# -------------------------------------------------------------------------
# 2. List conversations
# -------------------------------------------------------------------------


class TestListConversations:
    def test_list(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations").mock(
            return_value=httpx.Response(200, json=[MODEL_CONVERSATION])
        )

        result = mistral_client.beta.conversations.list()

        assert len(result) == 1


# -------------------------------------------------------------------------
# 3. Get conversation
# -------------------------------------------------------------------------


class TestGetConversation:
    def test_get(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(200, json=MODEL_CONVERSATION)
        )

        result = mistral_client.beta.conversations.get(conversation_id="conv-001")

        assert result.id == "conv-002"  # from MODEL_CONVERSATION


# -------------------------------------------------------------------------
# 4. Delete conversation
# -------------------------------------------------------------------------


class TestDeleteConversation:
    def test_delete(self, mock_router, mistral_client):
        mock_router.delete("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(204)
        )

        result = mistral_client.beta.conversations.delete(
            conversation_id="conv-001",
        )

        assert result is None


# -------------------------------------------------------------------------
# 5. Append to conversation
# -------------------------------------------------------------------------


class TestAppendConversation:
    def test_append(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = mistral_client.beta.conversations.append(
            conversation_id="conv-001",
            inputs=USER_INPUTS,
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 6. Get history
# -------------------------------------------------------------------------


class TestGetHistory:
    def test_get_history(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001/history").mock(
            return_value=httpx.Response(200, json=CONVERSATION_HISTORY)
        )

        result = mistral_client.beta.conversations.get_history(
            conversation_id="conv-001",
        )

        assert result.conversation_id == "conv-001"
        assert result.object == "conversation.history"


# -------------------------------------------------------------------------
# 7. Get messages
# -------------------------------------------------------------------------


class TestGetMessages:
    def test_get_messages(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001/messages").mock(
            return_value=httpx.Response(200, json=CONVERSATION_MESSAGES)
        )

        result = mistral_client.beta.conversations.get_messages(
            conversation_id="conv-001",
        )

        assert result.conversation_id == "conv-001"
        assert result.object == "conversation.messages"


# -------------------------------------------------------------------------
# 8. Restart conversation
# -------------------------------------------------------------------------


class TestRestartConversation:
    def test_restart(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations/conv-001/restart").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = mistral_client.beta.conversations.restart(
            conversation_id="conv-001",
            from_entry_id="entry-001",
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 9. Start stream
# -------------------------------------------------------------------------


class TestStartStream:
    def test_start_stream(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.beta.conversations.start_stream(
            inputs=USER_INPUTS,
            model="mistral-small-latest",
        )

        # The stream object should be iterable
        assert stream is not None


# -------------------------------------------------------------------------
# 10. Append stream
# -------------------------------------------------------------------------


class TestAppendStream:
    def test_append_stream(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.beta.conversations.append_stream(
            conversation_id="conv-001",
            inputs=USER_INPUTS,
        )

        assert stream is not None


# -------------------------------------------------------------------------
# 11. Restart stream
# -------------------------------------------------------------------------


class TestRestartStream:
    def test_restart_stream(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations/conv-001/restart").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = mistral_client.beta.conversations.restart_stream(
            conversation_id="conv-001",
            from_entry_id="entry-001",
        )

        assert stream is not None


# -------------------------------------------------------------------------
# 12. Async start conversation
# -------------------------------------------------------------------------


class TestStartConversationAsync:
    @pytest.mark.asyncio
    async def test_start_async(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = await mistral_client.beta.conversations.start_async(
            inputs=USER_INPUTS,
            model="mistral-small-latest",
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 13. Async append to conversation
# -------------------------------------------------------------------------


class TestAppendConversationAsync:
    @pytest.mark.asyncio
    async def test_append_async(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = await mistral_client.beta.conversations.append_async(
            conversation_id="conv-001",
            inputs=USER_INPUTS,
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 14. Async get history
# -------------------------------------------------------------------------


class TestGetHistoryAsync:
    @pytest.mark.asyncio
    async def test_get_history_async(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001/history").mock(
            return_value=httpx.Response(200, json=CONVERSATION_HISTORY)
        )

        result = await mistral_client.beta.conversations.get_history_async(
            conversation_id="conv-001",
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 15. Async delete conversation
# -------------------------------------------------------------------------


class TestDeleteConversationAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        mock_router.delete("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(204)
        )

        result = await mistral_client.beta.conversations.delete_async(
            conversation_id="conv-001",
        )

        assert result is None


# -------------------------------------------------------------------------
# 16. Async restart conversation
# -------------------------------------------------------------------------


class TestRestartConversationAsync:
    @pytest.mark.asyncio
    async def test_restart_async(self, mock_router, mistral_client):
        mock_router.post("/v1/conversations/conv-001/restart").mock(
            return_value=httpx.Response(200, json=CONVERSATION_RESPONSE)
        )

        result = await mistral_client.beta.conversations.restart_async(
            conversation_id="conv-001",
            from_entry_id="entry-001",
        )

        assert result.conversation_id == "conv-001"


# -------------------------------------------------------------------------
# 17. Async get conversation
# -------------------------------------------------------------------------


class TestGetConversationAsync:
    @pytest.mark.asyncio
    async def test_get_async(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(200, json=MODEL_CONVERSATION)
        )

        result = await mistral_client.beta.conversations.get_async(conversation_id="conv-001")

        assert result.id == "conv-002"


# -------------------------------------------------------------------------
# 18. Async get messages
# -------------------------------------------------------------------------


class TestGetMessagesAsync:
    @pytest.mark.asyncio
    async def test_get_messages_async(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations/conv-001/messages").mock(
            return_value=httpx.Response(200, json=CONVERSATION_MESSAGES)
        )

        result = await mistral_client.beta.conversations.get_messages_async(
            conversation_id="conv-001",
        )

        assert result.conversation_id == "conv-001"
        assert result.object == "conversation.messages"


# -------------------------------------------------------------------------
# 19. Async start stream
# -------------------------------------------------------------------------


class TestStartStreamAsync:
    @pytest.mark.asyncio
    async def test_start_stream_async(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.beta.conversations.start_stream_async(
            inputs=USER_INPUTS,
            model="mistral-small-latest",
        )

        assert stream is not None


# -------------------------------------------------------------------------
# 20. Async append stream
# -------------------------------------------------------------------------


class TestAppendStreamAsync:
    @pytest.mark.asyncio
    async def test_append_stream_async(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations/conv-001").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.beta.conversations.append_stream_async(
            conversation_id="conv-001",
            inputs=USER_INPUTS,
        )

        assert stream is not None


# -------------------------------------------------------------------------
# 21. Async restart stream
# -------------------------------------------------------------------------


class TestRestartStreamAsync:
    @pytest.mark.asyncio
    async def test_restart_stream_async(self, mock_router, mistral_client):
        event = {
            "event": "response.started",
            "data": {
                "type": "response.started",
                "conversation_id": "conv-001",
            },
        }
        body = make_conversation_sse_body([event])
        mock_router.post("/v1/conversations/conv-001/restart").mock(
            return_value=httpx.Response(
                200,
                content=body,
                headers={"content-type": "text/event-stream"},
            )
        )

        stream = await mistral_client.beta.conversations.restart_stream_async(
            conversation_id="conv-001",
            from_entry_id="entry-001",
        )

        assert stream is not None


# -------------------------------------------------------------------------
# 22. Async list conversations
# -------------------------------------------------------------------------


class TestListConversationsAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        mock_router.get("/v1/conversations").mock(
            return_value=httpx.Response(200, json=[MODEL_CONVERSATION])
        )

        result = await mistral_client.beta.conversations.list_async()

        assert len(result) == 1
