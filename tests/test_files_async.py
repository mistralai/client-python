import orjson
import pytest
from mistralai.models.files import FileDeleted, FileObject

from .utils import (
    mock_file_deleted_response_payload,
    mock_file_response_payload,
    mock_response,
)


class TestFilesAyncClient:
    @pytest.mark.asyncio
    async def test_create_file(self, async_client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        async_client._client.request.return_value = mock_response(
            200,
            expected_response_file.model_dump_json(),
        )

        response_file = await async_client.files.create(b"file_content")

        async_client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/files",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            files={"file": b"file_content"},
            json=None,
            data={"purpose": "fine-tune"},
        )
        assert response_file == expected_response_file

    @pytest.mark.asyncio
    async def test_retrieve(self, async_client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        async_client._client.request.return_value = mock_response(
            200,
            expected_response_file.model_dump_json(),
        )

        response_file = await async_client.files.retrieve("file_id")

        async_client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/files/file_id",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file

    @pytest.mark.asyncio
    async def test_list_files(self, async_client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        async_client._client.request.return_value = mock_response(
            200,
            orjson.dumps(
                {
                    "data": [expected_response_file.model_dump()],
                    "object": "list",
                }
            ),
        )

        response_files = await async_client.files.list()
        response_file = response_files.data[0]

        async_client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/files",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file

    @pytest.mark.asyncio
    async def test_delete_file(self, async_client):
        expected_response_file = FileDeleted.model_validate_json(mock_file_deleted_response_payload())
        async_client._client.request.return_value = mock_response(200, expected_response_file.model_dump_json())

        response_file = await async_client.files.delete("file_id")

        async_client._client.request.assert_called_once_with(
            "delete",
            "https://api.mistral.ai/v1/files/file_id",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file
