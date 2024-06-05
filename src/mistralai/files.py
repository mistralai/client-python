from typing import Any

from mistralai.exceptions import (
    MistralException,
)
from mistralai.models.files import FileDeleted, FileObject, Files


class FilesClient:
    def __init__(self, client: Any):
        self.client = client

    def create(
        self,
        file: bytes,
        purpose: str = "fine-tune",
    ) -> FileObject:
        single_response = self.client._request(
            "post",
            None,
            "v1/files",
            files={"file": file},
            data={"purpose": purpose},
        )
        for response in single_response:
            return FileObject(**response)
        raise MistralException("No response received")

    def retrieve(self, file_id: str) -> FileObject:
        single_response = self.client._request("get", {}, f"v1/files/{file_id}")
        for response in single_response:
            return FileObject(**response)
        raise MistralException("No response received")

    def list(self) -> Files:
        single_response = self.client._request("get", {}, "v1/files")
        for response in single_response:
            return Files(**response)
        raise MistralException("No response received")

    def delete(self, file_id: str) -> FileDeleted:
        single_response = self.client._request("delete", {}, f"v1/files/{file_id}")
        for response in single_response:
            return FileDeleted(**response)
        raise MistralException("No response received")


class FilesAsyncClient:
    def __init__(self, client: Any):
        self.client = client

    async def create(
        self,
        file: bytes,
        purpose: str = "fine-tune",
    ) -> FileObject:
        single_response = self.client._request(
            "post",
            None,
            "v1/files",
            files={"file": file},
            data={"purpose": purpose},
        )
        async for response in single_response:
            return FileObject(**response)
        raise MistralException("No response received")

    async def retrieve(self, file_id: str) -> FileObject:
        single_response = self.client._request("get", {}, f"v1/files/{file_id}")
        async for response in single_response:
            return FileObject(**response)
        raise MistralException("No response received")

    async def list(self) -> Files:
        single_response = self.client._request("get", {}, "v1/files")
        async for response in single_response:
            return Files(**response)
        raise MistralException("No response received")

    async def delete(self, file_id: str) -> FileDeleted:
        single_response = self.client._request("delete", {}, f"v1/files/{file_id}")
        async for response in single_response:
            return FileDeleted(**response)
        raise MistralException("No response received")
