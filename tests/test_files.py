import orjson
from mistralai.models.files import FileDeleted, FileObject

from .utils import (
    mock_file_deleted_response_payload,
    mock_file_response_payload,
    mock_response,
)


class TestFilesClient:
    def test_create_file(self, client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        client._client.request.return_value = mock_response(
            200,
            expected_response_file.json(),
        )

        response_file = client.files.create(b"file_content")

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/files",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            files={"file": b"file_content"},
            json=None,
            data={"purpose": "fine-tune"},
        )
        assert response_file == expected_response_file

    def test_retrieve(self, client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        client._client.request.return_value = mock_response(
            200,
            expected_response_file.json(),
        )

        response_file = client.files.retrieve("file_id")

        client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/files/file_id",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file

    def test_list_files(self, client):
        expected_response_file = FileObject.model_validate_json(mock_file_response_payload())
        client._client.request.return_value = mock_response(
            200,
            orjson.dumps(
                {
                    "data": [expected_response_file.model_dump()],
                    "object": "list",
                }
            ),
        )

        response_files = client.files.list()
        response_file = response_files.data[0]

        client._client.request.assert_called_once_with(
            "get",
            "https://api.mistral.ai/v1/files",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file

    def test_delete_file(self, client):
        expected_response_file = FileDeleted.model_validate_json(mock_file_deleted_response_payload())
        client._client.request.return_value = mock_response(200, expected_response_file.json())

        response_file = client.files.delete("file_id")

        client._client.request.assert_called_once_with(
            "delete",
            "https://api.mistral.ai/v1/files/file_id",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key",
            },
            json={},
            data=None,
        )
        assert response_file == expected_response_file
