from __future__ import annotations

# mypy: disable-error-code="import-not-found,import-untyped"
# pyright: reportMissingImports=false

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, cast

from mistralai.extra.workflows.encoding.config import StorageProvider

if TYPE_CHECKING:
    import aioboto3
    import aiohttp
    from azure.core.exceptions import ResourceNotFoundError
    from azure.storage.blob.aio import BlobServiceClient
    from botocore.exceptions import ClientError
    from gcloud.aio.storage import Storage

try:
    import aioboto3
    from botocore.exceptions import ClientError

    _HAS_S3 = True
except ImportError:
    _HAS_S3 = False

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.storage.blob.aio import BlobServiceClient

    _HAS_AZURE = True
except ImportError:
    _HAS_AZURE = False

try:
    import aiohttp
    from gcloud.aio.storage import Storage

    _HAS_GCS = True
except ImportError:
    _HAS_GCS = False


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


class AzureBlobStorage(BlobStorage):
    def __init__(
        self,
        container_name: str,
        azure_connection_string: str,
        prefix: str | None = None,
    ):
        if not _HAS_AZURE:
            raise ImportError(
                "Azure Blob Storage support requires azure-storage-blob. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_azure]'"
            )
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


class GCSBlobStorage(BlobStorage):
    def __init__(self, bucket_id: str, prefix: str | None = None):
        if not _HAS_GCS:
            raise ImportError(
                "Google Cloud Storage support requires gcloud-aio-storage. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_gcs]'"
            )
        self.bucket_id = bucket_id
        self.prefix = prefix or ""
        self._storage: Storage | None = None
        self._session: aiohttp.ClientSession | None = None

    def _get_full_key(self, key: str) -> str:
        if not self.prefix:
            return key
        if key.startswith(self.prefix):
            return key
        return f"{self.prefix}/{key}"

    async def __aenter__(self) -> "GCSBlobStorage":
        self._session = aiohttp.ClientSession()
        self._storage = Storage(session=self._session)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._storage:
            await self._storage.close()
        if self._session:
            await self._session.close()

    async def upload_blob(self, key: str, content: bytes) -> str:
        full_key = self._get_full_key(key)
        assert self._storage is not None
        response = await self._storage.upload(self.bucket_id, full_key, content)
        return str(response.get("selfLink"))

    async def get_blob(self, key: str) -> bytes:
        full_key = self._get_full_key(key)
        assert self._storage is not None
        try:
            content = await self._storage.download(self.bucket_id, full_key)
            return cast(bytes, content)
        except Exception as e:
            if "404" in str(e) or "Not Found" in str(e):
                raise BlobNotFoundError(f"Blob not found: {key}") from e
            raise

    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        full_key = self._get_full_key(key)
        assert self._storage is not None
        try:
            metadata = await self._storage.download_metadata(self.bucket_id, full_key)
            return {
                "size": int(metadata.get("size", 0)),
                "last_modified": metadata.get("updated"),
            }
        except Exception as e:
            if "404" in str(e) or "Not Found" in str(e):
                return None
            raise

    async def delete_blob(self, key: str) -> None:
        full_key = self._get_full_key(key)
        assert self._storage is not None
        await self._storage.delete(self.bucket_id, full_key)

    async def blob_exists(self, key: str) -> bool:
        full_key = self._get_full_key(key)
        assert self._storage is not None
        try:
            await self._storage.download_metadata(self.bucket_id, full_key)
            return True
        except Exception as e:
            if "404" in str(e) or "Not Found" in str(e):
                return False
            raise


class S3BlobStorage(BlobStorage):
    def __init__(
        self,
        bucket_name: str,
        prefix: str | None = None,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
    ):
        if not _HAS_S3:
            raise ImportError(
                "AWS S3 support requires aioboto3. "
                "Install it with: pip install 'mistralai[workflow_payload_offloading_s3]'"
            )
        self.bucket_name = bucket_name
        self.prefix = prefix or ""
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self._session: aioboto3.Session | None = None
        self._client: Any = None

    def _get_full_key(self, key: str) -> str:
        if not self.prefix:
            return key
        if key.startswith(self.prefix):
            return key
        return f"{self.prefix}/{key}"

    async def __aenter__(self) -> "S3BlobStorage":
        self._session = aioboto3.Session()
        assert self._session is not None
        kwargs: dict[str, Any] = {}
        if self.region_name:
            kwargs["region_name"] = self.region_name
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url
        if self.aws_access_key_id:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
        if self.aws_secret_access_key:
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key

        self._client = self._session.client("s3", **kwargs)
        self._client = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None
        self._client = None

    async def upload_blob(self, key: str, content: bytes) -> str:
        full_key = self._get_full_key(key)
        await self._client.put_object(
            Bucket=self.bucket_name, Key=full_key, Body=content
        )
        endpoint = (
            self.endpoint_url
            or f"https://s3.{self.region_name or 'us-east-1'}.amazonaws.com"
        )
        return f"{endpoint}/{self.bucket_name}/{full_key}"

    async def get_blob(self, key: str) -> bytes:
        full_key = self._get_full_key(key)
        try:
            response = await self._client.get_object(
                Bucket=self.bucket_name, Key=full_key
            )
            async with response["Body"] as stream:
                return cast(bytes, await stream.read())
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") == "NoSuchKey":
                raise BlobNotFoundError(f"Blob not found: {key}") from e
            raise

    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        full_key = self._get_full_key(key)
        try:
            response = await self._client.head_object(
                Bucket=self.bucket_name, Key=full_key
            )
            return {
                "size": response["ContentLength"],
                "last_modified": response["LastModified"],
            }
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") in ("NoSuchKey", "404"):
                return None
            raise

    async def delete_blob(self, key: str) -> None:
        full_key = self._get_full_key(key)
        await self._client.delete_object(Bucket=self.bucket_name, Key=full_key)

    async def blob_exists(self, key: str) -> bool:
        full_key = self._get_full_key(key)
        try:
            await self._client.head_object(Bucket=self.bucket_name, Key=full_key)
            return True
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") in ("NoSuchKey", "404"):
                return False
            raise


def blob_storage_factory(
    storage_provider: StorageProvider, **kwargs: Any
) -> BlobStorage:
    if storage_provider == StorageProvider.AZURE:
        return AzureBlobStorage(**kwargs)
    elif storage_provider == StorageProvider.GCS:
        return GCSBlobStorage(**kwargs)
    elif storage_provider == StorageProvider.S3:
        return S3BlobStorage(**kwargs)
    else:
        raise ValueError(f"Unsupported storage provider: {storage_provider}")
