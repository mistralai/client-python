from enum import Enum
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, SecretStr


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
    azure_storage_account_url: Optional[str] = None

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


class ZstdCompressionConfig(BaseModel):
    algorithm: Literal["zstd"] = "zstd"
    level: int = Field(default=3, ge=1, le=22)


AlgorithmConfig = Annotated[
    Union[ZstdCompressionConfig], Field(discriminator="algorithm")
]


class PayloadCompressionConfig(BaseModel):
    min_size_bytes: int = 1024 * 1024  # 1MB
    algorithm_config: AlgorithmConfig = Field(default_factory=ZstdCompressionConfig)


class WorkflowEncodingConfig(BaseModel):
    payload_offloading: PayloadOffloadingConfig | None = None
    payload_encryption: PayloadEncryptionConfig | None = None
    payload_compression: PayloadCompressionConfig | None = None
