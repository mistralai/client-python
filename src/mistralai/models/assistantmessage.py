"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .toolcall import ToolCall, ToolCallTypedDict
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
import pydantic
from pydantic import model_serializer
from typing import Final, List, Literal, Optional, TypedDict
from typing_extensions import Annotated, NotRequired


AssistantMessageRole = Literal["assistant"]

class AssistantMessageTypedDict(TypedDict):
    content: NotRequired[Nullable[str]]
    tool_calls: NotRequired[Nullable[List[ToolCallTypedDict]]]
    prefix: NotRequired[bool]
    r"""Set this to `true` when adding an assistant message as prefix to condition the model response. The role of the prefix message is to force the model to start its answer by the content of the message."""
    

class AssistantMessage(BaseModel):
    ROLE: Annotated[Final[Optional[AssistantMessageRole]], pydantic.Field(alias="role")] = "assistant" # type: ignore
    content: OptionalNullable[str] = UNSET
    tool_calls: OptionalNullable[List[ToolCall]] = UNSET
    prefix: Optional[bool] = False
    r"""Set this to `true` when adding an assistant message as prefix to condition the model response. The role of the prefix message is to force the model to start its answer by the content of the message."""
    
    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["role", "content", "tool_calls", "prefix"]
        nullable_fields = ["content", "tool_calls"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (self.__pydantic_fields_set__.intersection({n}) or k in null_default_fields) # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
        
