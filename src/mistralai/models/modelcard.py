"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .modelcapabilities import ModelCapabilities, ModelCapabilitiesTypedDict
from datetime import datetime
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from pydantic import model_serializer
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class ModelCardTypedDict(TypedDict):
    id: str
    capabilities: ModelCapabilitiesTypedDict
    object: NotRequired[str]
    created: NotRequired[int]
    owned_by: NotRequired[str]
    root: NotRequired[Nullable[str]]
    archived: NotRequired[bool]
    name: NotRequired[Nullable[str]]
    description: NotRequired[Nullable[str]]
    max_context_length: NotRequired[int]
    aliases: NotRequired[List[str]]
    deprecation: NotRequired[Nullable[datetime]]
    

class ModelCard(BaseModel):
    id: str
    capabilities: ModelCapabilities
    object: Optional[str] = "model"
    created: Optional[int] = None
    owned_by: Optional[str] = "mistralai"
    root: OptionalNullable[str] = UNSET
    archived: Optional[bool] = False
    name: OptionalNullable[str] = UNSET
    description: OptionalNullable[str] = UNSET
    max_context_length: Optional[int] = 32768
    aliases: Optional[List[str]] = None
    deprecation: OptionalNullable[datetime] = UNSET
    
    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["object", "created", "owned_by", "root", "archived", "name", "description", "max_context_length", "aliases", "deprecation"]
        nullable_fields = ["root", "name", "description", "deprecation"]
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
        
