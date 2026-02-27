"""Unit tests for the Models API (mistralai.client.models_.Models)."""

import json

import httpx
import pytest

from mistralai.client.errors.sdkerror import SDKError


# ---------------------------------------------------------------------------
# Mock response payloads
# ---------------------------------------------------------------------------

MODEL_DATA = {
    "id": "mistral-small-latest",
    "object": "model",
    "created": 1700000000,
    "owned_by": "mistralai",
    "type": "base",
    "capabilities": {
        "completion_chat": True,
        "function_calling": True,
    },
}

MODEL_LIST_RESPONSE = {
    "object": "list",
    "data": [MODEL_DATA],
}

DELETE_MODEL_RESPONSE = {
    "id": "ft:mistral-small:my-model:abc123",
    "object": "model",
    "deleted": True,
}

FT_MODEL_RESPONSE = {
    "id": "ft:mistral-small:my-model:abc123",
    "object": "model",
    "created": 1700000000,
    "owned_by": "user",
    "workspace_id": "ws-abc123",
    "root": "mistral-small-latest",
    "root_version": "1",
    "archived": False,
    "capabilities": {
        "completion_chat": True,
    },
    "job": "ftjob-abc123",
    "model_type": "completion",
}

ARCHIVE_MODEL_RESPONSE = {
    "id": "ft:mistral-small:my-model:abc123",
    "object": "model",
    "archived": True,
}

UNARCHIVE_MODEL_RESPONSE = {
    "id": "ft:mistral-small:my-model:abc123",
    "object": "model",
    "archived": False,
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestModelsList:
    def test_list_returns_models(self, mock_router, mistral_client):
        """models.list() returns a ModelList."""
        mock_router.get("/v1/models").mock(
            return_value=httpx.Response(200, json=MODEL_LIST_RESPONSE)
        )
        result = mistral_client.models.list()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0].id == "mistral-small-latest"


class TestModelsRetrieve:
    def test_retrieve_returns_model(self, mock_router, mistral_client):
        """models.retrieve(model_id=...) returns model details."""
        mock_router.get(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(200, json=MODEL_DATA)
        )
        result = mistral_client.models.retrieve(model_id="mistral-small-latest")
        assert result is not None
        assert result.id == "mistral-small-latest"


class TestModelsDelete:
    def test_delete_returns_response(self, mock_router, mistral_client):
        """models.delete(model_id=...) returns a DeleteModelOut."""
        mock_router.delete(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(200, json=DELETE_MODEL_RESPONSE)
        )
        result = mistral_client.models.delete(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.id == "ft:mistral-small:my-model:abc123"
        assert result.deleted is True


class TestModelsUpdate:
    def test_update_sends_patch(self, mock_router, mistral_client):
        """models.update(model_id=..., name=...) sends PATCH to fine_tuning/models."""
        route = mock_router.patch(url__regex=r"/v1/fine_tuning/models/.*").mock(
            return_value=httpx.Response(200, json=FT_MODEL_RESPONSE)
        )
        result = mistral_client.models.update(
            model_id="ft:mistral-small:my-model:abc123",
            name="renamed-model",
            description="updated description",
        )
        assert result is not None
        # Verify PATCH was called
        assert route.called
        # Verify the request body contains name and description
        req_body = json.loads(mock_router.calls.last.request.content)
        assert req_body["name"] == "renamed-model"
        assert req_body["description"] == "updated description"


class TestModelsArchive:
    def test_archive_returns_response(self, mock_router, mistral_client):
        """models.archive(model_id=...) sends POST to archive endpoint."""
        mock_router.post(url__regex=r"/v1/fine_tuning/models/.*/archive").mock(
            return_value=httpx.Response(200, json=ARCHIVE_MODEL_RESPONSE)
        )
        result = mistral_client.models.archive(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.archived is True


class TestModelsUnarchive:
    def test_unarchive_returns_response(self, mock_router, mistral_client):
        """models.unarchive(model_id=...) sends DELETE to archive endpoint."""
        mock_router.delete(url__regex=r"/v1/fine_tuning/models/.*/archive").mock(
            return_value=httpx.Response(200, json=UNARCHIVE_MODEL_RESPONSE)
        )
        result = mistral_client.models.unarchive(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.archived is False


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestModelsListAsync:
    @pytest.mark.asyncio
    async def test_list_async(self, mock_router, mistral_client):
        """models.list_async() returns a ModelList."""
        mock_router.get("/v1/models").mock(
            return_value=httpx.Response(200, json=MODEL_LIST_RESPONSE)
        )
        result = await mistral_client.models.list_async()
        assert result is not None
        assert result.data is not None
        assert len(result.data) == 1


class TestModelsRetrieveAsync:
    @pytest.mark.asyncio
    async def test_retrieve_async(self, mock_router, mistral_client):
        """models.retrieve_async(model_id=...) returns model details."""
        mock_router.get(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(200, json=MODEL_DATA)
        )
        result = await mistral_client.models.retrieve_async(
            model_id="mistral-small-latest"
        )
        assert result is not None
        assert result.id == "mistral-small-latest"


class TestModelsDeleteAsync:
    @pytest.mark.asyncio
    async def test_delete_async(self, mock_router, mistral_client):
        """models.delete_async(model_id=...) returns a DeleteModelOut."""
        mock_router.delete(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(200, json=DELETE_MODEL_RESPONSE)
        )
        result = await mistral_client.models.delete_async(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.id == "ft:mistral-small:my-model:abc123"
        assert result.deleted is True


class TestModelsUpdateAsync:
    @pytest.mark.asyncio
    async def test_update_async(self, mock_router, mistral_client):
        """models.update_async(model_id=..., name=...) sends PATCH."""
        mock_router.patch(url__regex=r"/v1/fine_tuning/models/.*").mock(
            return_value=httpx.Response(200, json=FT_MODEL_RESPONSE)
        )
        result = await mistral_client.models.update_async(
            model_id="ft:mistral-small:my-model:abc123",
            name="renamed-model",
        )
        assert result is not None


class TestModelsArchiveAsync:
    @pytest.mark.asyncio
    async def test_archive_async(self, mock_router, mistral_client):
        """models.archive_async(model_id=...) sends POST to archive endpoint."""
        mock_router.post(url__regex=r"/v1/fine_tuning/models/.*/archive").mock(
            return_value=httpx.Response(200, json=ARCHIVE_MODEL_RESPONSE)
        )
        result = await mistral_client.models.archive_async(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.archived is True


class TestModelsUnarchiveAsync:
    @pytest.mark.asyncio
    async def test_unarchive_async(self, mock_router, mistral_client):
        """models.unarchive_async(model_id=...) sends DELETE to archive endpoint."""
        mock_router.delete(url__regex=r"/v1/fine_tuning/models/.*/archive").mock(
            return_value=httpx.Response(200, json=UNARCHIVE_MODEL_RESPONSE)
        )
        result = await mistral_client.models.unarchive_async(
            model_id="ft:mistral-small:my-model:abc123"
        )
        assert result is not None
        assert result.archived is False


class TestModelsRetrieveNotFound:
    def test_retrieve_not_found(self, mock_router, mistral_client):
        """models.retrieve() raises SDKError on 404."""
        mock_router.get(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.models.retrieve(model_id="nonexistent-model")


class TestModelsDeleteNotFound:
    def test_delete_not_found(self, mock_router, mistral_client):
        """models.delete() raises SDKError on 404."""
        mock_router.delete(url__regex=r"/v1/models/.*").mock(
            return_value=httpx.Response(404, text="not found")
        )
        with pytest.raises(SDKError):
            mistral_client.models.delete(model_id="nonexistent-model")
