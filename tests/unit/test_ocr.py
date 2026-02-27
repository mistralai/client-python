"""Tests for ocr.process() and ocr.process_async()."""

import json
from typing import Any

import httpx
import pytest


# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestProcessReturnsResponse:
    def test_process_returns_response(self, mock_router, mistral_client):
        mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        result = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
        )

        assert result is not None
        assert result.model == "mistral-ocr-latest"
        assert len(result.pages) == 1
        assert result.pages[0].index == 0
        assert result.pages[0].markdown == "# Hello World"


class TestProcessWithOptionalParams:
    def test_process_with_optional_params(self, mock_router, mistral_client):
        route = mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
            pages=[0, 1],
            include_image_base64=True,
            image_limit=5,
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["pages"] == [0, 1]
        assert body["include_image_base64"] is True
        assert body["image_limit"] == 5


class TestProcessAsync:
    @pytest.mark.asyncio
    async def test_process_async(self, mock_router, mistral_client):
        mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        result = await mistral_client.ocr.process_async(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
        )

        assert result is not None
        assert result.model == "mistral-ocr-latest"
        assert len(result.pages) == 1


class TestRequestBodyHasModelAndDocument:
    def test_request_body_has_model_and_document(self, mock_router, mistral_client):
        route = mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["model"] == "mistral-ocr-latest"
        assert body["document"]["type"] == "document_url"
        assert body["document"]["document_url"] == "https://example.com/doc.pdf"


class TestProcessResponsePagesContent:
    def test_process_response_pages_content(self, mock_router, mistral_client):
        mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        result = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
        )

        assert result.usage_info is not None
        assert result.usage_info.pages_processed == 1
        page = result.pages[0]
        assert hasattr(page, "images")
        assert hasattr(page, "dimensions")


class TestProcessAsyncWithOptionalParams:
    @pytest.mark.asyncio
    async def test_process_async_with_optional_params(self, mock_router, mistral_client):
        route = mock_router.post("/v1/ocr").mock(
            return_value=httpx.Response(200, json=OCR_RESPONSE)
        )

        await mistral_client.ocr.process_async(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://example.com/doc.pdf",
            },
            pages=[0, 1],
            include_image_base64=True,
        )

        assert route.called
        request = route.calls.last.request
        body = json.loads(request.content)
        assert body["pages"] == [0, 1]
        assert body["include_image_base64"] is True
