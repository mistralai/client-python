"""Unit tests for the Accesses API (mistralai.client.accesses.Accesses)."""

import json

import httpx
import pytest


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

SHARING_OUT_RESPONSE = {
    "library_id": "lib-abc123",
    "org_id": "org-abc123",
    "role": "Viewer",
    "share_with_type": "User",
    "share_with_uuid": "user-uuid-123",
}

LIST_SHARING_OUT_RESPONSE = {
    "data": [SHARING_OUT_RESPONSE],
}

LIB_ID = "lib-abc123"


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestAccessesList:
    def test_list_returns_accesses(self, mock_router, mistral_client):
        """accesses.list() returns a ListSharingOut."""
        mock_router.get(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=LIST_SHARING_OUT_RESPONSE)
        )
        result = mistral_client.beta.libraries.accesses.list(library_id=LIB_ID)
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].library_id == "lib-abc123"


class TestAccessesUpdateOrCreate:
    def test_update_or_create_returns_access(self, mock_router, mistral_client):
        """accesses.update_or_create() sends PUT and returns SharingOut."""
        mock_router.put(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=SHARING_OUT_RESPONSE)
        )
        result = mistral_client.beta.libraries.accesses.update_or_create(
            library_id=LIB_ID,
            level="Viewer",
            share_with_uuid="user-uuid-123",
            share_with_type="User",
        )
        assert result is not None
        assert result.role == "Viewer"
        # Verify the request body
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["share_with_uuid"] == "user-uuid-123"
        assert req_body["level"] == "Viewer"
        assert req_body["share_with_type"] == "User"


class TestAccessesDelete:
    def test_delete_returns_response(self, mock_router, mistral_client):
        """accesses.delete() sends DELETE with body and returns SharingOut."""
        mock_router.delete(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=SHARING_OUT_RESPONSE)
        )
        result = mistral_client.beta.libraries.accesses.delete(
            library_id=LIB_ID,
            share_with_uuid="user-uuid-123",
            share_with_type="User",
        )
        assert result is not None
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["share_with_uuid"] == "user-uuid-123"
        assert req_body["share_with_type"] == "User"


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAccessesListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """accesses.list_async() returns a ListSharingOut."""
        mock_router.get(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=LIST_SHARING_OUT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.accesses.list_async(
            library_id=LIB_ID
        )
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestAccessesUpdateOrCreateAsync:
    @pytest.mark.asyncio
    async def test_update_or_create_async(self, mock_router, mistral_client):
        """accesses.update_or_create_async() sends PUT and returns SharingOut."""
        mock_router.put(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=SHARING_OUT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.accesses.update_or_create_async(
            library_id=LIB_ID,
            level="Viewer",
            share_with_uuid="user-uuid-123",
            share_with_type="User",
        )
        assert result is not None


class TestAccessesDeleteAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        """accesses.delete_async() sends DELETE with body and returns SharingOut."""
        mock_router.delete(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=SHARING_OUT_RESPONSE)
        )
        result = await mistral_client.beta.libraries.accesses.delete_async(
            library_id=LIB_ID,
            share_with_uuid="user-uuid-123",
            share_with_type="User",
        )
        assert result is not None


class TestAccessesListWithLibraryId:
    def test_list_sends_library_id_in_path(self, mock_router, mistral_client):
        """accesses.list() includes library_id in the URL path."""
        route = mock_router.get(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=LIST_SHARING_OUT_RESPONSE)
        )
        mistral_client.beta.libraries.accesses.list(library_id=LIB_ID)
        assert route.called
        request_url = str(route.calls.last.request.url)
        assert "lib-abc123" in request_url


class TestAccessesUpdateOrCreateRequestBody:
    def test_update_or_create_request_body(self, mock_router, mistral_client):
        """accesses.update_or_create() sends level, share_with_uuid, share_with_type."""
        mock_router.put(url__regex=r"/v1/libraries/.*/share").mock(
            return_value=httpx.Response(200, json=SHARING_OUT_RESPONSE)
        )
        mistral_client.beta.libraries.accesses.update_or_create(
            library_id=LIB_ID,
            level="Editor",
            share_with_uuid="user-uuid-456",
            share_with_type="Organization",
        )
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["level"] == "Editor"
        assert req_body["share_with_uuid"] == "user-uuid-456"
        assert req_body["share_with_type"] == "Organization"
