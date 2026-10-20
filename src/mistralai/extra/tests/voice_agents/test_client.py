"""init(): wire declarations and local handlers into session creation."""
from datetime import datetime, timezone
from typing import Any, cast
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from mistralai.client.models import (
    AudioSessionCreateResponse,
    Function,
    FunctionTool,
    VoiceAgentFunctionTool,
    WebSearchTool,
)
from mistralai.client.types import UNSET
from mistralai.extra.voice_agents import (
    VoiceAgentConfigurationError,
    VoiceAgentConnectionError,
    VoiceAgentSession,
    VoiceAgentTool,
    function_tool,
)
from mistralai.extra.voice_agents.client import init as voice_init


@pytest.fixture
def rest():
    """Generated sessions client whose response echoes the effective function tools.

    Functions saved on an agent are listed in `rest.saved_functions`; tools=
    replaces them, as the backend does.
    """
    now = datetime.now(timezone.utc)
    rest = SimpleNamespace(saved_functions=[], close_async=AsyncMock())

    async def create_async(**request):
        tools = request["tools"]
        functions = rest.saved_functions if tools is UNSET else [
            VoiceAgentFunctionTool.model_validate(tool)
            for tool in tools or [] if tool.get("type") == "function"
        ]
        return AudioSessionCreateResponse(
            id="session", participant_token="token", server_url="ws://localhost",
            created_at=now, expires_at=now, function_tools=functions,
        )

    rest.create_async = AsyncMock(side_effect=create_async)
    return rest


@pytest.fixture
def handler():
    @function_tool(filler={"text": "Checking"}, timeout_ms=20000)
    async def lookup(query: str) -> str:
        """Look up a query."""
        return query

    return lookup


@pytest.fixture
def init(rest):
    async def init_session(**kwargs):
        return await voice_init(rest, **kwargs)

    return init_session


def saved(handler):
    return VoiceAgentFunctionTool.model_validate(handler.to_wire())


@pytest.mark.asyncio
async def test_init_creates_the_session_without_connecting(init, rest, handler):
    session = await init(tools=[{"type": "function", "function": {"name": "unhandled", "parameters": {}}}, handler])
    assert isinstance(session, VoiceAgentSession)
    assert session.id == "session"
    assert session._session_response.participant_token == "token"
    assert session._transport is None and not session._started
    rest.create_async.assert_awaited_once()
    rest.close_async.assert_not_awaited()  # handlers are checked at connect()
    assert session._function_handlers == [handler]


@pytest.mark.asyncio
@pytest.mark.parametrize("handlers", [None, [], "handler"])
async def test_handlers_only_do_not_override_saved_tools(init, rest, handler, handlers):
    rest.saved_functions = [saved(handler)] if handlers == "handler" else []
    local_handlers = [handler] if handlers == "handler" else handlers
    session = await init(agent_id="agent", function_handlers=local_handlers)
    request = rest.create_async.call_args.kwargs
    assert request["tools"] is UNSET
    assert request["agent_id"] == "agent"
    assert request["agent_version"] is UNSET
    assert "function_handlers" not in request
    assert session._function_handlers == ([handler] if handlers == "handler" else [])


@pytest.mark.asyncio
@pytest.mark.parametrize("declarations", [None, [], [WebSearchTool()]])
async def test_tools_retains_full_list_override_policy(init, rest, declarations):
    await init(agent_id="agent", tools=declarations)
    expected = [{"type": "web_search"}] if declarations else []
    assert rest.create_async.call_args.kwargs["tools"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("variant", ["model", "dict", "wrapper"])
async def test_function_declarations_belong_in_tools(init, rest, handler, variant):
    declaration = FunctionTool(function=Function(
        name="lookup", parameters={"type": "object", "properties": {"query": {"type": "string"}}},
    ))
    value = {
        "model": declaration,
        "dict": declaration.model_dump(mode="json"),
        "wrapper": VoiceAgentTool(tool=declaration, filler=cast(Any, {"text": "Remote filler"})),
    }[variant]
    await init(tools=[WebSearchTool(), value], function_handlers=[handler])
    actual = rest.create_async.call_args.kwargs["tools"]
    assert actual[0] == {"type": "web_search"}
    assert actual[1]["function"] == declaration.function.model_dump(mode="json")
    filler = {"type": "static", "text": "Remote filler"}
    assert actual[1].get("filler") == (filler if variant == "wrapper" else None)
    assert "timeout_ms" not in actual[1]


@pytest.mark.asyncio
async def test_handler_schema_and_options_do_not_replace_remote_declaration(init, rest, handler):
    declaration = {
        "type": "function",
        "function": {"name": handler.name, "parameters": {"type": "object", "properties": {"query": {}}}},
        "filler": {"type": "static", "text": "Server-owned filler"}, "timeout_ms": 45000,
    }
    await init(tools=[declaration], function_handlers=[handler])
    assert rest.create_async.call_args.kwargs["tools"] == [declaration]
    assert handler.filler.text == "Checking" and handler.timeout_ms == 20000


@pytest.mark.asyncio
async def test_handlers_are_never_serialized(init, rest, handler, monkeypatch):
    rest.saved_functions = [saved(handler)]
    monkeypatch.setattr(handler, "to_wire", Mock(side_effect=AssertionError("handler serialized")))
    await init(agent_id="agent", function_handlers=[handler])
    handler.to_wire.assert_not_called()
    assert rest.create_async.call_args.kwargs["tools"] is UNSET


@pytest.mark.asyncio
async def test_decorated_tool_submits_definition_and_registers_handler(init, rest, handler):
    session = await init(tools=[WebSearchTool(), handler])
    assert session._function_handlers == [handler]
    assert rest.create_async.call_args.kwargs["tools"] == [
        {"type": "web_search"}, handler.to_wire(),
    ]


@pytest.mark.asyncio
async def test_plain_callable_in_tools_requires_decorator(init, rest):
    def lookup(query: str) -> str:
        return query

    with pytest.raises(ValueError):
        await init(tools=[lookup])
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_conflicting_handlers_are_rejected(init, rest, handler):
    @function_tool(name=handler.name)
    async def other(query: str) -> str:
        return query

    with pytest.raises(VoiceAgentConfigurationError, match="Different handlers"):
        await init(function_handlers=[handler, other])
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_same_handler_repeated_is_accepted(init, rest, handler):
    rest.saved_functions = [saved(handler)]
    assert (await init(function_handlers=[handler, handler]))._function_handlers == [handler]
    assert (await init(function_handlers=[handler, handler.fn]))._function_handlers == [handler]


@pytest.mark.asyncio
async def test_plain_function_handler_is_registered_without_a_declaration(init, rest):
    async def lookup(query: str) -> str:
        return query.upper()

    rest.saved_functions = [VoiceAgentFunctionTool.model_validate({
        "function": {"name": "lookup", "parameters": {"type": "object", "properties": {"query": {}}}},
    })]
    session = await init(agent_id="agent", function_handlers=[lookup, lookup])
    assert rest.create_async.call_args.kwargs["tools"] is UNSET
    assert len(session._function_handlers) == 1
    tool = session._function_handlers[0]
    assert tool.name == "lookup" and tool.fn is lookup
    assert await tool.invoke('{"query":"hello"}') == "HELLO"


@pytest.mark.asyncio
@pytest.mark.parametrize("value", [{"type": "function"}, "not a handler"])
async def test_function_handlers_require_callables(init, rest, value):
    with pytest.raises(VoiceAgentConfigurationError, match="function_handlers"):
        await init(function_handlers=[value])
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_agent_version_is_forwarded_without_lookup_or_replacement(init, rest, handler):
    rest.saved_functions = [saved(handler)]
    await init(agent_id="agent", agent_version=3, function_handlers=[handler])
    request = rest.create_async.call_args.kwargs
    assert request["agent_version"] == 3
    assert request["tools"] is UNSET


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("kwargs", "message"),
    [({"agent_version": 3}, "requires agent_id"), ({"agent_id": "agent", "agent_version": 0}, "positive")],
)
async def test_invalid_agent_version_is_rejected_before_create(init, rest, kwargs, message):
    with pytest.raises(VoiceAgentConfigurationError, match=message):
        await init(**kwargs)
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_headers_are_snapshotted_for_create_and_close(init, rest):
    headers = {"x-workspace-id": "workspace"}
    session = await init(tools=[{"type": "web_search"}], http_headers=headers)
    headers["x-workspace-id"] = "changed"
    await session.close()
    for call in (rest.create_async.call_args, rest.close_async.call_args):
        assert call.kwargs["http_headers"] == {"x-workspace-id": "workspace"}
    assert rest.close_async.call_args.kwargs["session_id"] == "session"


@pytest.mark.asyncio
async def test_merges_handlers_from_both_parameters(init, rest, handler):
    @function_tool
    async def other(query: str) -> str:
        return query

    rest.saved_functions = [saved(handler), saved(other)]
    session = await init(tools=UNSET, function_handlers=[handler, other])
    assert session._function_handlers == [handler, other]


@pytest.mark.asyncio
@pytest.mark.parametrize("handler_only", ["decorated", "plain"])
async def test_same_inline_handler_can_also_be_attached(init, handler, handler_only):
    attached = handler if handler_only == "decorated" else handler.fn
    session = await init(tools=[handler], function_handlers=[attached])
    assert session._function_handlers == [handler]


@pytest.mark.asyncio
async def test_conflicting_handlers_across_parameters_are_rejected(init, rest, handler):
    @function_tool(name=handler.name)
    async def other(query: str) -> str:
        return query

    with pytest.raises(VoiceAgentConfigurationError, match="Different handlers"):
        await init(tools=[handler], function_handlers=[other])
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_inline_tool_iterable_is_consumed_once(init, rest, handler):
    session = await init(tools=iter([WebSearchTool(), handler]))
    assert session._function_handlers == [handler]
    assert rest.create_async.call_args.kwargs["tools"] == [
        {"type": "web_search"}, handler.to_wire(),
    ]


# Local preconditions fail before a session is created.
@pytest.mark.asyncio
async def test_audio_preflight_failure_does_not_create(init, rest):
    audio = AsyncMock()
    audio.preflight.side_effect = RuntimeError("microphone unavailable")
    with pytest.raises(VoiceAgentConnectionError, match="microphone unavailable"):
        await init(audio_interface=audio)
    rest.create_async.assert_not_awaited()


@pytest.mark.asyncio
async def test_missing_transport_dependencies_fail_before_create(init, rest, monkeypatch):
    import builtins

    original_import = builtins.__import__

    def without_transport(name, globals=None, locals=None, fromlist=(), level=0):
        if level == 1 and "transport" in (fromlist or ()):
            raise ImportError("LiveKit dependency unavailable")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", without_transport)
    with pytest.raises(ImportError, match="LiveKit dependency unavailable"):
        await init()
    rest.create_async.assert_not_awaited()


def test_audio_sessions_exposes_init_as_a_method():
    from mistralai.client import Mistral

    sessions = Mistral(api_key="key").audio.sessions
    assert sessions.init.__func__ is voice_init
    assert callable(sessions.create_async) and callable(sessions.close_async)
