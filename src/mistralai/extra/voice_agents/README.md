# Voice agents in the main Python SDK

Install `mistralai[voice-agents]`; the single extra pulls in everything needed to
stream live audio. System audio requires PortAudio (`brew install portaudio` on macOS).
No separate `mistralai-voice-agents` package is needed.

```python
import asyncio
from mistralai.client import Mistral
from mistralai.client.models import WebSearchTool
from mistralai.extra.voice_agents import DefaultAudioInterface, function_tool

@function_tool(filler={"text": "Let me check."}, timeout_ms=15000)
async def lookup(query: str) -> str:
    """Look up a query in the application's data."""
    return query

async def main():
    async with Mistral() as client:
        session = await client.audio.sessions.init(
            tools=[WebSearchTool(), lookup],
            audio_interface=DefaultAudioInterface(),
        )
        session.on("connected", lambda event: print(event.session_id))
        session.on("transcript", lambda event: print(event.role, event.content))
        session.on("error", lambda event: print(event.model_dump_json()))
        async with session:  # Calls await session.connect(), closes on exit.
            await session.wait()

asyncio.run(main())
```

`init()` creates the remote session and returns a `VoiceAgentSession`; it does not
join the room or open audio. Register callbacks, then call `await session.connect()`
or enter `async with session` within the session's join window. Call
`await session.close()` to give up a session without connecting; it still deletes
the remote session. The generated `create[_async]`, `get[_async]` and
`close[_async]` REST methods remain on `client.audio.sessions`.

A missing audio device or a missing extra fails `init()` before any session is
created. A rejected join (for example an expired participant token) raises
`VoiceAgentConnectionError` from `connect()`.

Repeated connect/close calls are idempotent, but a closed session cannot reconnect.
Startup failures close the session and raise directly. Nonfatal errors notify the
`error` callback; fatal errors also close the session and raise through `wait()`.
Cleanup errors are reported as nonfatal `error` events and do not replace the
original failure.

## Tool declarations versus executable function handlers

`tools` controls remote declarations for **all** tool kinds, including functions.
Use `WebSearchTool`, `DocumentLibraryTool`, `CustomConnector`, and `FunctionTool`
from `mistralai.extra.voice_agents`. `VoiceAgentTool(tool=..., filler=...)` adds voice
options and serializes to the flat wire shape. Dictionary declarations also work.

`function_handlers` attaches **handlers only**, matched by name. It accepts decorated
`FunctionHandler` objects or plain named Python functions, and never sends definitions,
fillers, or timeouts to the backend. Changing this list, including passing `None`
or `[]`, does not override or remove remotely declared tools.

For an inline function, pass the decorated tool directly to submit its declaration
and register its handler together:

```python
session = await client.audio.sessions.init(
    tools=[WebSearchTool(), lookup],
)
```

For a saved agent that already declares `lookup`, attach only the handler:

```python
session = await client.audio.sessions.init(
    agent_id="...",
    function_handlers=[lookup],
)
```

| Input | `tools` | `function_handlers` |
| --- | --- | --- |
| omitted | Inherit the complete saved tools list (`UNSET`) | No additional handlers; decorated tools still register theirs |
| `None` / `[]` | Clear the complete remote tools list | No additional handlers; remote tools unchanged |
| Nonempty iterable | Replace the complete remote tools list | Register handlers only; remote tools unchanged |

A `FunctionTool` model or dictionary in `tools` is a declaration only. A decorated
`FunctionHandler` in `tools` submits its declaration (including filler and timeout) and
registers its handler. An undecorated callable belongs only in `function_handlers`.
Handlers from both parameters are merged by name: two different handlers with the
same name raise before the session is created; repeating the same callable is allowed.
Metadata on handlers supplied only through `function_handlers` does not replace the
remote schema or voice options. Local invocation validates arguments against the
Python callable's signature.

`connect()` validates local handlers against the effective function declarations
returned by REST creation; it does not fetch agents or reconstruct overrides.
An argument-name mismatch raises `VoiceAgentConfigurationError` and closes the
session. Missing handlers and handlers without declarations emit
`VoiceAgentErrorEvent(code="function_handler_configuration_error", fatal=False)`
and the session still connects; register an `error` callback before `connect()`
to observe them. `**kwargs` handlers accept and retain additional named arguments. Per-call argument validation still applies; unmatched function
invocations emit `unhandled_tool` and return a failed RPC. Change remote schemas,
fillers, or timeouts through agent CRUD or an explicit declaration in `tools`.

TransferCallTool and HangUpTool use VoiceAgentTool for fillers and are SIP-only.

## Migrating from the standalone Python package

- Replace `MistralVoiceAgent` with `Mistral`; use the main SDK's authentication,
  HTTP clients, server configuration, and retry settings.
- Replace `await client.connect(...)` with
  `session = await client.audio.sessions.init(...)`, attach callbacks, then
  `await session.connect()` or `async with session`.
- Move imports from `mistralai.voice.agents` to `mistralai.extra.voice_agents`.
  Backend messages and shared tool declarations come from `mistralai.client.models`.
- `VoiceSession` becomes `VoiceAgentSession`. The transport classes moved to
  `mistralai.extra.voice_agents.transport`; applications should not reference them
  directly.
- `client.audio.sessions.create[_async]` is the generated REST call and returns
  connection credentials only; use `init()` for a live session.
- Omitted/`UNSET` `tools` inherits; explicit `None` or `[]` clears the whole tools
  list, consistent with generated nullable input semantics. `function_handlers` is
  handler-only; omitted/`UNSET`/`None`/`[]` attaches no additional handlers.
- Replace old agent version helpers with the generated CRUD/version routes below.
  The standalone package's `VoiceAgentAPIError` is replaced by main SDK REST errors.
- Custom worker helpers remain available but their `livekit-agents` dependency
  must be installed separately. The old standalone release workflows are retired;
  voice runtime changes now ship with the main SDK.

## Saved agents and versions

`client.audio.agents` is generated from the current backend routes:

```python
agent = await client.audio.agents.create_async(
    name="Support bot",
    configuration={"instructions": "Be helpful.", "tools": [lookup.to_wire()]},
)
selected = await client.audio.agents.get_async(agent_id=agent.id, version=1)
updated = await client.audio.agents.update_async(
    agent_id=agent.id,
    name="Support bot",
    configuration={"instructions": "Be concise.", "tools": [lookup.to_wire()]},
)
versions = await client.audio.agents.list_versions_async(agent_id=agent.id)
session = await client.audio.sessions.init(
    agent_id=agent.id, agent_version=updated.version, function_handlers=[lookup],
)
```

Updating uses **PUT** with a name and full configuration. There is no
`create_version()` or `get_version()` helper: use `update[_async]()` and
`get[_async](version=...)`. Version lists use the generated paginated response.
`client.audio.sessions.get[_async](session_id=...)` returns the backend snapshot,
not a live runtime. `close[_async](session_id=...)` performs remote REST deletion;
`session.close()` additionally stops that runtime's local resources.

## Events and manual audio

The six `VoiceAgent*Event` models are generated in `mistralai.client.models` and
re-exported from `mistralai.extra.voice_agents`. The unified `VoiceAgentErrorEvent`
is used for both remote and local errors. Connected/disconnected, unhandled tools,
unknown packets, event unions and transport abstractions remain handwritten.

Assistant transcript updates follow worker audio playout and interruptions.
Updates sharing an `id` replace previous text; `final` completes a segment.
`session.transcript` retains the latest segments after closure.

Omit `audio_interface` to manage 48 kHz mono signed 16-bit PCM yourself. Register
an `audio` callback and, after `await session.connect()`, call `session.send_audio()`.

Custom worker authentication is retained at
`mistralai.extra.voice_agents.worker`; install `livekit-agents` explicitly when
using that worker helper. It is not required for the client runtime.
