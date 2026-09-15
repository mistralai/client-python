from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, AsyncGenerator

from mistralai.extra.workflows.encoding.config import BlobStorageConfig, StorageProvider
from mistralai.extra.exceptions import WorkflowPayloadOffloadingException

if TYPE_CHECKING:
    from ._s3 import S3BlobStorage

_S3_STORAGE_CACHE: dict[tuple[str | None, ...], "S3BlobStorage"] = {}


class BlobNotFoundError(Exception):
    """Raised when a blob is not found in storage."""

    pass


class BlobStorage(ABC):
    """Abstract base class for blob storage implementations."""

    @abstractmethod
    async def upload_blob(self, key: str, content: bytes) -> str:
        """Upload a blob to storage and return its URL."""
        pass

    @abstractmethod
    async def get_blob(self, key: str) -> bytes:
        """Download a blob from storage."""
        pass

    @abstractmethod
    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        """Get blob properties. Returns None if blob doesn't exist."""
        pass

    @abstractmethod
    async def delete_blob(self, key: str) -> None:
        """Delete a blob from storage."""
        pass

    @abstractmethod
    async def blob_exists(self, key: str) -> bool:
        """Check if a blob exists."""
        pass

    async def __aenter__(self) -> "BlobStorage":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        pass


@asynccontextmanager
async def get_blob_storage(
    blob_storage_config: BlobStorageConfig,
) -> AsyncGenerator[BlobStorage, None]:
    """ Create a blob storage instance based on the configuration.
    """
    storage: BlobStorage
    prefix = blob_storage_config.prefix
    cache_key: tuple[str | None, ...] | None = None

    if blob_storage_config.storage_provider == StorageProvider.AZURE:
        try:
            from ._azure import AzureBlobStorage  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "Azure Blob Storage support requires azure-storage-blob and azure-identity. "
                "Install with: pip install 'mistralai[workflow_payload_offloading_azure]'"
            ) from e

        if not blob_storage_config.container_name:
            raise WorkflowPayloadOffloadingException(
                "container_name is required for Azure blob storage"
            )
        azure_conn_str = (
            blob_storage_config.azure_connection_string.get_secret_value()
            if blob_storage_config.azure_connection_string
            else None
        )
        storage = AzureBlobStorage(
            container_name=blob_storage_config.container_name,
            azure_connection_string=azure_conn_str,
            prefix=prefix,
            azure_storage_account_url=blob_storage_config.azure_storage_account_url,
        )

    elif blob_storage_config.storage_provider == StorageProvider.GCS:
        try:
            from ._gcs import GCSBlobStorage  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "Google Cloud Storage support requires gcloud-aio-storage. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_gcs]'"
            ) from e

        if not blob_storage_config.bucket_id:
            raise WorkflowPayloadOffloadingException(
                "bucket_id is required for GCS blob storage"
            )
        storage = GCSBlobStorage(
            bucket_id=blob_storage_config.bucket_id,
            prefix=prefix,
        )

    elif blob_storage_config.storage_provider == StorageProvider.S3:
        try:
            from ._s3 import S3BlobStorage  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "AWS S3 support requires aioboto3. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_s3]'"
            ) from e

        if not blob_storage_config.bucket_name:
            raise WorkflowPayloadOffloadingException(
                "bucket_name is required for S3 blob storage"
            )
        access_key = (
            blob_storage_config.aws_access_key_id.get_secret_value()
            if blob_storage_config.aws_access_key_id
            else None
        )
        secret_key = (
            blob_storage_config.aws_secret_access_key.get_secret_value()
            if blob_storage_config.aws_secret_access_key
            else None
        )
        if blob_storage_config.reuse_client:
            cache_key = (
                blob_storage_config.bucket_name,
                prefix,
                blob_storage_config.region_name,
                blob_storage_config.endpoint_url,
                access_key,
                secret_key,
            )
            storage = _S3_STORAGE_CACHE.get(cache_key) or S3BlobStorage(
                bucket_name=blob_storage_config.bucket_name,
                prefix=prefix,
                region_name=blob_storage_config.region_name,
                endpoint_url=blob_storage_config.endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                reuse_client=True,
            )
            _S3_STORAGE_CACHE[cache_key] = storage
        else:
            storage = S3BlobStorage(
                bucket_name=blob_storage_config.bucket_name,
                prefix=prefix,
                region_name=blob_storage_config.region_name,
                endpoint_url=blob_storage_config.endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                reuse_client=False,
            )

    else:
        raise ValueError(
            f"Unsupported storage provider: {blob_storage_config.storage_provider}"
        )

    try:
        entered = await storage.__aenter__()
    except BaseException:
        # A pooled client that never finished entering must not stay cached.
        if cache_key is not None:
            _S3_STORAGE_CACHE.pop(cache_key, None)
        raise
    try:
        yield entered
    finally:
        await storage.__aexit__(*sys.exc_info())


async def close_cached_blob_storages() -> None:
    storages = list(_S3_STORAGE_CACHE.values())
    _S3_STORAGE_CACHE.clear()
    for storage in storages:
        await storage.aclose()


__all__ = [
    "BlobStorage",
    "BlobNotFoundError",
    "close_cached_blob_storages",
    "get_blob_storage",
]
