import pytest
from mistralai.models.models import ModelDeleted

from .utils import mock_model_deleted_response_payload, mock_response


class TestAsyncDeleteModel:
    @pytest.mark.asyncio
    async def test_delete_model(self, async_client):
        expected_response_model = ModelDeleted.model_validate_json(mock_model_deleted_response_payload())
        async_client._client.request.return_value = mock_response(200, expected_response_model.json())

        response_model = await async_client.delete_model("model_id")

        async_client._client.request.assert_called_once_with(
            "delete",
            "https://api.mistral.ai/v1/models/model_id",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )

        assert response_model == expected_response_model

