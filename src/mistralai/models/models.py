from typing import List, Optional

from mistralai.models.base_model import BackwardCompatibleBaseModel


class ModelPermission(BackwardCompatibleBaseModel):
    id: str
    object: str
    created: int
    allow_create_engine: Optional[bool] = False
    allow_sampling: bool = True
    allow_logprobs: bool = True
    allow_search_indices: Optional[bool] = False
    allow_view: bool = True
    allow_fine_tuning: bool = False
    organization: str = "*"
    group: Optional[str] = None
    is_blocking: Optional[bool] = False


class ModelCard(BackwardCompatibleBaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    root: Optional[str] = None
    parent: Optional[str] = None
    permission: List[ModelPermission] = []


class ModelList(BackwardCompatibleBaseModel):
    object: str
    data: List[ModelCard]
