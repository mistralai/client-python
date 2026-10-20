from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from itertools import chain
from typing import TYPE_CHECKING, Any, Optional, Union, cast

from mistralai.client import models, utils
from mistralai.client.types import OptionalNullable, UNSET
from mistralai.client.types.basemodel import Unset

from .audio import AudioInterface
from .errors import (
    VoiceAgentConfigurationError,
    VoiceAgentConnectionError,
    VoiceAgentError,
)
from .session import VoiceAgentSession
from .tools import FunctionHandler, VoiceAgentTool

if TYPE_CHECKING:
    from mistralai.client.audio_sessions import AudioSessions

ToolDeclaration = Union[
    models.WebSearchTool,
    models.DocumentLibraryTool,
    models.CustomConnector,
    models.FunctionTool,
    models.TransferCallTool,
    models.HangUpTool,
    VoiceAgentTool,
    dict[str, Any],
]

async def init(
    sessions: AudioSessions,
    *,
    llm: Optional[Union[models.AudioLLMConfig, models.AudioLLMConfigTypedDict]] = None,
    tts: Optional[Union[models.AudioTTSConfig, models.AudioTTSConfigTypedDict]] = None,
    stt: Optional[Union[models.AudioSTTConfig, models.AudioSTTConfigTypedDict]] = None,
    turn: Optional[Union[models.AudioTurnConfig, models.AudioTurnConfigTypedDict]] = None,
    instructions: OptionalNullable[str] = UNSET,
    tools: OptionalNullable[Iterable[Union[ToolDeclaration, FunctionHandler]]] = UNSET,
    function_handlers: OptionalNullable[Iterable[Union[FunctionHandler, Callable[..., Any]]]] = UNSET,
    welcome_message: OptionalNullable[str] = UNSET,
    agent_id: OptionalNullable[str] = UNSET,
    agent_version: OptionalNullable[int] = UNSET,
    audio_interface: Optional[AudioInterface] = None,
    retries: OptionalNullable[utils.RetryConfig] = UNSET,
    server_url: Optional[str] = None,
    timeout_ms: Optional[int] = None,
    http_headers: Optional[Mapping[str, str]] = None,
) -> VoiceAgentSession:
    """Create the remote session and return it ready to connect().

    The session's room and agent exist from here on: register callbacks, then
    call `await session.connect()` (or enter `async with session`) within the
    session's join window. Call `await session.close()` to give it up without connecting.

    tools controls the full remote declaration list: UNSET inherits it,
    None/[] clears it, and a nonempty iterable replaces it. function_handlers
    registers local handlers only and never changes remote configuration.
    A decorated FunctionHandler in tools submits its declaration and also
    registers its handler, without needing a separate function_handlers entry.
    connect() checks the handlers against the session's function tools.
    """
    declared_handlers: list[FunctionHandler] = []
    if isinstance(tools, Unset):
        declarations: list[dict[str, Any]] | Unset = UNSET
    else:
        declarations = []
        for tool in tools or []:
            if isinstance(tool, FunctionHandler):
                declarations.append(tool.to_wire())
                declared_handlers.append(tool)
                continue
            wrapper = (
                tool if isinstance(tool, VoiceAgentTool)
                else VoiceAgentTool.model_validate(tool)
            )
            declarations.append(wrapper.to_wire())

    # Merge inline and handler-only registrations. Only tools= declarations
    # are sent; function_handlers= never contributes schemas or voice options.
    # Repeating the same callable is harmless; conflicting handlers are not.
    by_name: dict[str, FunctionHandler] = {}
    for handler in chain(declared_handlers, [] if isinstance(function_handlers, Unset) else function_handlers or []):
        if isinstance(handler, FunctionHandler):
            local_tool = handler
        elif callable(handler):
            local_tool = FunctionHandler(handler)
        else:
            raise VoiceAgentConfigurationError(
                "function_handlers must contain callables or @function_tool handlers"
            )
        if by_name.setdefault(local_tool.name, local_tool).fn is not local_tool.fn:
            raise VoiceAgentConfigurationError(
                f"Different handlers registered for function `{local_tool.name}`"
            )
    handlers = list(by_name.values())
    if not isinstance(agent_version, Unset) and agent_version is not None:
        if isinstance(agent_id, Unset) or agent_id is None:
            raise VoiceAgentConfigurationError("agent_version requires agent_id")
        if agent_version < 1:
            raise VoiceAgentConfigurationError("agent_version must be positive")

    # Fail on a missing microphone or transport extra before allocating a room.
    if audio_interface is not None:
        try:
            await audio_interface.preflight()
        except VoiceAgentError:
            raise
        except Exception as exc:
            raise VoiceAgentConnectionError(f"Audio interface is unavailable: {exc}") from exc
    from . import transport  # noqa: F401  # pylint: disable=import-outside-toplevel,unused-import

    options: dict[str, Any] = dict(
        retries=retries, server_url=server_url, timeout_ms=timeout_ms,
        http_headers=dict(http_headers) if http_headers is not None else None,
    )

    async def delete_remote_session(session_id: str) -> None:
        await sessions.close_async(session_id=session_id, **options)

    response = await sessions.create_async(
        llm=llm, tts=tts, stt=stt, turn=turn, instructions=instructions,
        tools=cast(Any, declarations), welcome_message=welcome_message,
        agent_id=agent_id, agent_version=agent_version, **options,
    )
    return VoiceAgentSession(
        response, delete_remote_session=delete_remote_session,
        audio_interface=audio_interface, function_handlers=handlers,
    )

