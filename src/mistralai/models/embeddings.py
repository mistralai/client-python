from typing import List

from pydantic import BaseModel

from mistralai.models.common import UsageInfo


class EmbeddingObject(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingResponse(BaseModel):
    id: str
    object: str
    data: List[EmbeddingObject]
    model: str
    usage: UsageInfo
