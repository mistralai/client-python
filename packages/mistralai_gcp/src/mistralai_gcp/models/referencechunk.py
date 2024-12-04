"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mistralai_gcp.types import BaseModel
from typing import List, Literal, Optional
from typing_extensions import NotRequired, TypedDict


ReferenceChunkType = Literal["reference"]


class ReferenceChunkTypedDict(TypedDict):
    reference_ids: List[int]
    type: NotRequired[ReferenceChunkType]


class ReferenceChunk(BaseModel):
    reference_ids: List[int]

    type: Optional[ReferenceChunkType] = "reference"
