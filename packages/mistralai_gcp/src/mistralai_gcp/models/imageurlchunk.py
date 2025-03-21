"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .imageurl import ImageURL, ImageURLTypedDict
from mistralai_gcp.types import BaseModel
from typing import Literal, Optional, Union
from typing_extensions import NotRequired, TypeAliasType, TypedDict


ImageURLChunkImageURLTypedDict = TypeAliasType(
    "ImageURLChunkImageURLTypedDict", Union[ImageURLTypedDict, str]
)


ImageURLChunkImageURL = TypeAliasType("ImageURLChunkImageURL", Union[ImageURL, str])


ImageURLChunkType = Literal["image_url"]


class ImageURLChunkTypedDict(TypedDict):
    r"""{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,iVBORw0"""

    image_url: ImageURLChunkImageURLTypedDict
    type: NotRequired[ImageURLChunkType]


class ImageURLChunk(BaseModel):
    r"""{\"type\":\"image_url\",\"image_url\":{\"url\":\"data:image/png;base64,iVBORw0"""

    image_url: ImageURLChunkImageURL

    type: Optional[ImageURLChunkType] = "image_url"
