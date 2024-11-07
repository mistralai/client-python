"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .deltamessage import DeltaMessage, DeltaMessageTypedDict
from mistralai_gcp.types import BaseModel, Nullable, UNSET_SENTINEL, UnrecognizedStr
from mistralai_gcp.utils import validate_open_enum
from pydantic import model_serializer
from pydantic.functional_validators import PlainValidator
from typing import Literal, Union
from typing_extensions import Annotated, TypedDict


FinishReason = Union[Literal["stop", "length", "error", "tool_calls"], UnrecognizedStr]


class CompletionResponseStreamChoiceTypedDict(TypedDict):
    index: int
    delta: DeltaMessageTypedDict
    finish_reason: Nullable[FinishReason]


class CompletionResponseStreamChoice(BaseModel):
    index: int

    delta: DeltaMessage

    finish_reason: Annotated[
        Nullable[FinishReason], PlainValidator(validate_open_enum(False))
    ]

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = []
        nullable_fields = ["finish_reason"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
