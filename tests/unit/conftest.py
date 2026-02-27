"""Shared fixtures and helpers for hand-written unit tests."""

import json
from typing import Any

import httpx
import pytest
import respx

from mistralai.client.sdk import Mistral


# ---------------------------------------------------------------------------
# Minimal valid response payloads
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

EMBEDDING_RESPONSE: dict[str, Any] = {
    "id": "emb-001",
    "object": "list",
    "model": "mistral-embed",
    "data": [
        {
            "object": "embedding",
            "index": 0,
            "embedding": [0.1, 0.2, 0.3],
        }
    ],
    "usage": {"prompt_tokens": 5, "total_tokens": 5},
}

VALIDATION_ERROR_RESPONSE: dict[str, Any] = {
    "detail": [
        {
            "loc": ["body", "model"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ],
}

CLASSIFICATION_RESPONSE: dict[str, Any] = {
    "id": "cls-001",
    "model": "mistral-moderation-latest",
    "results": [
        {
            "categories": {},
            "category_scores": {},
        }
    ],
}

CLASSIFY_RESPONSE: dict[str, Any] = {
    "id": "cls-002",
    "model": "mistral-moderation-latest",
    "results": [
        {
            "self_harm": {"scores": {"safe": 0.99, "unsafe": 0.01}},
        }
    ],
}

OCR_RESPONSE: dict[str, Any] = {
    "pages": [
        {
            "index": 0,
            "markdown": "# Hello World",
            "images": [],
            "dimensions": None,
        }
    ],
    "model": "mistral-ocr-latest",
    "usage_info": {"pages_processed": 1},
}

TRANSCRIPTION_RESPONSE: dict[str, Any] = {
    "model": "mistral-large-latest",
    "text": "Hello world.",
    "usage": {"prompt_tokens": 10, "completion_tokens": 0, "total_tokens": 10},
    "language": "en",
}


# ---------------------------------------------------------------------------
# SSE helpers
# ---------------------------------------------------------------------------

STREAM_CHUNK_TEMPLATE: dict[str, Any] = {
    "id": "stream-001",
    "object": "chat.completion.chunk",
    "model": "mistral-small-latest",
    "created": 1700000000,
}


def make_stream_chunk(
    content: str = "",
    finish_reason: str | None = None,
    index: int = 0,
) -> dict[str, Any]:
    """Build a single streaming chunk."""
    delta: dict[str, Any] = {"role": "assistant"}
    if content:
        delta["content"] = content
    choice: dict[str, Any] = {"index": index, "delta": delta, "finish_reason": finish_reason}
    return {**STREAM_CHUNK_TEMPLATE, "choices": [choice]}


def make_sse_body(
    events: list[dict[str, Any]],
    sentinel: str = "[DONE]",
) -> bytes:
    """Build text/event-stream body from event dicts."""
    lines = [f"data: {json.dumps(e)}\n\n" for e in events]
    lines.append(f"data: {sentinel}\n\n")
    return "".join(lines).encode()


def make_completion_event(data: dict[str, Any]) -> dict[str, Any]:
    """Wrap a chunk dict in a CompletionEvent-compatible dict."""
    return {"data": data}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_router():
    """Provide a respx mock router scoped to https://test.api."""
    with respx.mock(base_url="https://test.api") as router:
        yield router


@pytest.fixture()
def mistral_client(mock_router):
    """Provide a Mistral client pointed at the mock router."""
    return Mistral(api_key="test-key", server_url="https://test.api")


def user_msg(content: str = "Hello") -> list[dict[str, str]]:
    """Convenience: build a single user message list."""
    return [{"role": "user", "content": content}]
