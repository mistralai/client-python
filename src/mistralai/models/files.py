from typing import Literal, Optional

from pydantic import BaseModel


class FileObject(BaseModel):
    id: str
    object: str
    bytes: int
    created_at: int
    filename: str
    purpose: Optional[Literal["fine-tune"]] = "fine-tune"


class FileDeleted(BaseModel):
    id: str
    object: str
    deleted: bool


class Files(BaseModel):
    data: list[FileObject]
    object: Literal["list"]
