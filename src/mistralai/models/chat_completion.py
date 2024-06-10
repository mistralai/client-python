from enum import Enum
from typing import List, Optional

from mistralai.models.base_model import BackwardCompatibleBaseModel
from mistralai.models.common import UsageInfo


class Function(BackwardCompatibleBaseModel):
    name: str
    description: str
    parameters: dict


class ToolType(str, Enum):
    function = "function"


class FunctionCall(BackwardCompatibleBaseModel):
    name: str
    arguments: str


class ToolCall(BackwardCompatibleBaseModel):
    id: str = "null"
    type: ToolType = ToolType.function
    function: FunctionCall


class ResponseFormats(str, Enum):
    text: str = "text"
    json_object: str = "json_object"


class ToolChoice(str, Enum):
    auto: str = "auto"
    any: str = "any"
    none: str = "none"


class ResponseFormat(BackwardCompatibleBaseModel):
    type: ResponseFormats = ResponseFormats.text


class ChatMessage(BackwardCompatibleBaseModel):
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class DeltaMessage(BackwardCompatibleBaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class FinishReason(str, Enum):
    stop = "stop"
    length = "length"
    error = "error"
    tool_calls = "tool_calls"


class ChatCompletionResponseStreamChoice(BackwardCompatibleBaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[FinishReason]


class ChatCompletionStreamResponse(BackwardCompatibleBaseModel):
    id: str
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    created: Optional[int] = None
    object: Optional[str] = None
    usage: Optional[UsageInfo] = None


class ChatCompletionResponseChoice(BackwardCompatibleBaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[FinishReason]


class ChatCompletionResponse(BackwardCompatibleBaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
