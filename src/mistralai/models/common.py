from typing import Optional

from mistralai.models.base_model import BackwardCompatibleBaseModel


class UsageInfo(BackwardCompatibleBaseModel):
    prompt_tokens: int
    total_tokens: int
    completion_tokens: Optional[int]
