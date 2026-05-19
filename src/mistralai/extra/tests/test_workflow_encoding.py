"""Tests for workflow encoding configuration lifecycle."""

import gc
import json

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
from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder
from mistralai.extra.tests.fixtures.workflow_encoding import InMemoryBlobStorage


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
    assert encoded.encoding_metadata == {
        "compression": {"algorithm": "zstd", "level": 3}
    }
    assert not encoded.get_payload().startswith(b"{")

    decoded = await encoder.decode_network_result(encoded.model_dump(mode="json"))
    assert decoded == payload


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
    encoder = PayloadEncoder(encoding_config=WorkflowEncodingConfig())
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
    assert encoded.encoding_metadata == {
        "compression": {"algorithm": "zstd", "level": 22}
    }
    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("encryption_mode", "expected_options"),
    [
        (
            PayloadEncryptionMode.PARTIAL,
            [EncodedPayloadOptions.PARTIALLY_ENCRYPTED, EncodedPayloadOptions.COMPRESSED],
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
    tampered = NetworkEncodedInput.from_data(
        encoded.get_payload(),
        encoded.encoding_options,
        {"compression": {"algorithm": "zstd", "level": 1}},
    )

    decoded = await PayloadEncoder(WorkflowEncodingConfig()).decode_network_result(
        tampered.model_dump(mode="json")
    )

    assert decoded == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "encoding_metadata",
    [
        {},
        {"compression": {"algorithm": "lz4", "level": 1}},
        {"compression": {"level": 3}},
    ],
)
async def test_payload_encoder_invalid_compression_metadata_is_error(
    encoding_metadata: dict[str, object],
):
    encoded = NetworkEncodedInput.from_data(
        b"compressed-data", [EncodedPayloadOptions.COMPRESSED], encoding_metadata
    )

    with pytest.raises(WorkflowPayloadCompressionException):
        await PayloadEncoder(WorkflowEncodingConfig()).decode_network_result(
            encoded.model_dump(mode="json")
        )


@pytest.mark.asyncio
async def test_payload_encoder_corrupted_compressed_data_is_error():
    encoded = NetworkEncodedInput.from_data(
        b"corrupted-data",
        [EncodedPayloadOptions.COMPRESSED],
        {"compression": {"algorithm": "zstd", "level": 3}},
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
