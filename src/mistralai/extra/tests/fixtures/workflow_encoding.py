from __future__ import annotations

from typing import Any


class InMemoryBlobStorage:
    def __init__(self) -> None:
        self.blobs: dict[str, bytes] = {}

    async def __aenter__(self) -> "InMemoryBlobStorage":
        return self

    async def __aexit__(self, *_args: Any) -> None:
        pass

    async def upload_blob(self, key: str, content: bytes) -> str:
        self.blobs[key] = content
        return key

    async def get_blob(self, key: str) -> bytes:
        return self.blobs[key]

    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        if key not in self.blobs:
            return None
        return {"size": len(self.blobs[key]), "last_modified": "test"}
