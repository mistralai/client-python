"""Tests for embeddings.create() and embeddings.create_async()."""

import json
from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCreateReturnsEmbeddingResponse:
    def test_create_returns_embedding_response(self, mock_router, mistral_client):
        mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        result = mistral_client.embeddings.create(
            model="mistral-embed", inputs="Hello"
        )

        assert result is not None
        assert result.id == "emb-001"
        assert result.model == "mistral-embed"
        assert len(result.data) == 1
        assert result.data[0].embedding == [0.1, 0.2, 0.3]


class TestRequestBodyHasModelAndInputs:
    def test_request_body_has_model_and_inputs(self, mock_router, mistral_client):
        route = mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        mistral_client.embeddings.create(model="mistral-embed", inputs="Hello")

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["model"] == "mistral-embed"
        # The SDK may serialize as "input" (alias) or "inputs"
        assert "input" in body or "inputs" in body


class TestMultipleInputs:
    def test_multiple_inputs(self, mock_router, mistral_client):
        route = mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        mistral_client.embeddings.create(
            model="mistral-embed", inputs=["Hello", "World"]
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        # The SDK serializes the inputs; verify the list was sent
        sent_inputs = body.get("input", body.get("inputs"))
        assert isinstance(sent_inputs, list)
        assert len(sent_inputs) == 2


class TestOutputDimensionParam:
    def test_output_dimension_param(self, mock_router, mistral_client):
        route = mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        mistral_client.embeddings.create(
            model="mistral-embed", inputs="Hello", output_dimension=256
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["output_dimension"] == 256


class TestOutputDtypeParam:
    def test_output_dtype_param(self, mock_router, mistral_client):
        route = mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        mistral_client.embeddings.create(
            model="mistral-embed", inputs="Hello", output_dtype="float"
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["output_dtype"] == "float"


class TestCreateAsync:
    @pytest.mark.asyncio
    async def test_create_async(self, mock_router, mistral_client):
        mock_router.post("/v1/embeddings").mock(
            return_value=httpx.Response(200, json=EMBEDDING_RESPONSE)
        )

        result = await mistral_client.embeddings.create_async(
            model="mistral-embed", inputs="Hello"
        )

        assert result is not None
        assert result.id == "emb-001"
        assert len(result.data) == 1
