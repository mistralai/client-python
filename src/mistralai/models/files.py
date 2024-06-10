from typing import Literal, Optional

from mistralai.models.base_model import BackwardCompatibleBaseModel


class FileObject(BackwardCompatibleBaseModel):
    id: str
    object: str
    bytes: int
    created_at: int
    filename: str
    purpose: Optional[Literal["fine-tune"]] = "fine-tune"


class FileDeleted(BackwardCompatibleBaseModel):
    id: str
    object: str
    deleted: bool


class Files(BackwardCompatibleBaseModel):
    data: list[FileObject]
    object: Literal["list"]
