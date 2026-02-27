"""Unit tests for the Documents API (mistralai.client.documents.Documents)."""

import json

import httpx
import pytest


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

DOCUMENT_RESPONSE = {
    "id": "doc-abc123",
    "library_id": "lib-abc123",
    "hash": None,
    "mime_type": "application/pdf",
    "extension": ".pdf",
    "size": 4096,
    "name": "test-document.pdf",
    "created_at": "2024-01-01T00:00:00Z",
    "process_status": "done",
    "uploaded_by_id": None,
    "uploaded_by_type": "user",
    "processing_status": "processed",
    "tokens_processing_total": 100,
}

PAGINATION_INFO = {
    "total_items": 1,
    "total_pages": 1,
    "current_page": 0,
    "page_size": 50,
    "has_more": False,
}

LIST_DOCUMENTS_RESPONSE = {
    "pagination": PAGINATION_INFO,
    "data": [DOCUMENT_RESPONSE],
}

DOCUMENT_TEXT_CONTENT_RESPONSE = {
    "text": "This is the extracted text content of the document.",
}

PROCESSING_STATUS_RESPONSE = {
    "document_id": "doc-abc123",
    "process_status": "done",
    "processing_status": "processed",
}

LIB_ID = "lib-abc123"
DOC_ID = "doc-abc123"


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestDocumentsList:
    def test_list_returns_documents(self, mock_router, mistral_client):
        """documents.list() returns a ListDocumentsResponse."""
        mock_router.get(url__regex=r"/v1/libraries/.*/documents").mock(
            return_value=httpx.Response(200, json=LIST_DOCUMENTS_RESPONSE)
        )
        result = mistral_client.beta.libraries.documents.list(library_id=LIB_ID)
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "doc-abc123"


class TestDocumentsUpload:
    def test_upload_returns_document(self, mock_router, mistral_client):
        """documents.upload() returns a Document."""
        mock_router.post(url__regex=r"/v1/libraries/.*/documents").mock(
            return_value=httpx.Response(200, json=DOCUMENT_RESPONSE)
        )
        result = mistral_client.beta.libraries.documents.upload(
            library_id=LIB_ID,
            file={"file_name": "test.pdf", "content": b"pdf-content"},
        )
        assert result is not None
        assert result.id == "doc-abc123"


class TestDocumentsGet:
    def test_get_returns_document(self, mock_router, mistral_client):
        """documents.get() returns a Document."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/[^/]+$"
        ).mock(
            return_value=httpx.Response(200, json=DOCUMENT_RESPONSE)
        )
        result = mistral_client.beta.libraries.documents.get(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.id == "doc-abc123"


class TestDocumentsUpdate:
    def test_update_sends_put(self, mock_router, mistral_client):
        """documents.update() sends PUT with name."""
        updated = {**DOCUMENT_RESPONSE, "name": "renamed.pdf"}
        mock_router.put(
            url__regex=r"/v1/libraries/.*/documents/[^/]+$"
        ).mock(
            return_value=httpx.Response(200, json=updated)
        )
        result = mistral_client.beta.libraries.documents.update(
            library_id=LIB_ID,
            document_id=DOC_ID,
            name="renamed.pdf",
        )
        assert result is not None
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["name"] == "renamed.pdf"


class TestDocumentsDelete:
    def test_delete_returns_none(self, mock_router, mistral_client):
        """documents.delete() returns None (204 No Content)."""
        mock_router.delete(
            url__regex=r"/v1/libraries/.*/documents/[^/]+$"
        ).mock(
            return_value=httpx.Response(204)
        )
        result = mistral_client.beta.libraries.documents.delete(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is None


class TestDocumentsTextContent:
    def test_text_content_returns_text(self, mock_router, mistral_client):
        """documents.text_content() returns DocumentTextContent."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/text_content"
        ).mock(
            return_value=httpx.Response(200, json=DOCUMENT_TEXT_CONTENT_RESPONSE)
        )
        result = mistral_client.beta.libraries.documents.text_content(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.text == "This is the extracted text content of the document."


class TestDocumentsStatus:
    def test_status_returns_status(self, mock_router, mistral_client):
        """documents.status() returns ProcessingStatusOut."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/status"
        ).mock(
            return_value=httpx.Response(200, json=PROCESSING_STATUS_RESPONSE)
        )
        result = mistral_client.beta.libraries.documents.status(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.document_id == "doc-abc123"
        assert result.process_status == "done"


class TestDocumentsGetSignedUrl:
    def test_get_signed_url(self, mock_router, mistral_client):
        """documents.get_signed_url() returns a string URL."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/signed-url"
        ).mock(
            return_value=httpx.Response(
                200,
                json="https://storage.example.com/signed/doc-abc123",
            )
        )
        result = mistral_client.beta.libraries.documents.get_signed_url(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result == "https://storage.example.com/signed/doc-abc123"


class TestDocumentsExtractedTextSignedUrl:
    def test_extracted_text_signed_url(self, mock_router, mistral_client):
        """documents.extracted_text_signed_url() returns a string URL."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/extracted-text-signed-url"
        ).mock(
            return_value=httpx.Response(
                200,
                json="https://storage.example.com/extracted/doc-abc123",
            )
        )
        result = mistral_client.beta.libraries.documents.extracted_text_signed_url(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result == "https://storage.example.com/extracted/doc-abc123"


class TestDocumentsReprocess:
    def test_reprocess(self, mock_router, mistral_client):
        """documents.reprocess() returns None (204 No Content)."""
        mock_router.post(
            url__regex=r"/v1/libraries/.*/documents/.*/reprocess"
        ).mock(
            return_value=httpx.Response(204)
        )
        result = mistral_client.beta.libraries.documents.reprocess(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is None


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestDocumentsListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """documents.list_async() returns a ListDocumentsResponse."""
        mock_router.get(url__regex=r"/v1/libraries/.*/documents").mock(
            return_value=httpx.Response(200, json=LIST_DOCUMENTS_RESPONSE)
        )
        result = await mistral_client.beta.libraries.documents.list_async(
            library_id=LIB_ID
        )
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestDocumentsUploadAsync:
    @pytest.mark.asyncio
    async def test_upload_async(self, mock_router, mistral_client):
        """documents.upload_async() returns a Document."""
        mock_router.post(url__regex=r"/v1/libraries/.*/documents").mock(
            return_value=httpx.Response(200, json=DOCUMENT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.documents.upload_async(
            library_id=LIB_ID,
            file={"file_name": "test.pdf", "content": b"pdf-content"},
        )
        assert result is not None
        assert result.id == "doc-abc123"


class TestDocumentsGetAsync:
    @pytest.mark.asyncio
    async def test_get_async(self, mock_router, mistral_client):
        """documents.get_async() returns a Document."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/[^/]+$"
        ).mock(
            return_value=httpx.Response(200, json=DOCUMENT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.documents.get_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.id == "doc-abc123"


class TestDocumentsDeleteAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        """documents.delete_async() returns None (204 No Content)."""
        mock_router.delete(
            url__regex=r"/v1/libraries/.*/documents/[^/]+$"
        ).mock(
            return_value=httpx.Response(204)
        )
        result = await mistral_client.beta.libraries.documents.delete_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is None


class TestDocumentsTextContentAsync:
    @pytest.mark.asyncio
    async def test_text_content_async(self, mock_router, mistral_client):
        """documents.text_content_async() returns DocumentTextContent."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/text_content"
        ).mock(
            return_value=httpx.Response(200, json=DOCUMENT_TEXT_CONTENT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.documents.text_content_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.text == "This is the extracted text content of the document."


class TestDocumentsStatusAsync:
    @pytest.mark.asyncio
    async def test_status_async(self, mock_router, mistral_client):
        """documents.status_async() returns ProcessingStatusOut."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/status"
        ).mock(
            return_value=httpx.Response(200, json=PROCESSING_STATUS_RESPONSE)
        )
        result = await mistral_client.beta.libraries.documents.status_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is not None
        assert result.document_id == "doc-abc123"


class TestDocumentsGetSignedUrlAsync:
    @pytest.mark.asyncio
    async def test_get_signed_url_async(self, mock_router, mistral_client):
        """documents.get_signed_url_async() returns a string URL."""
        mock_router.get(
            url__regex=r"/v1/libraries/.*/documents/.*/signed-url"
        ).mock(
            return_value=httpx.Response(
                200,
                json="https://storage.example.com/signed/doc-abc123",
            )
        )
        result = await mistral_client.beta.libraries.documents.get_signed_url_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result == "https://storage.example.com/signed/doc-abc123"


class TestDocumentsReprocessAsync:
    @pytest.mark.asyncio
    async def test_reprocess_async(self, mock_router, mistral_client):
        """documents.reprocess_async() returns None (204 No Content)."""
        mock_router.post(
            url__regex=r"/v1/libraries/.*/documents/.*/reprocess"
        ).mock(
            return_value=httpx.Response(204)
        )
        result = await mistral_client.beta.libraries.documents.reprocess_async(
            library_id=LIB_ID, document_id=DOC_ID
        )
        assert result is None
