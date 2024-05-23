from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from mistralai.models.common import UsageInfo


class Function(BaseModel):
    name: str
    description: str
    parameters: dict


class ToolType(str, Enum):
    function = "function"


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
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


class ResponseFormat(BaseModel):
    type: ResponseFormats = ResponseFormats.text


class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[str]]
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class DeltaMessage(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class FinishReason(str, Enum):
    stop = "stop"
    length = "length"
    error = "error"
    tool_calls = "tool_calls"


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
