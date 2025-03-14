"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from mistralai_azure.types import BaseModel
from typing import Any, Dict, Optional
from typing_extensions import NotRequired, TypedDict


class FunctionTypedDict(TypedDict):
    name: str
    parameters: Dict[str, Any]
    description: NotRequired[str]
    strict: NotRequired[bool]


class Function(BaseModel):
    name: str

    parameters: Dict[str, Any]

    description: Optional[str] = ""

    strict: Optional[bool] = False
