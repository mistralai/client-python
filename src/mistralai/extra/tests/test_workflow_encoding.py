"""Tests for workflow encoding configuration lifecycle."""

import gc

import pytest
from pydantic import SecretStr

from mistralai.client import Mistral
from mistralai.client._hooks.workflow_encoding_hook import (
    _workflow_configs,
    _ENCODING_CONFIG_ID_ATTR,
    configure_workflow_encoding,
)
from mistralai.extra.workflows import (
    WorkflowEncodingConfig,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
)


@pytest.fixture
def encryption_config() -> WorkflowEncodingConfig:
    """Create a test encryption config."""
    return WorkflowEncodingConfig(
        payload_encryption=PayloadEncryptionConfig(
            mode=PayloadEncryptionMode.FULL,
            main_key=SecretStr("0" * 64),  # 256-bit key in hex
        )
    )


def test_payload_encoder_cleanup_on_client_gc(encryption_config: WorkflowEncodingConfig):
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


def test_multiple_clients_independent_configs(encryption_config: WorkflowEncodingConfig):
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
