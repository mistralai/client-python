from __future__ import annotations

from typing import Any, cast

import aiohttp
from gcloud.aio.storage import Storage

from .blob_storage import BlobNotFoundError, BlobStorage


class GCSBlobStorage(BlobStorage):
    def __init__(self, bucket_id: str, prefix: str | None = None):
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
