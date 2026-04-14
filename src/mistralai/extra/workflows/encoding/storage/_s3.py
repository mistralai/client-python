from __future__ import annotations

from typing import Any, cast

import aioboto3  # type: ignore[import-untyped]
from botocore.exceptions import ClientError  # type: ignore[import-untyped]

from .blob_storage import BlobNotFoundError, BlobStorage


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
