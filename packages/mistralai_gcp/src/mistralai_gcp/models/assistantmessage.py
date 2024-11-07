"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .contentchunk import ContentChunk, ContentChunkTypedDict
from .toolcall import ToolCall, ToolCallTypedDict
from mistralai_gcp.types import (
    BaseModel,
    Nullable,
    OptionalNullable,
    UNSET,
    UNSET_SENTINEL,
)
from pydantic import model_serializer
from typing import List, Literal, Optional, Union
from typing_extensions import NotRequired, TypedDict


AssistantMessageContentTypedDict = Union[str, List[ContentChunkTypedDict]]


AssistantMessageContent = Union[str, List[ContentChunk]]


AssistantMessageRole = Literal["assistant"]


class AssistantMessageTypedDict(TypedDict):
    content: NotRequired[Nullable[AssistantMessageContentTypedDict]]
    tool_calls: NotRequired[Nullable[List[ToolCallTypedDict]]]
    prefix: NotRequired[bool]
    role: NotRequired[AssistantMessageRole]


class AssistantMessage(BaseModel):
    content: OptionalNullable[AssistantMessageContent] = UNSET

    tool_calls: OptionalNullable[List[ToolCall]] = UNSET

    prefix: Optional[bool] = False

    role: Optional[AssistantMessageRole] = "assistant"

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["content", "tool_calls", "prefix", "role"]
        nullable_fields = ["content", "tool_calls"]
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
