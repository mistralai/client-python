from __future__ import annotations

from typing import Any, cast

from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from .blob_storage import BlobNotFoundError, BlobStorage


class AzureBlobStorage(BlobStorage):
    def __init__(
        self,
        container_name: str,
        azure_connection_string: str | None = None,
        prefix: str | None = None,
        azure_storage_account_url: str | None = None,
    ):
        if azure_connection_string and azure_storage_account_url:
            raise ValueError(
                "azure_connection_string and azure_storage_account_url are mutually exclusive"
            )
        if not azure_connection_string and not azure_storage_account_url:
            raise ValueError(
                "Either azure_connection_string or azure_storage_account_url must be provided"
            )
        self.container_name = container_name
        self.connection_string = azure_connection_string
        self.account_url = azure_storage_account_url
        self.prefix = prefix or ""
        self._service_client: BlobServiceClient | None = None
        self._container_client: Any = None
        self._credential: Any = None

    def _get_full_key(self, key: str) -> str:
        if not self.prefix:
            return key
        if key.startswith(self.prefix):
            return key
        return f"{self.prefix}/{key}"

    async def __aenter__(self) -> "AzureBlobStorage":
        if self.connection_string:
            self._service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
        else:
            assert self.account_url is not None
            self._credential = DefaultAzureCredential()
            self._service_client = BlobServiceClient(
                self.account_url, credential=self._credential
            )
        assert self._service_client is not None
        self._container_client = self._service_client.get_container_client(
            self.container_name
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._service_client:
            await self._service_client.close()
        if self._credential:
            await self._credential.close()

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
