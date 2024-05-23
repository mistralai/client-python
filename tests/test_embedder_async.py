import pytest
from mistralai.models.embeddings import EmbeddingResponse

from .utils import mock_embedding_response_payload, mock_response


class TestAsyncEmbeddings:
    @pytest.mark.asyncio
    async def test_embeddings(self, async_client):
        async_client._client.request.return_value = mock_response(
            200,
            mock_embedding_response_payload(),
        )

        result = await async_client.embeddings(
            model="mistral-embed",
            input="What is the best French cheese?",
        )

        async_client._client.request.assert_awaited_once_with(
            "post",
            "https://api.mistral.ai/v1/embeddings",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={"model": "mistral-embed", "input": "What is the best French cheese?"},
        )

        assert isinstance(result, EmbeddingResponse), "Should return an EmbeddingResponse"
        assert len(result.data) == 1
        assert result.data[0].index == 0
        assert result.object == "list"

    @pytest.mark.asyncio
    async def test_embeddings_batch(self, async_client):
        async_client._client.request.return_value = mock_response(
            200,
            mock_embedding_response_payload(batch_size=10),
        )

        result = await async_client.embeddings(
            model="mistral-embed",
            input=["What is the best French cheese?"] * 10,
        )

        async_client._client.request.assert_awaited_once_with(
            "post",
            "https://api.mistral.ai/v1/embeddings",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-embed",
                "input": ["What is the best French cheese?"] * 10,
            },
        )

        assert isinstance(result, EmbeddingResponse), "Should return an EmbeddingResponse"
        assert len(result.data) == 10
        assert result.data[0].index == 0
        assert result.object == "list"
