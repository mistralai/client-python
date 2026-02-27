"""Unit tests for the Libraries API (mistralai.client.libraries.Libraries)."""

import json

import httpx
import pytest


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

LIBRARY_RESPONSE = {
    "id": "lib-abc123",
    "name": "My Knowledge Base",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "owner_id": None,
    "owner_type": "user",
    "total_size": 0,
    "nb_documents": 0,
    "chunk_size": None,
    "description": "Test library",
}

LIST_LIBRARIES_RESPONSE = {
    "data": [LIBRARY_RESPONSE],
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestLibrariesCreate:
    def test_create_returns_library(self, mock_router, mistral_client):
        """libraries.create() returns a Library."""
        mock_router.post("/v1/libraries").mock(
            return_value=httpx.Response(201, json=LIBRARY_RESPONSE)
        )
        result = mistral_client.beta.libraries.create(
            name="My Knowledge Base",
            description="Test library",
        )
        assert result is not None
        assert result.id == "lib-abc123"
        assert result.name == "My Knowledge Base"
        # Verify request body
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["name"] == "My Knowledge Base"
        assert req_body["description"] == "Test library"


class TestLibrariesList:
    def test_list_returns_libraries(self, mock_router, mistral_client):
        """libraries.list() returns a ListLibrariesResponse."""
        mock_router.get("/v1/libraries").mock(
            return_value=httpx.Response(200, json=LIST_LIBRARIES_RESPONSE)
        )
        result = mistral_client.beta.libraries.list()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "lib-abc123"


class TestLibrariesGet:
    def test_get_returns_library(self, mock_router, mistral_client):
        """libraries.get(library_id=...) returns a Library."""
        mock_router.get(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=LIBRARY_RESPONSE)
        )
        result = mistral_client.beta.libraries.get(library_id="lib-abc123")
        assert result is not None
        assert result.id == "lib-abc123"


class TestLibrariesUpdate:
    def test_update_returns_library(self, mock_router, mistral_client):
        """libraries.update() sends PUT and returns a Library."""
        updated = {**LIBRARY_RESPONSE, "name": "Updated Name"}
        mock_router.put(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=updated)
        )
        result = mistral_client.beta.libraries.update(
            library_id="lib-abc123",
            name="Updated Name",
        )
        assert result is not None
        assert result.name == "Updated Name"
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["name"] == "Updated Name"


class TestLibrariesDelete:
    def test_delete_returns_response(self, mock_router, mistral_client):
        """libraries.delete(library_id=...) returns a Library."""
        mock_router.delete(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=LIBRARY_RESPONSE)
        )
        result = mistral_client.beta.libraries.delete(library_id="lib-abc123")
        assert result is not None
        assert result.id == "lib-abc123"


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestLibrariesCreateAsync:
    @pytest.mark.asyncio
    async def test_create_async(self, mock_router, mistral_client):
        """libraries.create_async() returns a Library."""
        mock_router.post("/v1/libraries").mock(
            return_value=httpx.Response(201, json=LIBRARY_RESPONSE)
        )
        result = await mistral_client.beta.libraries.create_async(
            name="My Knowledge Base",
        )
        assert result is not None
        assert result.id == "lib-abc123"


class TestLibrariesListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """libraries.list_async() returns a ListLibrariesResponse."""
        mock_router.get("/v1/libraries").mock(
            return_value=httpx.Response(200, json=LIST_LIBRARIES_RESPONSE)
        )
        result = await mistral_client.beta.libraries.list_async()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestLibrariesGetAsync:
    @pytest.mark.asyncio
    async def test_get_async(self, mock_router, mistral_client):
        """libraries.get_async(library_id=...) returns a Library."""
        mock_router.get(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=LIBRARY_RESPONSE)
        )
        result = await mistral_client.beta.libraries.get_async(library_id="lib-abc123")
        assert result is not None
        assert result.id == "lib-abc123"


class TestLibrariesUpdateAsync:
    @pytest.mark.asyncio
    async def test_update_async(self, mock_router, mistral_client):
        """libraries.update_async() sends PUT and returns a Library."""
        updated = {**LIBRARY_RESPONSE, "name": "Updated Name"}
        mock_router.put(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=updated)
        )
        result = await mistral_client.beta.libraries.update_async(
            library_id="lib-abc123",
            name="Updated Name",
        )
        assert result is not None
        assert result.name == "Updated Name"


class TestLibrariesDeleteAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        """libraries.delete_async(library_id=...) returns a Library."""
        mock_router.delete(url__regex=r"/v1/libraries/[^/]+$").mock(
            return_value=httpx.Response(200, json=LIBRARY_RESPONSE)
        )
        result = await mistral_client.beta.libraries.delete_async(library_id="lib-abc123")
        assert result is not None
        assert result.id == "lib-abc123"
