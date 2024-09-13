"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mistralai.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class TrainingFileTypedDict(TypedDict):
    file_id: str
    weight: NotRequired[float]


class TrainingFile(BaseModel):
    file_id: str

    weight: Optional[float] = 1
