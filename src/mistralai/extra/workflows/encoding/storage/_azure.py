from __future__ import annotations

from typing import Any, cast

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob.aio import BlobServiceClient
from .blob_storage import BlobNotFoundError, BlobStorage


class AzureBlobStorage(BlobStorage):
    def __init__(
        self,
        container_name: str,
        azure_connection_string: str,
        prefix: str | None = None,
    ):
        self.container_name = container_name
        self.connection_string = azure_connection_string
        self.prefix = prefix or ""
        self._service_client: BlobServiceClient | None = None
        self._container_client: Any = None

    def _get_full_key(self, key: str) -> str:
        if not self.prefix:
            return key
        if key.startswith(self.prefix):
            return key
        return f"{self.prefix}/{key}"

    async def __aenter__(self) -> "AzureBlobStorage":
        self._service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )
        assert self._service_client is not None
        self._container_client = self._service_client.get_container_client(
            self.container_name
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._service_client:
            await self._service_client.close()

    async def upload_blob(self, key: str, content: bytes) -> str:
        full_key = self._get_full_key(key)
        blob_client = self._container_client.get_blob_client(full_key)
        await blob_client.upload_blob(content, overwrite=True)
        return cast(str, blob_client.url)

    async def get_blob(self, key: str) -> bytes:
        full_key = self._get_full_key(key)
        blob_client = self._container_client.get_blob_client(full_key)
        try:
            stream = await blob_client.download_blob()
            return cast(bytes, await stream.readall())
        except ResourceNotFoundError as e:
            raise BlobNotFoundError(f"Blob not found: {key}") from e

    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        full_key = self._get_full_key(key)
        blob_client = self._container_client.get_blob_client(full_key)
        try:
            props = await blob_client.get_blob_properties()
            return {"size": props.size, "last_modified": props.last_modified}
        except ResourceNotFoundError:
            return None

    async def delete_blob(self, key: str) -> None:
        full_key = self._get_full_key(key)
        blob_client = self._container_client.get_blob_client(full_key)
        await blob_client.delete_blob()

    async def blob_exists(self, key: str) -> bool:
        full_key = self._get_full_key(key)
        blob_client = self._container_client.get_blob_client(full_key)
        return cast(bool, await blob_client.exists())
