"""Tests for classifiers.moderate(), moderate_chat(), classify(), classify_chat() and async variants."""

from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

# Response for moderate / moderate_chat (ModerationResponse)
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

# Response for classify / classify_chat (ClassificationResponse)
CLASSIFY_RESPONSE: dict[str, Any] = {
    "id": "cls-002",
    "model": "mistral-moderation-latest",
    "results": [
        {
            "self_harm": {"scores": {"safe": 0.99, "unsafe": 0.01}},
        }
    ],
}


def _chat_input():
    """Build a single-conversation input suitable for moderate_chat / classify_chat."""
    return [{"role": "user", "content": "test text"}]


# ---------------------------------------------------------------------------
# moderate
# ---------------------------------------------------------------------------


class TestModerateReturnsResponse:
    def test_moderate_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/moderations").mock(
            return_value=httpx.Response(200, json=CLASSIFICATION_RESPONSE)
        )

        result = mistral_client.classifiers.moderate(
            model="mistral-moderation-latest", inputs=["test text"]
        )

        assert result is not None
        assert result.id == "cls-001"
        assert result.model == "mistral-moderation-latest"
        assert len(result.results) == 1


# ---------------------------------------------------------------------------
# moderate_chat
# ---------------------------------------------------------------------------


class TestModerateChatReturnsResponse:
    def test_moderate_chat_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/moderations").mock(
            return_value=httpx.Response(200, json=CLASSIFICATION_RESPONSE)
        )

        result = mistral_client.classifiers.moderate_chat(
            model="mistral-moderation-latest", inputs=_chat_input()
        )

        assert result is not None
        assert result.id == "cls-001"


# ---------------------------------------------------------------------------
# classify
# ---------------------------------------------------------------------------


class TestClassifyReturnsResponse:
    def test_classify_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/classifications").mock(
            return_value=httpx.Response(200, json=CLASSIFY_RESPONSE)
        )

        result = mistral_client.classifiers.classify(
            model="mistral-moderation-latest", inputs=["test text"]
        )

        assert result is not None
        assert result.id == "cls-002"
        assert result.model == "mistral-moderation-latest"
        assert len(result.results) == 1


# ---------------------------------------------------------------------------
# classify_chat
# ---------------------------------------------------------------------------


class TestClassifyChatReturnsResponse:
    def test_classify_chat_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/classifications").mock(
            return_value=httpx.Response(200, json=CLASSIFY_RESPONSE)
        )

        # classify_chat uses `input` parameter (singular), not `inputs`
        result = mistral_client.classifiers.classify_chat(
            model="mistral-moderation-latest",
            input={"messages": _chat_input()},
        )

        assert result is not None
        assert result.id == "cls-002"


# ---------------------------------------------------------------------------
# Async variants
# ---------------------------------------------------------------------------


class TestModerateAsync:
    @pytest.mark.asyncio
    async def test_moderate_async(self, mock_router, mistral_client):
        mock_router.post("/v1/moderations").mock(
            return_value=httpx.Response(200, json=CLASSIFICATION_RESPONSE)
        )

        result = await mistral_client.classifiers.moderate_async(
            model="mistral-moderation-latest", inputs=["test text"]
        )

        assert result is not None
        assert result.id == "cls-001"


class TestModerateChatAsync:
    @pytest.mark.asyncio
    async def test_moderate_chat_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/moderations").mock(
            return_value=httpx.Response(200, json=CLASSIFICATION_RESPONSE)
        )

        result = await mistral_client.classifiers.moderate_chat_async(
            model="mistral-moderation-latest", inputs=_chat_input()
        )

        assert result is not None
        assert result.id == "cls-001"


class TestClassifyAsync:
    @pytest.mark.asyncio
    async def test_classify_async(self, mock_router, mistral_client):
        mock_router.post("/v1/classifications").mock(
            return_value=httpx.Response(200, json=CLASSIFY_RESPONSE)
        )

        result = await mistral_client.classifiers.classify_async(
            model="mistral-moderation-latest", inputs=["test text"]
        )

        assert result is not None
        assert result.id == "cls-002"


class TestClassifyChatAsync:
    @pytest.mark.asyncio
    async def test_classify_chat_async(self, mock_router, mistral_client):
        mock_router.post("/v1/chat/classifications").mock(
            return_value=httpx.Response(200, json=CLASSIFY_RESPONSE)
        )

        result = await mistral_client.classifiers.classify_chat_async(
            model="mistral-moderation-latest",
            input={"messages": _chat_input()},
        )

        assert result is not None
        assert result.id == "cls-002"


# ---------------------------------------------------------------------------
# Request body verification
# ---------------------------------------------------------------------------


class TestModerateRequestBodyHasModel:
    def test_moderate_request_body_has_model(self, mock_router, mistral_client):
        """moderate() sends 'model' in the request body."""
        import json

        route = mock_router.post("/v1/moderations").mock(
            return_value=httpx.Response(200, json=CLASSIFICATION_RESPONSE)
        )
        mistral_client.classifiers.moderate(
            model="mistral-moderation-latest", inputs=["text one", "text two"]
        )
        assert route.called
        req_body = json.loads(route.calls.last.request.content)
        assert req_body["model"] == "mistral-moderation-latest"
        # Verify input data is present in the body (SDK may serialize as 'input' or 'inputs')
        assert "input" in req_body or "inputs" in req_body


class TestClassifyError422:
    def test_classify_error_422(self, mock_router, mistral_client):
        """classifiers.classify() raises HTTPValidationError on 422."""
        from mistralai.client.errors.httpvalidationerror import HTTPValidationError

        mock_router.post("/v1/classifications").mock(
            return_value=httpx.Response(
                422,
                json={"detail": [{"loc": ["body"], "msg": "error", "type": "value_error"}]},
            )
        )
        with pytest.raises(HTTPValidationError):
            mistral_client.classifiers.classify(
                model="mistral-moderation-latest", inputs=["test"]
            )
