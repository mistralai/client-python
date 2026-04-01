from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict

from mistralai.extra.workflows.encoding.config import BlobStorageConfig
from .blob_storage_impl import BlobStorage, blob_storage_factory
from mistralai.extra.exceptions import WorkflowPayloadOffloadingException

# Re-export for tests and external usage
__all__ = ["BlobStorage", "blob_storage_factory", "get_blob_storage"]


@asynccontextmanager
async def get_blob_storage(
    blob_storage_config: BlobStorageConfig,
) -> AsyncGenerator[BlobStorage, None]:
    """
    Dependency provider for blob storage.

    This creates a blob storage instance based on the configuration.
    If blob storage is disabled, returns a placeholder that fails when used.

    Usage in activities/workflows:
        async def my_activity(
            blob_storage: BlobStorage = Depends(blob_storage),
        ) -> None:
            await blob_storage.upload_blob("key", b"data")
    """
    # Build kwargs for the factory based on storage provider
    factory_kwargs: Dict[str, Any] = {}

    if blob_storage_config.prefix:
        factory_kwargs["prefix"] = blob_storage_config.prefix

    if blob_storage_config.storage_provider.value == "azure":
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

        factory_kwargs.update(
            {
                "container_name": blob_storage_config.container_name,
                "azure_connection_string": azure_conn_str,
            }
        )

    elif blob_storage_config.storage_provider.value == "gcs":
        if not blob_storage_config.bucket_id:
            raise WorkflowPayloadOffloadingException(
                "bucket_id is required for GCS blob storage"
            )

        factory_kwargs["bucket_id"] = blob_storage_config.bucket_id

    elif blob_storage_config.storage_provider.value == "s3":
        if not blob_storage_config.bucket_name:
            raise WorkflowPayloadOffloadingException(
                "bucket_name is required for S3 blob storage"
            )

        factory_kwargs["bucket_name"] = blob_storage_config.bucket_name

        if blob_storage_config.region_name:
            factory_kwargs["region_name"] = blob_storage_config.region_name
        if blob_storage_config.endpoint_url:
            factory_kwargs["endpoint_url"] = blob_storage_config.endpoint_url
        aws_access_key = (
            blob_storage_config.aws_access_key_id.get_secret_value()
            if blob_storage_config.aws_access_key_id
            else None
        )
        aws_secret_key = (
            blob_storage_config.aws_secret_access_key.get_secret_value()
            if blob_storage_config.aws_secret_access_key
            else None
        )
        if aws_access_key:
            factory_kwargs["aws_access_key_id"] = aws_access_key
        if aws_secret_key:
            factory_kwargs["aws_secret_access_key"] = aws_secret_key

    storage = blob_storage_factory(
        storage_provider=blob_storage_config.storage_provider, **factory_kwargs
    )
    async with storage as blob_storage_instance:
        yield blob_storage_instance
