"""Tests for workflow encoding configuration lifecycle."""

import gc
import json
from typing import cast

import msgpack
import pytest
import zstandard
from pydantic import SecretStr

from mistralai.client import Mistral
from mistralai.client._hooks.workflow_encoding_hook import (
    _workflow_configs,
    _ENCODING_CONFIG_ID_ATTR,
    configure_workflow_encoding,
)
from mistralai.extra.workflows import (
    BlobStorageConfig,
    EncryptedStrField,
    PayloadCompressionConfig,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
    PayloadOffloadingConfig,
    StorageProvider,
    WorkflowEncodingConfig,
    ZstdCompressionConfig,
)
from mistralai.extra.exceptions import WorkflowPayloadCompressionException
from mistralai.extra.workflows.encoding.models import (
    EncodedPayloadOptions,
    NetworkEncodedInput,
    WorkflowContext,
)
from mistralai.extra.workflows.encoding.payload_encoder import (
    CompressedPayloadData,
    PayloadEncoder,
)
from mistralai.extra.tests.fixtures.workflow_encoding import InMemoryBlobStorage


_COMPRESSED_TEST_PAYLOAD = CompressedPayloadData.from_payload(
    b"compressed-data", ZstdCompressionConfig(level=3)
)


def _compressed_payload_msgpack(
    compressed_payload: CompressedPayloadData,
    *,
    invalid_compression: dict[str, object] | None = None,
    invalid_payload: object | None = None,
) -> bytes:
    payload_data: dict[str, object] = {
        "compression": compressed_payload.compression.model_dump(mode="json"),
        "payload": compressed_payload.payload,
    }
    if invalid_compression is not None:
        payload_data["compression"] = invalid_compression
    if invalid_payload is not None:
        payload_data["payload"] = invalid_payload
    return cast(bytes, msgpack.packb(payload_data, use_bin_type=True))


@pytest.fixture
def encryption_config() -> WorkflowEncodingConfig:
    """Create a test encryption config."""
    return WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=PayloadEncryptionMode.FULL,
            main_key=SecretStr("0" * 64),  # 256-bit key in hex
        )
    )


def test_payload_encoder_cleanup_on_client_gc(
    encryption_config: WorkflowEncodingConfig,
):
    """Test that PayloadEncoder is cleaned up when client is garbage collected."""
    initial_config_count = len(_workflow_configs)

    # Create client and configure encoding
    client = Mistral(api_key="test-key")
    configure_workflow_encoding(
        encryption_config,
        namespace="test-namespace",
        sdk_config=client.sdk_configuration,
    )

    # Verify config was added
    config_id = getattr(client.sdk_configuration, _ENCODING_CONFIG_ID_ATTR)
    assert config_id is not None
    assert config_id in _workflow_configs
    assert len(_workflow_configs) == initial_config_count + 1

    # Delete client and force garbage collection
    del client
    gc.collect()

    # Verify config was cleaned up
    assert config_id not in _workflow_configs
    assert len(_workflow_configs) == initial_config_count


def test_multiple_clients_independent_configs(
    encryption_config: WorkflowEncodingConfig,
):
    """Test that multiple clients have independent configs."""
    initial_config_count = len(_workflow_configs)

    # Create two clients with different namespaces
    client1 = Mistral(api_key="test-key-1")
    client2 = Mistral(api_key="test-key-2")

    configure_workflow_encoding(
        encryption_config,
        namespace="namespace-1",
        sdk_config=client1.sdk_configuration,
    )
    configure_workflow_encoding(
        encryption_config,
        namespace="namespace-2",
        sdk_config=client2.sdk_configuration,
    )

    # Verify both configs exist
    config_id1 = getattr(client1.sdk_configuration, _ENCODING_CONFIG_ID_ATTR)
    config_id2 = getattr(client2.sdk_configuration, _ENCODING_CONFIG_ID_ATTR)
    assert config_id1 != config_id2
    assert len(_workflow_configs) == initial_config_count + 2

    # Verify namespaces are independent
    assert _workflow_configs[config_id1].namespace == "namespace-1"
    assert _workflow_configs[config_id2].namespace == "namespace-2"

    # Delete first client
    del client1
    gc.collect()

    # First config should be cleaned up, second should remain
    assert config_id1 not in _workflow_configs
    assert config_id2 in _workflow_configs
    assert len(_workflow_configs) == initial_config_count + 1

    # Delete second client
    del client2
    gc.collect()

    # Both configs should be cleaned up
    assert config_id2 not in _workflow_configs
    assert len(_workflow_configs) == initial_config_count


def test_reconfigure_same_client(encryption_config: WorkflowEncodingConfig):
    """Test that reconfiguring the same client updates the config."""
    client = Mistral(api_key="test-key")

    # Initial configuration
    configure_workflow_encoding(
        encryption_config,
        namespace="namespace-v1",
        sdk_config=client.sdk_configuration,
    )

    config_id = getattr(client.sdk_configuration, _ENCODING_CONFIG_ID_ATTR)
    assert _workflow_configs[config_id].namespace == "namespace-v1"

    # Reconfigure with different namespace
    configure_workflow_encoding(
        encryption_config,
        namespace="namespace-v2",
        sdk_config=client.sdk_configuration,
    )

    # Should use same config_id but updated namespace
    assert getattr(client.sdk_configuration, _ENCODING_CONFIG_ID_ATTR) == config_id
    assert _workflow_configs[config_id].namespace == "namespace-v2"

    # Cleanup
    del client
    gc.collect()
    assert config_id not in _workflow_configs


@pytest.mark.asyncio
async def test_payload_encoder_compresses_network_inputs():
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        )
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == [EncodedPayloadOptions.COMPRESSED]
    compressed_payload = CompressedPayloadData.from_msgpack(encoded.get_payload())
    assert compressed_payload.compression == ZstdCompressionConfig(level=3)

    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_content_keeps_two_value_contract_for_compression():
    # Workflow workers use this low-level API directly from their Temporal codec.
    # Keep compression self-describing without changing the two-value contract.
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        )
    )
    encoder = PayloadEncoder(encoding_config=config)
    raw = json.dumps({"data": "x" * 20_000}).encode()

    encoded_data, encoding_options = await encoder.encode_payload_content(
        raw, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert isinstance(encoded_data, bytes)
    assert encoding_options == [EncodedPayloadOptions.COMPRESSED]


@pytest.mark.asyncio
async def test_payload_encoder_wraps_compression_config_in_payload_content():
    # Temporal metadata only carries encoding_options, so compressed bytes must
    # include the algorithm config needed to decode them independently.
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        )
    )
    encoder = PayloadEncoder(encoding_config=config)
    raw = json.dumps({"data": "x" * 20_000}).encode()

    encoded_data, encoding_options = await encoder.encode_payload_content(
        raw, WorkflowContext(namespace="test", execution_id="exec")
    )
    compressed_payload = CompressedPayloadData.from_msgpack(encoded_data)

    assert encoding_options == [EncodedPayloadOptions.COMPRESSED]
    assert compressed_payload.compression == ZstdCompressionConfig(level=3)
    assert compressed_payload.get_payload() != raw


@pytest.mark.asyncio
async def test_payload_encoder_decodes_compressed_payload_content_without_metadata():
    # This mirrors Temporal payload decoding, where the codec passes only bytes
    # plus encoding_options back into PayloadEncoder.
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        )
    )
    encoder = PayloadEncoder(encoding_config=config)
    raw = json.dumps({"data": "x" * 20_000}).encode()

    encoded_data, encoding_options = await encoder.encode_payload_content(
        raw, WorkflowContext(namespace="test", execution_id="exec")
    )
    decoded = await PayloadEncoder(WorkflowEncodingConfig()).decode_payload_content(
        encoded_data, encoding_options
    )

    assert decoded == raw


@pytest.mark.asyncio
async def test_payload_encoder_skips_compression_below_min_size():
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(min_size_bytes=1_000_000)
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == []
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_skips_compression_when_not_smaller():
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        )
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {"d": "x"}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == []
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_skips_compression_without_config():
    encoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(payload_compression=None)
    )
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == []
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_compression_can_prevent_offloading(monkeypatch):
    storage = InMemoryBlobStorage()
    monkeypatch.setattr(
        "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
        lambda _: storage,
    )
    config = WorkflowEncodingConfig(
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        ),
        payload_offloading=PayloadOffloadingConfig(
            min_size_bytes=1_000,
            storage_config=BlobStorageConfig(
                storage_provider=StorageProvider.S3,
                bucket_name="test-bucket",
            ),
        ),
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == [EncodedPayloadOptions.COMPRESSED]
    assert storage.blobs == {}
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "decoder_config",
    [
        WorkflowEncodingConfig(),
        WorkflowEncodingConfig(
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=1)
            )
        ),
    ],
)
async def test_payload_encoder_decodes_compressed_payload_with_decoder_config(
    decoder_config: WorkflowEncodingConfig,
):
    encoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=22)
            )
        )
    )
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )
    decoded = await PayloadEncoder(decoder_config).decode_network_result(
        encoded.model_dump(mode="json")
    )

    assert encoded.encoding_options == [EncodedPayloadOptions.COMPRESSED]
    compressed_payload = CompressedPayloadData.from_msgpack(encoded.get_payload())
    assert compressed_payload.compression == ZstdCompressionConfig(level=22)
    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("encryption_mode", "expected_options"),
    [
        (
            PayloadEncryptionMode.PARTIAL,
            [
                EncodedPayloadOptions.PARTIALLY_ENCRYPTED,
                EncodedPayloadOptions.COMPRESSED,
            ],
        ),
        (
            PayloadEncryptionMode.FULL,
            [EncodedPayloadOptions.COMPRESSED, EncodedPayloadOptions.ENCRYPTED],
        ),
    ],
)
async def test_payload_encoder_decodes_encrypted_compressed_payload_with_different_level(
    encryption_mode: PayloadEncryptionMode,
    expected_options: list[EncodedPayloadOptions],
):
    encryption_config = PayloadEncryptionConfig(
        mode=encryption_mode,
        main_key=SecretStr("0" * 64),
    )
    encoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(
            payload_encryption=encryption_config,
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=10)
            ),
        )
    )
    decoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(
            payload_encryption=encryption_config,
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=1)
            ),
        )
    )
    payload = {
        "data": "x" * 20_000,
        "secret": EncryptedStrField(data="secret value").model_dump(),
    }

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )
    decoded = await decoder.decode_network_result(encoded.model_dump(mode="json"))

    assert encoded.encoding_options == expected_options
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_decodes_with_tampered_compression_level():
    # Zstd decompression must depend on the frame data, not on the compression
    # level that was used when the payload was encoded.
    encoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(
            payload_compression=PayloadCompressionConfig(
                min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=22)
            )
        )
    )
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )
    compressed_payload = CompressedPayloadData.from_msgpack(encoded.get_payload())
    tampered_payload = compressed_payload.model_copy(
        update={"compression": ZstdCompressionConfig(level=1)}
    )
    tampered = NetworkEncodedInput.from_data(
        tampered_payload.to_msgpack(), encoded.encoding_options
    )

    decoded = await PayloadEncoder(WorkflowEncodingConfig()).decode_network_result(
        tampered.model_dump(mode="json")
    )

    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "compressed_payload",
    [
        b"compressed-data",
        _compressed_payload_msgpack(
            _COMPRESSED_TEST_PAYLOAD,
            invalid_compression={"algorithm": "lz4", "level": 1},
        ),
        _compressed_payload_msgpack(
            _COMPRESSED_TEST_PAYLOAD,
            invalid_compression={"level": 3},
        ),
        _compressed_payload_msgpack(
            _COMPRESSED_TEST_PAYLOAD,
            invalid_payload=123,
        ),
    ],
)
async def test_payload_encoder_invalid_compressed_payload_is_error(
    compressed_payload: bytes,
):
    encoded = NetworkEncodedInput.from_data(
        compressed_payload, [EncodedPayloadOptions.COMPRESSED]
    )

    with pytest.raises(WorkflowPayloadCompressionException):
        await PayloadEncoder(WorkflowEncodingConfig()).decode_network_result(
            encoded.model_dump(mode="json")
        )


@pytest.mark.asyncio
async def test_payload_encoder_corrupted_compressed_data_is_error():
    compressed_payload = CompressedPayloadData.from_payload(
        b"corrupted-data", ZstdCompressionConfig(level=3)
    )
    encoded = NetworkEncodedInput.from_data(
        compressed_payload.to_msgpack(),
        [EncodedPayloadOptions.COMPRESSED],
    )

    with pytest.raises(zstandard.ZstdError):
        await PayloadEncoder(WorkflowEncodingConfig()).decode_network_result(
            encoded.model_dump(mode="json")
        )


@pytest.mark.asyncio
async def test_payload_encoder_partially_encrypts_before_offloading(monkeypatch):
    storage = InMemoryBlobStorage()
    monkeypatch.setattr(
        "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
        lambda _: storage,
    )
    config = WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=PayloadEncryptionMode.PARTIAL,
            main_key=SecretStr("0" * 64),
        ),
        payload_offloading=PayloadOffloadingConfig(
            min_size_bytes=1,
            storage_config=BlobStorageConfig(
                storage_provider=StorageProvider.S3,
                bucket_name="test-bucket",
            ),
        ),
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {
        "data": "plain value",
        "secret": EncryptedStrField(data="secret value").model_dump(),
    }

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )
    offloaded_payload = json.loads(encoded.get_payload())
    offloaded_bytes = storage.blobs[offloaded_payload["key"]]

    assert encoded.encoding_options == [
        EncodedPayloadOptions.PARTIALLY_ENCRYPTED,
        EncodedPayloadOptions.OFFLOADED,
    ]
    assert b"plain value" in offloaded_bytes
    assert b"secret value" not in offloaded_bytes

    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("encryption_mode", "expected_options"),
    [
        (
            PayloadEncryptionMode.PARTIAL,
            [
                EncodedPayloadOptions.PARTIALLY_ENCRYPTED,
                EncodedPayloadOptions.COMPRESSED,
                EncodedPayloadOptions.OFFLOADED,
            ],
        ),
        (
            PayloadEncryptionMode.FULL,
            [
                EncodedPayloadOptions.COMPRESSED,
                EncodedPayloadOptions.OFFLOADED,
                EncodedPayloadOptions.ENCRYPTED,
            ],
        ),
    ],
)
async def test_payload_encoder_compression_offloading_encryption_roundtrip(
    monkeypatch,
    encryption_mode: PayloadEncryptionMode,
    expected_options: list[EncodedPayloadOptions],
):
    storage = InMemoryBlobStorage()
    monkeypatch.setattr(
        "mistralai.extra.workflows.encoding.payload_encoder.get_blob_storage",
        lambda _: storage,
    )
    config = WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=encryption_mode,
            main_key=SecretStr("0" * 64),
        ),
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        ),
        payload_offloading=PayloadOffloadingConfig(
            min_size_bytes=1,
            storage_config=BlobStorageConfig(
                storage_provider=StorageProvider.S3,
                bucket_name="test-bucket",
            ),
        ),
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {
        "data": "x" * 20_000,
        "secret": EncryptedStrField(data="secret value").model_dump(),
    }

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == expected_options
    assert len(storage.blobs) == 1
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_does_not_partially_encrypt_when_no_marked_fields():
    config = WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=PayloadEncryptionMode.PARTIAL,
            main_key=SecretStr("0" * 64),
        ),
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        ),
    )
    encoder = PayloadEncoder(encoding_config=config)
    payload = {"data": "x" * 20_000}

    encoded = await encoder.encode_network_input(
        payload, WorkflowContext(namespace="test", execution_id="exec")
    )

    assert encoded.encoding_options == [EncodedPayloadOptions.COMPRESSED]
    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


@pytest.mark.asyncio
async def test_payload_encoder_encodes_event_content_without_offloading():
    encryption_config = PayloadEncryptionConfig(
        mode=PayloadEncryptionMode.PARTIAL,
        main_key=SecretStr("0" * 64),
    )
    config = WorkflowEncodingConfig(
        payload_encryption=encryption_config,
        payload_compression=PayloadCompressionConfig(
            min_size_bytes=1, algorithm_config=ZstdCompressionConfig(level=3)
        ),
        payload_offloading=PayloadOffloadingConfig(
            min_size_bytes=1,
            storage_config=BlobStorageConfig(
                storage_provider=StorageProvider.S3,
                bucket_name="test-bucket",
            ),
        ),
    )
    encoder = PayloadEncoder(encoding_config=config)
    decoder = PayloadEncoder(
        encoding_config=WorkflowEncodingConfig(payload_encryption=encryption_config)
    )
    payload = json.dumps({"data": "x" * 20_000}).encode()

    encoded, encoding_options = await encoder.encode_event_payload_content(payload)
    decoded = await decoder.decode_payload_content(encoded, encoding_options)

    assert encoding_options == [EncodedPayloadOptions.COMPRESSED]
    assert decoded == payload


@pytest.mark.asyncio
async def test_workflow_encoding_hook_handles_gzipped_response():
    """Test that WorkflowEncodingHook correctly handles gzipped responses.

    When httpx receives a gzip-compressed response, it auto-decompresses the content
    but preserves the Content-Encoding header. If we create a new Response with this
    header but with already-decompressed content, httpx will try to decompress again,
    causing a zlib error. The fix strips Content-Encoding when creating new Responses.
    """
    import gzip
    import httpx
    from pydantic import SecretStr
    from mistralai.client import Mistral
    from mistralai.client._hooks.workflow_encoding_hook import (
        WorkflowEncodingHook,
        configure_workflow_encoding,
        EXECUTE_WORKFLOW_OPERATION_ID,
    )
    from mistralai.client._hooks.types import AfterSuccessContext, HookContext

    # Setup client with encryption
    client = Mistral(api_key="test-key")
    config = WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=PayloadEncryptionMode.FULL,
            main_key=SecretStr("0" * 64),
        )
    )
    configure_workflow_encoding(
        config,
        namespace="test-namespace",
        sdk_config=client.sdk_configuration,
    )

    # Create an encoded result using the encoder
    encoder = PayloadEncoder(encoding_config=config)
    context = WorkflowContext(namespace="test-namespace", execution_id="test-123")
    original_data = {"secret": "value"}
    encoded_input = await encoder.encode_network_input(original_data, context)

    # Create gzipped response with encoded result
    body = {
        "execution_id": "test-exec-123",
        "status": "COMPLETED",
        "result": encoded_input.model_dump(mode="json"),
    }
    compressed_body = gzip.compress(json.dumps(body).encode("utf-8"))
    mock_request = httpx.Request(
        "GET", "https://api.example.com/v1/workflows/executions/test-exec-123"
    )
    response = httpx.Response(
        status_code=200,
        headers={"Content-Type": "application/json", "Content-Encoding": "gzip"},
        content=compressed_body,
        request=mock_request,
    )

    # Create hook context
    hook_ctx = AfterSuccessContext(
        HookContext(
            config=client.sdk_configuration,
            base_url="https://api.example.com",
            operation_id=EXECUTE_WORKFLOW_OPERATION_ID,
            oauth2_scopes=[],
            security_source=None,
        )
    )

    # Call after_success - without the fix, this raises httpx.DecodingError
    hook = WorkflowEncodingHook()
    result = hook.after_success(hook_ctx, response)

    # Verify response is valid and result is decoded
    assert isinstance(result, httpx.Response)
    response_body = json.loads(result.content)
    assert response_body["result"] == original_data
