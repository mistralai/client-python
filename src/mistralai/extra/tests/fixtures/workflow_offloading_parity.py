"""Shared fixtures for workflow payload offloading and compression parity with
the TS client.

The TypeScript client (``ts/client-ts``) must offload payloads under the same
blob keys and with the same bytes as this client, and decode the payloads this
client compresses and offloads. These cases run the real ``PayloadEncoder``
with deterministic nonces and an in-memory blob storage, and are written to
the TS test suite, which replays them. The
``test_workflow_offloading_parity`` test checks that this client still
produces the committed file.

Compressed bytes are not compared: they depend on the libzstd version of each
client, while any zstd frame decodes the same.

Regenerate the file from ``client-python`` with:

    uv run python -m mistralai.extra.tests.fixtures.workflow_offloading_parity
"""

from __future__ import annotations

import json
from typing import Any, Callable, Optional
from unittest import mock

from pydantic import SecretStr

from mistralai.extra.tests.fixtures.workflow_encoding import InMemoryBlobStorage
from mistralai.extra.tests.fixtures.workflow_encryption_parity import (
    FIXTURE_PATH as ENCRYPTION_FIXTURE_PATH,
    KEYS,
    NETWORK_INPUTS,
    _b64,
    _run_with_nonces,
)
from mistralai.extra.workflows.encoding import (
    BlobStorageConfig,
    PayloadCompressionConfig,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
    PayloadOffloadingConfig,
    StorageProvider,
    WorkflowEncodingConfig,
    ZstdCompressionConfig,
)
from mistralai.extra.workflows.encoding import payload_encoder as payload_encoder_module
from mistralai.extra.workflows.encoding.models import WorkflowContext
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

FIXTURE_PATH = ENCRYPTION_FIXTURE_PATH.with_name("workflow_offloading_parity.json")

CONTEXTS = {
    "plain": WorkflowContext(namespace="parity", execution_id="parity-execution"),
    # Python's quote(safe="") escapes !'()* and keeps ~, unlike encodeURIComponent.
    "escaped": WorkflowContext(
        namespace="team ns/!'()*~é", execution_id="exec:1+2&3?#"
    ),
}

LARGE_INPUT: dict[str, Any] = {
    "data": "x" * 2_000,
    "secret": {"field_type": "__encrypted_str__", "data": "secret value"},
}


def _config(
    encryption: Optional[str] = None,
    offloading: Optional[int] = None,
    compression: Optional[int] = None,
    level: int = 3,
    main: str = "main",
    secondary: Optional[str] = None,
) -> dict[str, Any]:
    """The config of a case, as the TS tests read it."""
    config: dict[str, Any] = {}
    if encryption:
        config["encryption"] = {"mode": encryption, "main_key": main}
        if secondary:
            config["encryption"]["secondary_key"] = secondary
    if offloading is not None:
        config["offloading"] = {"min_size_bytes": offloading}
    if compression is not None:
        config["compression"] = {"min_size_bytes": compression, "level": level}
    return config


def _encoder(config: dict[str, Any]) -> PayloadEncoder:
    encryption = config.get("encryption")
    offloading = config.get("offloading")
    compression = config.get("compression")
    return PayloadEncoder(
        WorkflowEncodingConfig(
            payload_encryption=PayloadEncryptionConfig(
                mode=PayloadEncryptionMode(encryption["mode"]),
                main_key=SecretStr(KEYS[encryption["main_key"]]),
                secondary_key=(
                    SecretStr(KEYS[encryption["secondary_key"]])
                    if "secondary_key" in encryption
                    else None
                ),
            )
            if encryption
            else None,
            payload_offloading=PayloadOffloadingConfig(
                min_size_bytes=offloading["min_size_bytes"],
                storage_config=BlobStorageConfig(
                    storage_provider=StorageProvider.S3,
                    bucket_name="parity-bucket",
                ),
            )
            if offloading
            else None,
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=compression["min_size_bytes"],
                algorithm_config=ZstdCompressionConfig(level=compression["level"]),
            )
            if compression
            else None,
        )
    )


def _context(name: Optional[str]) -> Optional[dict[str, str]]:
    if name is None:
        return None
    context = CONTEXTS[name]
    return {"namespace": context.namespace, "execution_id": context.execution_id}


def _run(
    case: str, storage: InMemoryBlobStorage, fn: Callable[[], Any]
) -> tuple[Any, list[str]]:
    with mock.patch.object(
        payload_encoder_module, "get_blob_storage", lambda _: storage
    ):
        return _run_with_nonces(case, fn)


def _blobs(storage: InMemoryBlobStorage) -> dict[str, str]:
    return {key: _b64(content) for key, content in sorted(storage.blobs.items())}


def _encode_network_input_cases() -> list[dict[str, Any]]:
    """Offloaded inputs, compared byte for byte with their blobs."""
    variants: list[tuple[str, dict[str, Any], str, str]] = []
    for encryption in [None, "full", "partial"]:
        for input_name in ["object", "unicode", "partial_top_level", "partial_nested"]:
            variants.append(
                (input_name, _config(encryption, offloading=1), input_name, "plain")
            )
        variants.append(
            ("escaped_context", _config(encryption, offloading=1), "object", "escaped")
        )
    variants.append(
        ("below_threshold", _config("full", offloading=1_000_000), "object", "plain")
    )

    cases = []
    for label, config, input_name, context_name in variants:
        mode = config.get("encryption", {}).get("mode", "none")
        name = f"{mode}/{label}/{input_name}"
        storage = InMemoryBlobStorage()
        encoder = _encoder(config)
        input_value = NETWORK_INPUTS[input_name]
        encoded, nonces = _run(
            name,
            storage,
            lambda: encoder.encode_network_input(
                input_value, CONTEXTS[context_name]
            ),
        )
        cases.append(
            {
                "name": name,
                "config": config,
                "context": _context(context_name),
                "input": input_value,
                "nonces": nonces,
                "expected": encoded.model_dump(mode="json"),
                "blobs": _blobs(storage),
            }
        )
    return cases


def _encode_payload_content_cases() -> list[dict[str, Any]]:
    """Raw payloads with the offloading options of encode_payload_content."""
    variants: list[tuple[str, Optional[str], dict[str, Any]]] = [
        ("force_offload", "plain", {"force_offload": True}),
        ("force_offload_escaped", "escaped", {"force_offload": True}),
        ("offloading_not_allowed", "plain", {"allow_offloading": False}),
        ("no_context", None, {}),
    ]
    cases = []
    for label, context_name, options in variants:
        for encryption in [None, "full"]:
            name = f"{encryption or 'none'}/{label}"
            config = _config(encryption, offloading=1_000_000 if "force" in label else 1)
            payload = b'{"tiny": true}'
            storage = InMemoryBlobStorage()
            encoder = _encoder(config)
            context = CONTEXTS[context_name] if context_name else None
            (data, encoding_options), nonces = _run(
                name,
                storage,
                lambda: encoder.encode_payload_content(payload, context, **options),
            )
            cases.append(
                {
                    "name": name,
                    "config": config,
                    "context": _context(context_name),
                    "options": options,
                    "data_b64": _b64(payload),
                    "nonces": nonces,
                    "expected": {
                        "data_b64": _b64(data),
                        "encoding_options": [o.value for o in encoding_options],
                    },
                    "blobs": _blobs(storage),
                }
            )
    return cases


def _compressed_cases() -> list[dict[str, Any]]:
    """Compressed inputs: the TS client must decode Python's, and produce the
    same encoding options and compression metadata."""
    variants: list[tuple[str, dict[str, Any], dict[str, Any]]] = [
        ("compressed", _config(compression=1), _config(compression=1)),
        ("level_22", _config(compression=1, level=22), _config(compression=1)),
        ("not_smaller", _config(compression=1), _config(compression=1)),
        ("below_threshold", _config(compression=1_000_000), _config(compression=1)),
        (
            "offloaded",
            _config(compression=1, offloading=1),
            _config(compression=1, offloading=1),
        ),
        (
            "compression_prevents_offloading",
            _config(compression=1, offloading=1_000),
            _config(compression=1, offloading=1_000),
        ),
        (
            "full",
            _config("full", compression=1, offloading=1),
            _config("full", compression=1, offloading=1),
        ),
        (
            "partial",
            _config("partial", compression=1, offloading=1),
            _config("partial", compression=1, offloading=1),
        ),
        (
            "rotated_key",
            _config("full", compression=1, offloading=1, main="secondary"),
            _config("full", offloading=1, main="main", secondary="secondary"),
        ),
    ]
    cases = []
    for name, encoder_config, decoder_config in variants:
        input_value: Any = {"d": "x"} if name == "not_smaller" else LARGE_INPUT
        storage = InMemoryBlobStorage()
        encoder = _encoder(encoder_config)
        encoded, _ = _run(
            name,
            storage,
            lambda: encoder.encode_network_input(input_value, CONTEXTS["plain"]),
        )
        decoded, _ = _run(
            name,
            storage,
            lambda: _encoder(decoder_config).decode_network_result(
                encoded.model_dump(mode="json")
            ),
        )
        assert decoded == input_value
        cases.append(
            {
                "name": name,
                "encoder_config": encoder_config,
                "decoder_config": decoder_config,
                "context": _context("plain"),
                "input": input_value,
                "encoded": encoded.model_dump(mode="json"),
                "blobs": _blobs(storage),
            }
        )
    return cases


def build_fixtures() -> dict[str, Any]:
    return {
        "keys": KEYS,
        "encode_network_input": _encode_network_input_cases(),
        "encode_payload_content": _encode_payload_content_cases(),
        "compressed": _compressed_cases(),
    }


def render_fixtures() -> str:
    return json.dumps(build_fixtures(), indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(render_fixtures(), encoding="utf-8")
    print(f"Wrote {FIXTURE_PATH}")
