"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .jsonschema import JSONSchema, JSONSchemaTypedDict
from .responseformats import ResponseFormats
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from pydantic import model_serializer
from typing import Optional
from typing_extensions import NotRequired, TypedDict


class ResponseFormatTypedDict(TypedDict):
    type: NotRequired[ResponseFormats]
    r"""An object specifying the format that the model must output. Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which guarantees the message the model generates is in JSON. When using JSON mode you MUST also instruct the model to produce JSON yourself with a system or a user message."""
    json_schema: NotRequired[Nullable[JSONSchemaTypedDict]]


class ResponseFormat(BaseModel):
    type: Optional[ResponseFormats] = None
    r"""An object specifying the format that the model must output. Setting to `{ \"type\": \"json_object\" }` enables JSON mode, which guarantees the message the model generates is in JSON. When using JSON mode you MUST also instruct the model to produce JSON yourself with a system or a user message."""

    json_schema: OptionalNullable[JSONSchema] = UNSET

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["type", "json_schema"]
        nullable_fields = ["json_schema"]
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
