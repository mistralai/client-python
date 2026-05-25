from __future__ import annotations

import base64
import functools
import hashlib
from importlib import import_module
import json
import logging
import os
from types import ModuleType
import urllib.parse
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False
from pydantic_core import from_json, to_json

from mistralai.extra.workflows.encoding.config import (
    AlgorithmConfig,
    PayloadEncryptionConfig,
    PayloadEncryptionMode,
    PayloadOffloadingConfig,
    WorkflowEncodingConfig,
)
from mistralai.extra.workflows.encoding.payload_compressor import (
    build_compressor,
    compressor_from_config,
)
from .storage.blob_storage import get_blob_storage, BlobNotFoundError
from mistralai.extra.workflows.encoding.models import (
    EncodedPayloadOptions,
    EncryptableFieldTypes,
    NetworkEncodedInput,
    NetworkEncodedResult,
    WorkflowContext,
)
from mistralai.client.models.jsonpatchpayloadresponse import JSONPatchPayloadResponse
from mistralai.extra.exceptions import (
    WorkflowPayloadCompressionException,
    WorkflowPayloadEncryptionException,
    WorkflowPayloadOffloadingException,
)

logger = logging.getLogger(__name__)


class OffloadedPayloadData(BaseModel):
    key: str


def _require_msgpack() -> ModuleType:
    try:
        return import_module("msgpack")
    except ImportError:
        raise WorkflowPayloadCompressionException(
            "Payload compression requires installing mistralai[workflow_payload_compression]"
        ) from None


class CompressedPayloadData(BaseModel):
    compression: AlgorithmConfig
    payload: bytes

    @classmethod
    def from_payload(
        cls, payload: bytes, compression: AlgorithmConfig
    ) -> "CompressedPayloadData":
        return cls(compression=compression, payload=payload)

    @classmethod
    def from_msgpack(cls, data: bytes) -> "CompressedPayloadData":
        msgpack = _require_msgpack()
        try:
            unpacked = msgpack.unpackb(data, raw=False)
        except Exception as exc:
            raise WorkflowPayloadCompressionException(
                "Invalid compressed payload data"
            ) from exc
        try:
            return cls.model_validate(unpacked)
        except ValidationError as exc:
            raise WorkflowPayloadCompressionException(
                "Invalid compressed payload metadata"
            ) from exc

    def to_msgpack(self) -> bytes:
        msgpack = _require_msgpack()
        return cast(
            bytes,
            msgpack.packb(
                {
                    "compression": self.compression.model_dump(mode="json"),
                    "payload": self.payload,
                },
                use_bin_type=True,
            ),
        )

    def get_payload(self) -> bytes:
        return self.payload


class PayloadEncoder:
    """This class is in charge of payload encoding/decoding operations such as:
    - Field-level or full-payload encryption
    - Compression
    - Blob storage offloading
    """

    BLOB_STORAGE_KEY_PREFIX = "temporal-payload"
    _NONCE_SIZE = 12

    offloading_config: Optional[PayloadOffloadingConfig]
    encryption_config: Optional[PayloadEncryptionConfig]

    encryptor_main: Optional[AESGCM] = None
    encryptor_secondary: Optional[AESGCM] = None

    def __init__(
        self,
        encoding_config: WorkflowEncodingConfig,
    ) -> None:
        self.offloading_config = encoding_config.payload_offloading
        if (
            self.offloading_config is not None
            and not self.offloading_config.storage_config
        ):
            raise WorkflowPayloadOffloadingException(
                "Blob storage config is not set for workflow payload encoding"
            )

        self.compression_config = encoding_config.payload_compression
        self.compressor = build_compressor(self.compression_config)
        self.encryption_config = encoding_config.payload_encryption
        if self.encryption_config is not None:
            if not _HAS_CRYPTO:
                raise ImportError(
                    "Encryption support requires cryptography. "
                    "Install it with: pip install 'mistralai[workflow_payload_encryption]'"
                )
            main_key = (
                self.encryption_config.main_key.get_secret_value()
                if self.encryption_config.main_key
                else None
            )
            if not main_key:
                raise WorkflowPayloadEncryptionException(
                    "You must configure payload encryption key"
                )
            self.encryptor_main = AESGCM(bytes.fromhex(main_key))
            secondary_key_secret = self.encryption_config.secondary_key
            secondary_key = (
                secondary_key_secret.get_secret_value()
                if secondary_key_secret
                else None
            )
            if secondary_key:
                self.encryptor_secondary = AESGCM(bytes.fromhex(secondary_key))

    @staticmethod
    def blob_storage_key_prefix(context: WorkflowContext) -> str:
        quote = functools.partial(urllib.parse.quote, safe="")
        return "/".join(
            [
                PayloadEncoder.BLOB_STORAGE_KEY_PREFIX,
                quote(context.namespace),
                quote(context.execution_id),
            ]
        )

    def _encrypt(self, data: bytes) -> bytes:
        if self.encryptor_main is None:
            raise WorkflowPayloadEncryptionException(
                "You must configure payload encryption"
            )
        nonce = os.urandom(self._NONCE_SIZE)
        return nonce + self.encryptor_main.encrypt(nonce, data, None)

    def _decrypt(self, data: bytes) -> bytes:
        if self.encryptor_main is None:
            raise WorkflowPayloadEncryptionException(
                "You must configure payload encryption"
            )
        try:
            return self.encryptor_main.decrypt(
                data[: self._NONCE_SIZE], data[self._NONCE_SIZE :], None
            )
        except InvalidTag as main_exc:
            if self.encryptor_secondary:
                logger.warning(
                    "Failed to decrypt payload with main key, trying secondary key"
                )
                try:
                    return self.encryptor_secondary.decrypt(
                        data[: self._NONCE_SIZE], data[self._NONCE_SIZE :], None
                    )
                except InvalidTag:
                    pass
            logger.error("Could not decrypt payload", exc_info=main_exc)
            raise WorkflowPayloadEncryptionException(
                "Failed to decrypt payload"
            ) from main_exc

    async def _handle_offloading(
        self, data: bytes, context: Optional[WorkflowContext]
    ) -> tuple[bytes, bool]:
        if (
            self.offloading_config is None
            or self.offloading_config.storage_config is None
        ):
            raise WorkflowPayloadOffloadingException(
                "You must configure payload offloading storage"
            )

        if len(data) < self.offloading_config.min_size_bytes:
            return data, False

        if not context:
            logger.error(
                "Payload offloading required but no context was provided. Cannot proceed with offloading..."
            )
            return data, False

        # Hash the content to have a uniq idempotent key for this payload
        blob_key = f"sha256:{hashlib.sha256(data).hexdigest()}"
        payload_key = f"{self.blob_storage_key_prefix(context)}/{blob_key}"
        async with get_blob_storage(
            self.offloading_config.storage_config
        ) as blob_storage:
            blob = None
            try:
                blob = await blob_storage.get_blob_properties(payload_key)
            except BlobNotFoundError:
                pass

            if not blob:
                logger.debug("Offloading payload")
                await blob_storage.upload_blob(key=payload_key, content=data)
            else:
                logger.debug("Offloaded payload exists already")

            data = OffloadedPayloadData(key=payload_key).model_dump_json().encode()
            return data, True

    @staticmethod
    def _extract_encrypted_fields(data: Any = None) -> list[dict[str, Any]]:
        encrypted_fields = []
        if isinstance(data, dict):
            if data.get("field_type") == EncryptableFieldTypes.STRING:
                return [data]
            for _, field_data in data.items():
                if isinstance(field_data, (dict, list)):
                    encrypted_fields.extend(
                        PayloadEncoder._extract_encrypted_fields(field_data)
                    )
        elif isinstance(data, list):
            for item in data:
                encrypted_fields.extend(PayloadEncoder._extract_encrypted_fields(item))
        return encrypted_fields

    async def _partially_encrypt_fields(self, data: bytes) -> tuple[bytes, bool]:
        try:
            obj = json.loads(data)
        except json.decoder.JSONDecodeError:
            return data, False

        encrypted_fields = self._extract_encrypted_fields(obj)
        for encrypted_field in encrypted_fields:
            encrypted_data = self._encrypt(encrypted_field["data"].encode())
            encrypted_field["data"] = base64.b64encode(encrypted_data).decode()

        return json.dumps(obj).encode(), len(encrypted_fields) > 0

    async def _partially_decrypt_fields(self, data: bytes) -> tuple[bytes, bool]:
        try:
            obj = json.loads(data)
        except json.decoder.JSONDecodeError:
            return data, False

        encrypted_fields = self._extract_encrypted_fields(obj)
        for encrypted_field in encrypted_fields:
            encrypted_data = base64.b64decode(encrypted_field["data"])
            encrypted_field["data"] = self._decrypt(encrypted_data).decode()

        return json.dumps(obj).encode(), len(encrypted_fields) > 0

    def _compress(self, data: bytes) -> tuple[bytes, bool]:
        if (
            self.compression_config is None
            or len(data) < self.compression_config.min_size_bytes
        ):
            return data, False
        assert self.compressor is not None, (
            "This should never be reached: compression is enabled in config "
            "but PayloadEncoder.__init__ did not build a compressor"
        )
        compressed = self.compressor.compress(data)
        if len(compressed) >= len(data):
            return data, False
        compressed_payload = CompressedPayloadData.from_payload(
            compressed, self.compressor.algorithm_config
        )
        return compressed_payload.to_msgpack(), True

    def _decompress(self, data: bytes) -> bytes:
        compressed_payload = CompressedPayloadData.from_msgpack(data)
        return compressor_from_config(compressed_payload.compression).decompress(
            compressed_payload.get_payload()
        )

    async def encode_payload_content(
        self,
        data: Union[bytes, str],
        context: Optional[WorkflowContext] = None,
        *,
        allow_offloading: bool = True,
    ) -> tuple[bytes, list[EncodedPayloadOptions]]:
        """Handle payload encoding.

        Encoding options are appended in the exact order in which transforms are
        applied; decode_payload_content reverses that list to restore the data.
        """
        if isinstance(data, str):
            data = data.encode()

        encoding_options: list[EncodedPayloadOptions] = []

        # Partial encryption needs the original JSON fields. It must run before
        # compression or offloading, which make field-level markers unavailable.
        if (
            self.encryption_config is not None
            and self.encryption_config.mode == PayloadEncryptionMode.PARTIAL
        ):
            data, partially_encrypted = await self._partially_encrypt_fields(data)
            if partially_encrypted:
                encoding_options.append(EncodedPayloadOptions.PARTIALLY_ENCRYPTED)

        # Compress before offloading so the offloading threshold applies to the
        # bytes that would otherwise cross the network, not to the raw JSON size.
        data, compressed = self._compress(data)
        if compressed:
            encoding_options.append(EncodedPayloadOptions.COMPRESSED)

        if allow_offloading and self.offloading_config is not None:
            data, offloaded = await self._handle_offloading(data, context)
            if offloaded:
                encoding_options.append(EncodedPayloadOptions.OFFLOADED)

        # Full encryption intentionally remains the final transform. If the
        # payload was offloaded, this encrypts the small blob-reference envelope
        # rather than the blob bytes.
        if (
            self.encryption_config is not None
            and self.encryption_config.mode == PayloadEncryptionMode.FULL
        ):
            data = self._encrypt(data)
            encoding_options.append(EncodedPayloadOptions.ENCRYPTED)

        return data, encoding_options

    async def encode_event_payload_content(
        self, data: Union[bytes, str]
    ) -> tuple[bytes, list[EncodedPayloadOptions]]:
        """Encode event payload content without offloading."""
        return await self.encode_payload_content(data, allow_offloading=False)

    async def decode_payload_content(
        self,
        data: bytes,
        encoding_options: List[EncodedPayloadOptions],
    ) -> bytes:
        # Decode in the exact reverse order of the encoding_options wire list.
        for option in reversed(encoding_options):
            if option == EncodedPayloadOptions.ENCRYPTED:
                data = self._decrypt(data)
            elif option == EncodedPayloadOptions.PARTIALLY_ENCRYPTED:
                data, _ = await self._partially_decrypt_fields(data)
            elif option == EncodedPayloadOptions.COMPRESSED:
                data = self._decompress(data)
            elif option == EncodedPayloadOptions.OFFLOADED:
                if (
                    self.offloading_config is None
                    or not self.offloading_config.storage_config
                ):
                    raise WorkflowPayloadOffloadingException(
                        "Payload offloading is not enabled but an offloaded payload was received"
                    )
                async with get_blob_storage(
                    self.offloading_config.storage_config
                ) as blob_storage:
                    offloaded_payload_data = OffloadedPayloadData.model_validate_json(
                        data
                    )
                    data = await blob_storage.get_blob(offloaded_payload_data.key)
            else:
                raise WorkflowPayloadOffloadingException(
                    f"Unknown decoding option: {option}"
                )

        return data

    async def decode_event_payload(
        self, payload_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Decrypt an event payload's value if it has encoding_options.

        Args:
            payload_data: Dict with 'type', 'value', and 'encoding_options' fields

        Returns:
            Dict with decrypted 'value' and empty 'encoding_options'
        """
        encoding_options_strs = payload_data.get("encoding_options", [])
        if not encoding_options_strs:
            return payload_data

        encoding_options = [EncodedPayloadOptions(opt) for opt in encoding_options_strs]

        # Handle selective encryption for json_patch payloads
        if EncodedPayloadOptions.PARTIALLY_ENCRYPTED in encoding_options:
            try:
                payload = JSONPatchPayloadResponse.model_validate(payload_data)
                if isinstance(payload.value, list):
                    decrypted_patches = self._decrypt_json_patch_selective(
                        [p.model_dump() for p in payload.value]
                    )
                    return {
                        "type": payload.type,
                        "value": decrypted_patches,
                        "encoding_options": [],
                    }
            except ValidationError:
                pass  # Not a json_patch payload, fall through to full decryption

        # Standard full encryption (base64 string value)
        encrypted_bytes = base64.b64decode(payload_data["value"])
        decrypted_bytes = await self.decode_payload_content(
            encrypted_bytes,
            encoding_options,
        )
        decrypted_value = json.loads(decrypted_bytes)

        return {
            "type": payload_data["type"],
            "value": decrypted_value,
            "encoding_options": [],
        }

    _ENCRYPTED_PATCH_TYPE = "__encrypted__"

    def _decrypt_json_patch_selective(
        self, patches: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Decrypt patches with EncryptedPatchValue wrapper: {type: "__encrypted__", value: "base64..."}."""
        decrypted = []
        for patch in patches:
            patch_value = patch.get("value")

            # EncryptedPatchValue format: {"type": "__encrypted__", "value": "base64-encrypted-data"}
            if (
                isinstance(patch_value, dict)
                and patch_value.get("type") == self._ENCRYPTED_PATCH_TYPE
            ):
                encrypted_b64 = patch_value.get("value", "")
                encrypted_data = base64.b64decode(encrypted_b64)
                decrypted_bytes = self._decrypt(encrypted_data)
                decrypted.append(
                    {
                        **patch,
                        "value": json.loads(decrypted_bytes),
                    }
                )
            else:
                decrypted.append(patch)
        return decrypted

    async def encode_network_input(
        self, data: Optional[Dict[str, Any]], context: WorkflowContext
    ) -> NetworkEncodedInput:
        """This method MUST be called to format every payload send to Mistral Workflows control plane
        to ensure a proper encoding of the payload.
        """
        encoded_data, encoding_options = await self.encode_payload_content(
            to_json(data), context
        )
        network_input = NetworkEncodedInput.from_data(encoded_data, encoding_options)
        return network_input

    async def decode_network_result(self, data: Any) -> Any:
        """This method MUST be called to format every response payload from the Mistral Workflows control plane
        otherwise the payload will not be decoded, hence not usable.
        """
        try:
            network_encoded_payload = NetworkEncodedResult.model_validate(data)
        except ValueError:
            logger.warning("Network result is not a NetworkEncodedResult")
            return data

        byte_results = await self.decode_payload_content(
            network_encoded_payload.get_payload(),
            network_encoded_payload.encoding_options,
        )
        try:
            return from_json(byte_results)
        except ValueError:
            logger.warning("Payload is not a valid json.")
            return byte_results  # Return as-is if JSON conversion fails

    def check_is_payload_encoded(self, data: Any) -> bool:
        """Check if the payload is encoded (offloaded or encrypted)"""
        try:
            NetworkEncodedResult.model_validate(data)
            return True
        except ValueError:
            return False
