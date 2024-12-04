"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .textchunk import TextChunk, TextChunkTypedDict
from mistralai.types import BaseModel
from typing import List, Literal, Optional, Union
from typing_extensions import NotRequired, TypeAliasType, TypedDict


SystemMessageContentTypedDict = TypeAliasType(
    "SystemMessageContentTypedDict", Union[str, List[TextChunkTypedDict]]
)


SystemMessageContent = TypeAliasType(
    "SystemMessageContent", Union[str, List[TextChunk]]
)


Role = Literal["system"]


class SystemMessageTypedDict(TypedDict):
    content: SystemMessageContentTypedDict
    role: NotRequired[Role]


class SystemMessage(BaseModel):
    content: SystemMessageContent

    role: Optional[Role] = "system"
