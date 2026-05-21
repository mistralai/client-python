from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
from importlib import import_module
from types import ModuleType

from pydantic import TypeAdapter, ValidationError

from mistralai.extra.exceptions import WorkflowPayloadCompressionException
from mistralai.extra.workflows.encoding.config import (
    AlgorithmConfig,
    PayloadCompressionConfig,
    ZstdCompressionConfig,
)

_ALGORITHM_CONFIG_ADAPTER: TypeAdapter[AlgorithmConfig] = TypeAdapter(AlgorithmConfig)


class Compressor(ABC):
    @property
    @abstractmethod
    def algorithm_config(self) -> AlgorithmConfig:
        """Algorithm config stored with metadata for config-independent decoding."""

    @abstractmethod
    def compress(self, data: bytes) -> bytes: ...

    @abstractmethod
    def decompress(self, data: bytes) -> bytes: ...


def _require_zstandard() -> ModuleType:
    try:
        return import_module("zstandard")
    except ImportError:
        raise WorkflowPayloadCompressionException(
            "Payload compression requires installing mistralai[workflow_payload_compression]"
        ) from None


class ZstdCompressor(Compressor):
    @property
    def algorithm_config(self) -> AlgorithmConfig:
        return self._config

    def __init__(self, cfg: ZstdCompressionConfig) -> None:
        zstd = _require_zstandard()
        self._config = cfg
        self._compressor = zstd.ZstdCompressor(level=cfg.level)
        self._decompressor = zstd.ZstdDecompressor()

    def compress(self, data: bytes) -> bytes:
        result: bytes = self._compressor.compress(data)
        return result

    def decompress(self, data: bytes) -> bytes:
        result: bytes = self._decompressor.decompress(data)
        return result


def compressor_from_config(algo_config: AlgorithmConfig) -> Compressor:
    if isinstance(algo_config, ZstdCompressionConfig):
        return ZstdCompressor(algo_config)
    raise WorkflowPayloadCompressionException(
        f"Unsupported compression algorithm: {algo_config.algorithm!r}"
    )


@lru_cache(maxsize=8)
def _build_compressor_for_config(config_json: str) -> Compressor:
    try:
        algo_config = _ALGORITHM_CONFIG_ADAPTER.validate_json(config_json)
    except ValidationError as exc:
        raise WorkflowPayloadCompressionException(
            f"Invalid compression config in payload: {exc}"
        ) from exc

    return compressor_from_config(algo_config)


def build_compressor(
    compression_config: PayloadCompressionConfig | None,
) -> Compressor | None:
    if compression_config is None:
        return None
    return _build_compressor_for_config(
        compression_config.algorithm_config.model_dump_json()
    )
