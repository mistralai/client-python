"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .assistantmessage import AssistantMessage, AssistantMessageTypedDict
from .responseformat import ResponseFormat, ResponseFormatTypedDict
from .systemmessage import SystemMessage, SystemMessageTypedDict
from .tool import Tool, ToolTypedDict
from .toolchoice import ToolChoice, ToolChoiceTypedDict
from .toolchoiceenum import ToolChoiceEnum
from .toolmessage import ToolMessage, ToolMessageTypedDict
from .usermessage import UserMessage, UserMessageTypedDict
from mistralai.types import BaseModel, Nullable, OptionalNullable, UNSET, UNSET_SENTINEL
from mistralai.utils import get_discriminator
from pydantic import Discriminator, Tag, model_serializer
from typing import List, Optional, Union
from typing_extensions import Annotated, NotRequired, TypeAliasType, TypedDict


AgentsCompletionRequestStopTypedDict = TypeAliasType(
    "AgentsCompletionRequestStopTypedDict", Union[str, List[str]]
)
r"""Stop generation if this token is detected. Or if one of these tokens is detected when providing an array"""


AgentsCompletionRequestStop = TypeAliasType(
    "AgentsCompletionRequestStop", Union[str, List[str]]
)
r"""Stop generation if this token is detected. Or if one of these tokens is detected when providing an array"""


AgentsCompletionRequestMessagesTypedDict = TypeAliasType(
    "AgentsCompletionRequestMessagesTypedDict",
    Union[
        SystemMessageTypedDict,
        UserMessageTypedDict,
        AssistantMessageTypedDict,
        ToolMessageTypedDict,
    ],
)


AgentsCompletionRequestMessages = Annotated[
    Union[
        Annotated[AssistantMessage, Tag("assistant")],
        Annotated[SystemMessage, Tag("system")],
        Annotated[ToolMessage, Tag("tool")],
        Annotated[UserMessage, Tag("user")],
    ],
    Discriminator(lambda m: get_discriminator(m, "role", "role")),
]


AgentsCompletionRequestToolChoiceTypedDict = TypeAliasType(
    "AgentsCompletionRequestToolChoiceTypedDict",
    Union[ToolChoiceTypedDict, ToolChoiceEnum],
)


AgentsCompletionRequestToolChoice = TypeAliasType(
    "AgentsCompletionRequestToolChoice", Union[ToolChoice, ToolChoiceEnum]
)


class AgentsCompletionRequestTypedDict(TypedDict):
    messages: List[AgentsCompletionRequestMessagesTypedDict]
    r"""The prompt(s) to generate completions for, encoded as a list of dict with role and content."""
    agent_id: str
    r"""The ID of the agent to use for this completion."""
    max_tokens: NotRequired[Nullable[int]]
    r"""The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length."""
    stream: NotRequired[bool]
    r"""Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON."""
    stop: NotRequired[AgentsCompletionRequestStopTypedDict]
    r"""Stop generation if this token is detected. Or if one of these tokens is detected when providing an array"""
    random_seed: NotRequired[Nullable[int]]
    r"""The seed to use for random sampling. If set, different calls will generate deterministic results."""
    response_format: NotRequired[ResponseFormatTypedDict]
    tools: NotRequired[Nullable[List[ToolTypedDict]]]
    tool_choice: NotRequired[AgentsCompletionRequestToolChoiceTypedDict]
    presence_penalty: NotRequired[float]
    r"""presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative."""
    frequency_penalty: NotRequired[float]
    r"""frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition."""
    n: NotRequired[Nullable[int]]
    r"""Number of completions to return for each request, input tokens are only billed once."""


class AgentsCompletionRequest(BaseModel):
    messages: List[AgentsCompletionRequestMessages]
    r"""The prompt(s) to generate completions for, encoded as a list of dict with role and content."""

    agent_id: str
    r"""The ID of the agent to use for this completion."""

    max_tokens: OptionalNullable[int] = UNSET
    r"""The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length."""

    stream: Optional[bool] = False
    r"""Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: [DONE] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON."""

    stop: Optional[AgentsCompletionRequestStop] = None
    r"""Stop generation if this token is detected. Or if one of these tokens is detected when providing an array"""

    random_seed: OptionalNullable[int] = UNSET
    r"""The seed to use for random sampling. If set, different calls will generate deterministic results."""

    response_format: Optional[ResponseFormat] = None

    tools: OptionalNullable[List[Tool]] = UNSET

    tool_choice: Optional[AgentsCompletionRequestToolChoice] = None

    presence_penalty: Optional[float] = None
    r"""presence_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative."""

    frequency_penalty: Optional[float] = None
    r"""frequency_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition."""

    n: OptionalNullable[int] = UNSET
    r"""Number of completions to return for each request, input tokens are only billed once."""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "max_tokens",
            "stream",
            "stop",
            "random_seed",
            "response_format",
            "tools",
            "tool_choice",
            "presence_penalty",
            "frequency_penalty",
            "n",
        ]
        nullable_fields = ["max_tokens", "random_seed", "tools", "n"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)
            serialized.pop(k, None)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
