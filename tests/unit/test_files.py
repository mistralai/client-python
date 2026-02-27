"""Unit tests for the Files API (mistralai.client.files.Files)."""

import httpx
import pytest

from mistralai.client import models
from mistralai.client.errors.sdkerror import SDKError


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

FILE_SCHEMA = {
    "id": "file-abc123",
    "object": "file",
    "bytes": 1024,
    "created_at": 1700000000,
    "filename": "data.jsonl",
    "purpose": "fine-tune",
    "sample_type": "instruct",
    "source": "upload",
}

CREATE_FILE_RESPONSE = {
    **FILE_SCHEMA,
}

LIST_FILES_RESPONSE = {
    "data": [FILE_SCHEMA],
    "object": "list",
    "total": 1,
}

GET_FILE_RESPONSE = {
    **FILE_SCHEMA,
    "deleted": False,
}

DELETE_FILE_RESPONSE = {
    "id": "file-abc123",
    "object": "file",
    "deleted": True,
}

SIGNED_URL_RESPONSE = {
    "url": "https://storage.example.com/signed/file-abc123",
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestFilesUpload:
    def test_upload_returns_response(self, mock_router, mistral_client):
        """files.upload() with file content returns a CreateFileResponse."""
        mock_router.post("/v1/files").mock(
            return_value=httpx.Response(200, json=CREATE_FILE_RESPONSE)
        )
        result = mistral_client.files.upload(
            file={"file_name": "data.jsonl", "content": b"test content"},
        )
        assert result is not None
        assert result.id == "file-abc123"

    def test_upload_includes_purpose(self, mock_router, mistral_client):
        """files.upload() sends purpose field when provided."""
        mock_router.post("/v1/files").mock(
            return_value=httpx.Response(200, json=CREATE_FILE_RESPONSE)
        )
        result = mistral_client.files.upload(
            file={"file_name": "data.jsonl", "content": b"test content"},
            purpose="fine-tune",
        )
        assert result is not None
        assert result.id == "file-abc123"


class TestFilesList:
    def test_list_returns_list(self, mock_router, mistral_client):
        """files.list() returns a ListFilesResponse."""
        mock_router.get("/v1/files").mock(
            return_value=httpx.Response(200, json=LIST_FILES_RESPONSE)
        )
        result = mistral_client.files.list()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "file-abc123"


class TestFilesRetrieve:
    def test_retrieve_returns_file(self, mock_router, mistral_client):
        """files.retrieve(file_id=...) returns a GetFileResponse."""
        mock_router.get(url__regex=r"/v1/files/[^/]+$").mock(
            return_value=httpx.Response(200, json=GET_FILE_RESPONSE)
        )
        result = mistral_client.files.retrieve(file_id="file-abc123")
        assert result is not None
        assert result.id == "file-abc123"
        assert result.deleted is False


class TestFilesDelete:
    def test_delete_returns_response(self, mock_router, mistral_client):
        """files.delete(file_id=...) returns a DeleteFileResponse."""
        mock_router.delete(url__regex=r"/v1/files/.*").mock(
            return_value=httpx.Response(200, json=DELETE_FILE_RESPONSE)
        )
        result = mistral_client.files.delete(file_id="file-abc123")
        assert result is not None
        assert result.id == "file-abc123"
        assert result.deleted is True


class TestFilesDownload:
    def test_download_returns_response(self, mock_router, mistral_client):
        """files.download(file_id=...) returns an httpx.Response with file bytes."""
        mock_router.get(url__regex=r"/v1/files/.*/content").mock(
            return_value=httpx.Response(
                200,
                content=b"file-content-bytes",
                headers={"content-type": "application/octet-stream"},
            )
        )
        result = mistral_client.files.download(file_id="file-abc123")
        assert isinstance(result, httpx.Response)
        assert result.status_code == 200


class TestFilesGetSignedUrl:
    def test_get_signed_url_returns_url(self, mock_router, mistral_client):
        """files.get_signed_url(file_id=...) returns a GetSignedURLResponse."""
        mock_router.get(url__regex=r"/v1/files/.*/url").mock(
            return_value=httpx.Response(200, json=SIGNED_URL_RESPONSE)
        )
        result = mistral_client.files.get_signed_url(file_id="file-abc123")
        assert result is not None
        assert result.url == "https://storage.example.com/signed/file-abc123"


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestFilesUploadAsync:
    @pytest.mark.asyncio
    async def test_upload_async(self, mock_router, mistral_client):
        """files.upload_async() returns a CreateFileResponse."""
        mock_router.post("/v1/files").mock(
            return_value=httpx.Response(200, json=CREATE_FILE_RESPONSE)
        )
        result = await mistral_client.files.upload_async(
            file={"file_name": "data.jsonl", "content": b"test content"},
        )
        assert result is not None
        assert result.id == "file-abc123"


class TestFilesListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """files.list_async() returns a ListFilesResponse."""
        mock_router.get("/v1/files").mock(
            return_value=httpx.Response(200, json=LIST_FILES_RESPONSE)
        )
        result = await mistral_client.files.list_async()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestFilesRetrieveAsync:
    @pytest.mark.asyncio
    async def test_retrieve_async(self, mock_router, mistral_client):
        """files.retrieve_async(file_id=...) returns a GetFileResponse."""
        mock_router.get(url__regex=r"/v1/files/[^/]+$").mock(
            return_value=httpx.Response(200, json=GET_FILE_RESPONSE)
        )
        result = await mistral_client.files.retrieve_async(file_id="file-abc123")
        assert result is not None
        assert result.id == "file-abc123"


class TestFilesDeleteAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        """files.delete_async(file_id=...) returns a DeleteFileResponse."""
        mock_router.delete(url__regex=r"/v1/files/.*").mock(
            return_value=httpx.Response(200, json=DELETE_FILE_RESPONSE)
        )
        result = await mistral_client.files.delete_async(file_id="file-abc123")
        assert result is not None
        assert result.id == "file-abc123"
        assert result.deleted is True


class TestFilesDownloadAsync:
    @pytest.mark.asyncio
    async def test_download_async(self, mock_router, mistral_client):
        """files.download_async(file_id=...) returns an httpx.Response."""
        mock_router.get(url__regex=r"/v1/files/.*/content").mock(
            return_value=httpx.Response(
                200,
                content=b"file-content-bytes",
                headers={"content-type": "application/octet-stream"},
            )
        )
        result = await mistral_client.files.download_async(file_id="file-abc123")
        assert isinstance(result, httpx.Response)
        assert result.status_code == 200


# ---------------------------------------------------------------------------
# Error tests
# ---------------------------------------------------------------------------


class TestFilesRetrieveNotFound:
    def test_retrieve_not_found(self, mock_router, mistral_client):
        """files.retrieve() raises SDKError on 404."""
        mock_router.get(url__regex=r"/v1/files/[^/]+$").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.files.retrieve(file_id="file-nonexistent")


class TestFilesDeleteNotFound:
    def test_delete_not_found(self, mock_router, mistral_client):
        """files.delete() raises SDKError on 404."""
        mock_router.delete(url__regex=r"/v1/files/.*").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.files.delete(file_id="file-nonexistent")


class TestFilesDownloadNotFound:
    def test_download_not_found(self, mock_router, mistral_client):
        """files.download() raises SDKError on 404."""
        mock_router.get(url__regex=r"/v1/files/.*/content").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.files.download(file_id="file-nonexistent")


class TestFilesGetSignedUrlAsync:
    @pytest.mark.asyncio
    async def test_get_signed_url_async(self, mock_router, mistral_client):
        """files.get_signed_url_async(file_id=...) returns a GetSignedURLResponse."""
        mock_router.get(url__regex=r"/v1/files/.*/url").mock(
            return_value=httpx.Response(200, json=SIGNED_URL_RESPONSE)
        )
        result = await mistral_client.files.get_signed_url_async(file_id="file-abc123")
        assert result is not None
        assert result.url == "https://storage.example.com/signed/file-abc123"


class TestFilesGetSignedUrlNotFound:
    def test_get_signed_url_not_found(self, mock_router, mistral_client):
        """files.get_signed_url() raises SDKError on 404."""
        mock_router.get(url__regex=r"/v1/files/.*/url").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.files.get_signed_url(file_id="file-nonexistent")
