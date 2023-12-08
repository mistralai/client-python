from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from mistralai.models.common import UsageInfo


class ChatMessage(BaseModel):
    role: str
    content: str


class DeltaMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class FinishReason(Enum):
    stop = "stop"
    length = "length"


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[FinishReason]


class ChatCompletionStreamResponse(BaseModel):
    id: str
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    created: Optional[int] = None
    object: Optional[str] = None
    usage: Optional[UsageInfo] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[FinishReason]


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
