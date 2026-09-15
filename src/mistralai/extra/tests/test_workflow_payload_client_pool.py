"""Tests for the reusable S3 payload-offloading blob-storage client pool."""

import unittest
from typing import Any
from unittest import mock

from mistralai.extra.workflows.encoding.config import BlobStorageConfig, StorageProvider
from mistralai.extra.workflows.encoding.storage import _s3 as s3_module
from mistralai.extra.workflows.encoding.storage._s3 import S3BlobStorage
from mistralai.extra.workflows.encoding.storage.blob_storage import (
    _S3_STORAGE_CACHE,
    close_cached_blob_storages,
    get_blob_storage,
)


class _FakeS3Client:
    def __init__(self, session: "_FakeSession") -> None:
        self._session = session
        self.entered = False
        self.exited = False

    async def __aenter__(self) -> "_FakeS3Client":
        self.entered = True
        self._session.client_enters += 1
        return self

    async def __aexit__(self, *_args: Any) -> None:
        self.exited = True
        self._session.client_exits += 1


class _FakeSession:
    def __init__(self) -> None:
        self.clients_created = 0
        self.client_enters = 0
        self.client_exits = 0

    def client(self, *_args: Any, **_kwargs: Any) -> _FakeS3Client:
        self.clients_created += 1
        return _FakeS3Client(self)


def _s3_config(**overrides: Any) -> BlobStorageConfig:
    values: dict[str, Any] = {
        "storage_provider": StorageProvider.S3,
        "bucket_name": "test-bucket",
    }
    values.update(overrides)
    return BlobStorageConfig(**values)


class ReuseClientConfigDefaultTest(unittest.TestCase):
    def test_reuse_client_defaults_to_false(self) -> None:
        assert "reuse_client" in BlobStorageConfig.model_fields
        assert BlobStorageConfig().reuse_client is False
        assert _s3_config().reuse_client is False


class BlobStorageClientPoolTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        await close_cached_blob_storages()
        self._session = _FakeSession()
        patcher = mock.patch.object(
            s3_module.aioboto3, "Session", return_value=self._session
        )
        self.addAsyncCleanup(close_cached_blob_storages)
        self.addCleanup(patcher.stop)
        patcher.start()

    async def test_reuse_client_false_creates_independent_clients(self) -> None:
        config = _s3_config(reuse_client=False)

        async with get_blob_storage(config) as first:
            assert isinstance(first, S3BlobStorage)
            first_client = first._client
        async with get_blob_storage(config) as second:
            assert isinstance(second, S3BlobStorage)
            second_client = second._client

        assert self._session.clients_created == 2
        assert self._session.client_enters == 2
        # Each non-reusing context closes its own client on exit.
        assert self._session.client_exits == 2
        assert first_client is not second_client
        assert first is not second
        assert not _S3_STORAGE_CACHE

    async def test_reuse_client_true_reuses_single_client(self) -> None:
        config = _s3_config(reuse_client=True)

        async with get_blob_storage(config) as first:
            assert isinstance(first, S3BlobStorage)
            first_client = first._client
        async with get_blob_storage(config) as second:
            assert isinstance(second, S3BlobStorage)
            second_client = second._client

        assert self._session.clients_created == 1
        assert self._session.client_enters == 1
        # The reused client is kept open across contexts.
        assert self._session.client_exits == 0
        assert first is second
        assert first_client is second_client
        assert len(_S3_STORAGE_CACHE) == 1

    async def test_reuse_client_true_distinct_configs_get_distinct_clients(self) -> None:
        async with get_blob_storage(_s3_config(reuse_client=True)) as a:
            pass
        async with get_blob_storage(
            _s3_config(reuse_client=True, bucket_name="other-bucket")
        ) as b:
            pass

        assert a is not b
        assert self._session.clients_created == 2
        assert len(_S3_STORAGE_CACHE) == 2

    async def test_close_cached_blob_storages_closes_and_is_repeatable(self) -> None:
        async with get_blob_storage(_s3_config(reuse_client=True)) as storage:
            assert isinstance(storage, S3BlobStorage)

        assert storage._client is not None
        assert self._session.client_exits == 0

        await close_cached_blob_storages()

        assert self._session.client_exits == 1
        assert storage._client is None
        assert not _S3_STORAGE_CACHE

        # Repeated cleanup is a no-op and must not raise or double-close.
        await close_cached_blob_storages()
        assert self._session.client_exits == 1
        assert not _S3_STORAGE_CACHE


class BlobStorageClientLifecycleFailureTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        await close_cached_blob_storages()
        self.addAsyncCleanup(close_cached_blob_storages)

    async def test_enter_failure_surfaces_root_error(self) -> None:
        boom = RuntimeError("connect failed")

        class _FailingEnterCtx:
            async def __aenter__(self) -> Any:
                raise boom

            async def __aexit__(self, *_args: Any) -> None:
                return None

        class _FailingEnterSession:
            def client(self, *_args: Any, **_kwargs: Any) -> _FailingEnterCtx:
                return _FailingEnterCtx()

        with mock.patch.object(
            s3_module.aioboto3, "Session", return_value=_FailingEnterSession()
        ):
            with self.assertRaises(RuntimeError) as caught:
                async with get_blob_storage(_s3_config(reuse_client=True)):
                    pass

        assert caught.exception is boom
        # A failed enter must not leave a half-open client cached.
        assert not _S3_STORAGE_CACHE

    async def test_exit_failure_surfaces_root_error(self) -> None:
        boom = RuntimeError("teardown failed")

        class _FailingExitClient:
            async def __aenter__(self) -> "_FailingExitClient":
                return self

            async def __aexit__(self, *_args: Any) -> None:
                raise boom

        class _FailingExitSession:
            def client(self, *_args: Any, **_kwargs: Any) -> _FailingExitClient:
                return _FailingExitClient()

        with mock.patch.object(
            s3_module.aioboto3, "Session", return_value=_FailingExitSession()
        ):
            with self.assertRaises(RuntimeError) as caught:
                async with get_blob_storage(_s3_config(reuse_client=False)):
                    pass

        assert caught.exception is boom


if __name__ == "__main__":
    unittest.main()
