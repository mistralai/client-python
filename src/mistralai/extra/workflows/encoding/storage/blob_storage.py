from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from mistralai.extra.workflows.encoding.config import BlobStorageConfig, StorageProvider
from mistralai.extra.exceptions import WorkflowPayloadOffloadingException


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

    if blob_storage_config.storage_provider == StorageProvider.AZURE:
        try:
            from ._azure import AzureBlobStorage  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "Azure Blob Storage support requires azure-storage-blob. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_azure]'"
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
        if not azure_conn_str:
            raise WorkflowPayloadOffloadingException(
                "azure_connection_string is required for Azure blob storage"
            )
        storage = AzureBlobStorage(
            container_name=blob_storage_config.container_name,
            azure_connection_string=azure_conn_str,
            prefix=prefix,
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
        storage = S3BlobStorage(
            bucket_name=blob_storage_config.bucket_name,
            prefix=prefix,
            region_name=blob_storage_config.region_name,
            endpoint_url=blob_storage_config.endpoint_url,
            aws_access_key_id=(
                blob_storage_config.aws_access_key_id.get_secret_value()
                if blob_storage_config.aws_access_key_id
                else None
            ),
            aws_secret_access_key=(
                blob_storage_config.aws_secret_access_key.get_secret_value()
                if blob_storage_config.aws_secret_access_key
                else None
            ),
        )

    else:
        raise ValueError(
            f"Unsupported storage provider: {blob_storage_config.storage_provider}"
        )

    async with storage as blob_storage_instance:
        yield blob_storage_instance


__all__ = ["BlobStorage", "BlobNotFoundError", "get_blob_storage"]
