from typing import Optional

from pydantic import BaseModel


class UsageInfo(BaseModel):
    prompt_tokens: int
    total_tokens: int
    completion_tokens: Optional[int]
