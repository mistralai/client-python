from enum import Enum
from typing import Literal, Optional

import base64
from pydantic import BaseModel, Field


class EncodedPayloadOptions(str, Enum):
    OFFLOADED = "offloaded"
    ENCRYPTED = "encrypted"
    PARTIALLY_ENCRYPTED = "encrypted-partial"


class EncryptableFieldTypes(str, Enum):
    STRING = "__encrypted_str__"


class EncryptedStrField(BaseModel):
    """Mark a string field for partial encryption in workflow payloads."""

    field_type: Literal[EncryptableFieldTypes.STRING] = EncryptableFieldTypes.STRING
    data: str


class WorkflowContext(BaseModel):
    namespace: str
    execution_id: str
    parent_workflow_exec_id: Optional[str] = None
    root_workflow_exec_id: Optional[str] = None
    execution_token: Optional[str] = None


class EncodedPayload(BaseModel):
    context: WorkflowContext
    encoding_options: list[EncodedPayloadOptions] = Field(
        description="The encoding of the payload", default=[]
    )
    payload: bytes = Field(description="The encoded payload")


class NetworkEncodedBase(BaseModel):
    b64payload: str = Field(description="The encoded payload")
    encoding_options: list[EncodedPayloadOptions] = Field(
        description="The encoding of the payload", default=[]
    )

    def get_payload(self) -> bytes:
        return base64.b64decode(self.b64payload)


class NetworkEncodedInput(NetworkEncodedBase):
    empty: bool = Field(description="Whether the payload is empty", default=False)

    def to_encoded_payload(
        self, namespace: str, execution_id: str, execution_token: str | None = None
    ) -> EncodedPayload:
        return EncodedPayload(
            payload=base64.b64decode(self.b64payload),
            encoding_options=self.encoding_options,
            context=WorkflowContext(
                namespace=namespace,
                execution_id=execution_id,
                execution_token=execution_token,
            ),
        )

    @staticmethod
    def from_encoded_payload(encoded_payload: EncodedPayload) -> "NetworkEncodedInput":
        return NetworkEncodedInput(
            b64payload=base64.b64encode(encoded_payload.payload).decode("utf-8"),
            encoding_options=encoded_payload.encoding_options,
        )

    @staticmethod
    def from_data(
        data: bytes, encoding_options: list[EncodedPayloadOptions]
    ) -> "NetworkEncodedInput":
        return NetworkEncodedInput(
            b64payload=base64.b64encode(data).decode("utf-8"),
            encoding_options=encoding_options,
        )


class NetworkEncodedResult(NetworkEncodedBase):
    @staticmethod
    def from_encoded_payload(encoded_payload: EncodedPayload) -> "NetworkEncodedResult":
        return NetworkEncodedResult(
            b64payload=base64.b64encode(encoded_payload.payload).decode("utf-8"),
            encoding_options=encoded_payload.encoding_options,
        )
