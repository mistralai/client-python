"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .textchunk import TextChunk, TextChunkTypedDict
from mistralai_gcp.types import BaseModel
import pydantic
from typing import Final, List, Literal, Optional, TypedDict, Union
from typing_extensions import Annotated


Role = Literal["system"]

ContentTypedDict = Union[str, List[TextChunkTypedDict]]


Content = Union[str, List[TextChunk]]


class SystemMessageTypedDict(TypedDict):
    content: ContentTypedDict
    

class SystemMessage(BaseModel):
    content: Content
    ROLE: Annotated[Final[Optional[Role]], pydantic.Field(alias="role")] = "system" # type: ignore
    
