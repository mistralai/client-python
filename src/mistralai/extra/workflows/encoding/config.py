from enum import Enum
from pydantic import SecretStr, BaseModel
from typing import Optional


class StorageProvider(str, Enum):
    AZURE = "azure"
    GCS = "gcs"
    S3 = "s3"


class BlobStorageConfig(BaseModel):
    storage_provider: StorageProvider = StorageProvider.S3
    prefix: Optional[str] = None

    # Azure settings
    container_name: Optional[str] = None
    azure_connection_string: Optional[SecretStr] = None

    # GCS settings
    bucket_id: Optional[str] = None

    # S3 settings
    bucket_name: Optional[str] = None
    region_name: Optional[str] = None
    endpoint_url: Optional[str] = None
    aws_access_key_id: Optional[SecretStr] = None
    aws_secret_access_key: Optional[SecretStr] = None


class PayloadOffloadingConfig(BaseModel):
    storage_config: Optional[BlobStorageConfig] = None
    min_size_bytes: int = 1024 * 1024  # 1MB


class PayloadEncryptionMode(str, Enum):
    FULL = "full"
    PARTIAL = "partial"


class PayloadEncryptionConfig(BaseModel):
    mode: PayloadEncryptionMode

    # If both keys are provided, the main key will be used for encryption and both keys will be used for decryption
    # to support key rotation.
    main_key: Optional[SecretStr] = None
    secondary_key: Optional[SecretStr] = None


class WorkflowEncodingConfig(BaseModel):
    payload_offloading: PayloadOffloadingConfig | None = None
    payload_encryption: PayloadEncryptionConfig | None = None
