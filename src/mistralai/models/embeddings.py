from typing import List

from mistralai.models.base_model import BackwardCompatibleBaseModel
from mistralai.models.common import UsageInfo


class EmbeddingObject(BackwardCompatibleBaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingResponse(BackwardCompatibleBaseModel):
    id: str
    object: str
    data: List[EmbeddingObject]
    model: str
    usage: UsageInfo
