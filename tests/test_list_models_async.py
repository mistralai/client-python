import pytest
from mistralai.models.models import ModelList

from .utils import mock_list_models_response_payload, mock_response


class TestAsyncListModels:
    @pytest.mark.asyncio
    async def test_list_models(self, async_client):
        async_client._client.request.return_value = mock_response(
            200,
            mock_list_models_response_payload(),
        )

        result = await async_client.list_models()

        async_client._client.request.assert_awaited_once_with(
            "get",
            "https://api.mistral.ai/v1/models",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={},
            data=None,
        )

        assert isinstance(result, ModelList), "Should return an ModelList"
        assert len(result.data) == 4
        assert result.object == "list"
