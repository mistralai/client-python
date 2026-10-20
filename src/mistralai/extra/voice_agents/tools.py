from __future__ import annotations

import asyncio
import functools
import inspect
import json
from collections.abc import Callable
from typing import Annotated, Any

from mistralai.client.models import (
    HangUpTool,
    PhoneDestination,
    SipDestination,
    StaticToolFiller,
    TransferCallTool,
    TransferTarget,
    VoiceAgentErrorEvent,
    VoiceAgentFunctionTool,
)
from mistralai.client.models import (
    CustomConnector,
    DocumentLibraryTool,
    Function,
    FunctionTool,
    ToolConfiguration,
    WebSearchTool,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializationInfo,
    create_model,
    model_serializer,
    model_validator,
)

from .errors import VoiceAgentConfigurationError

__all__ = [
    "StaticToolFiller",
    "PhoneDestination",
    "SipDestination",
    "TransferTarget",
    "TransferCallTool",
    "HangUpTool",
    "FunctionHandler",
    "function_tool",
    "VoiceAgentTool",
    "WebSearchTool",
    "DocumentLibraryTool",
    "CustomConnector",
    "FunctionTool",
    "ToolConfiguration",
]


SharedTool = Annotated[
    WebSearchTool | DocumentLibraryTool | CustomConnector | FunctionTool,
    Field(discriminator="type"),
]


class VoiceAgentTool(BaseModel):
    """SDK convenience composition; the backend accepts only flat declarations.

    VoiceAgentTool(tool=WebSearchTool(), filler={"text": "Searching"})
    serializes as {"type": "web_search", "filler": {"type": "static", "text": "Searching"}}.
    The backend does not need another flattening adapter: its discriminated
    variants inherit the shared declaration schemas and add voice-only fields.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)
    tool: SharedTool | BaseModel
    filler: StaticToolFiller | None = None
    timeout_ms: int | None = Field(default=None, ge=1, le=4294967295)

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, value: Any) -> Any:
        if isinstance(value, BaseModel) and not isinstance(value, cls):
            value = {"tool": value}
        if not isinstance(value, dict):
            return value
        value = dict(value)
        if "tool" not in value:
            filler = value.pop("filler", None)
            timeout_ms = value.pop("timeout_ms", None)
            value = {"tool": value, "filler": filler, "timeout_ms": timeout_ms}
        declaration = value.get("tool")
        if isinstance(declaration, dict):
            # Main generated models ignore unknown fields. Validate keys here
            # so removed wait/filler fields cannot silently disappear.
            kind = declaration.get("type")
            classes: dict[str, type[BaseModel]] = {
                "web_search": WebSearchTool,
                "document_library": DocumentLibraryTool,
                "connector": CustomConnector,
                "function": FunctionTool,
            }
            cls_ = classes.get(kind) if isinstance(kind, str) else None
            if kind in {"transfer_call", "hang_up"}:
                cls_ = TransferCallTool if kind == "transfer_call" else HangUpTool
            if cls_ is None:
                raise ValueError(f"Unsupported voice tool type: {kind!r}")
            unknown = declaration.keys() - cls_.model_fields.keys()
            if unknown:
                raise ValueError(f"Unknown tool fields: {', '.join(sorted(unknown))}")
            value["tool"] = cls_.model_validate(declaration)
        elif not isinstance(
            declaration,
            (WebSearchTool, DocumentLibraryTool, CustomConnector, FunctionTool),
        ):
            if not isinstance(declaration, (TransferCallTool, HangUpTool)):
                raise ValueError("Unsupported voice tool declaration")
        return value

    @model_validator(mode="after")
    def _validate_timeout(self) -> "VoiceAgentTool":
        if self.timeout_ms is not None and not isinstance(self.tool, FunctionTool):
            raise ValueError("timeout_ms is only supported for function tools")
        return self

    @model_serializer(mode="plain")
    def _serialize(self, info: SerializationInfo) -> dict[str, Any]:
        payload = self.tool.model_dump(
            mode=info.mode,
            exclude_none=info.exclude_none,
            exclude_unset=info.exclude_unset,
            exclude_defaults=info.exclude_defaults,
        )
        payload["type"] = getattr(self.tool, "type")
        if self.filler is not None:
            payload["filler"] = self.filler.model_dump(
                mode=info.mode, exclude_none=info.exclude_none
            )
        elif (
            not info.exclude_none
            and not info.exclude_defaults
            and (not info.exclude_unset or "filler" in self.model_fields_set)
        ):
            payload["filler"] = None
        if self.timeout_ms is not None:
            payload["timeout_ms"] = self.timeout_ms
        return payload

    def to_wire(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)


# ── function handlers (executed locally over RPC) ──


class FunctionHandler:
    """A local function the voice agent can call.

    Carries both the declaration sent to the backend (``to_wire``) and the local
    handler invoked when the agent calls it (``invoke``), so the tool name the
    model calls and the handler that runs can never drift apart.

    Build these with the :func:`function_tool` decorator rather than directly.
    """

    def __init__(
        self,
        fn: Callable[..., Any],
        *,
        name: str | None = None,
        description: str | None = None,
        filler: StaticToolFiller | dict[str, Any] | None = None,
        timeout_ms: int = 15000,
    ) -> None:
        self.fn = fn
        self.name = name or fn.__name__
        self.description = description or inspect.getdoc(fn)
        self.filler = (
            StaticToolFiller.model_validate(filler) if filler is not None else None
        )
        self._args_model = _build_args_model(fn, self.name)
        self.parameters = self._args_model.model_json_schema()
        declaration = FunctionTool(
            function=Function(name=self.name, parameters=self.parameters)
        )
        self.timeout_ms = VoiceAgentTool(
            tool=declaration, timeout_ms=timeout_ms
        ).timeout_ms
        functools.update_wrapper(self, fn)

    def to_wire(self) -> dict[str, Any]:
        declaration = FunctionTool(
            function=Function(
                name=self.name,
                description=self.description,
                parameters=self.parameters,
            )
        )
        return VoiceAgentTool(
            tool=declaration, filler=self.filler, timeout_ms=self.timeout_ms
        ).to_wire()

    async def invoke(self, raw_arguments: str | None) -> str:
        """Validate JSON args, run the handler, return a string for the model."""
        args = json.loads(raw_arguments) if raw_arguments else {}
        validated = self._args_model.model_validate(args)
        kwargs = {
            field: getattr(validated, field) for field in self._args_model.model_fields
        }
        # Preserve named RPC arguments accepted by **kwargs, not just fields
        # explicitly present in the signature-derived model.
        kwargs.update(validated.model_extra or {})
        if inspect.iscoroutinefunction(self.fn):
            result = await self.fn(**kwargs)
        else:
            # Run sync handlers in a thread so a blocking call (time.sleep,
            # blocking I/O, ...) can't stall the event loop that pumps audio
            # and services RPC.
            result = await asyncio.to_thread(self.fn, **kwargs)
            if inspect.isawaitable(result):
                result = await result
        if result is None:
            return ""
        return result if isinstance(result, str) else json.dumps(result)

    def signature_mismatch(self, parameters: dict[str, Any]) -> str | None:
        """Compare argument names once at startup; this is not JSON Schema validation."""
        # Function.parameters is an arbitrary JSON Schema (worker/tools.py uses
        # it verbatim for the raw tool). Non-object schemas have no static names.
        properties = parameters.get("properties")
        if properties is not None and not isinstance(properties, dict):
            return None
        declared = set(properties or {})
        fields = self._args_model.model_fields
        accepts_kwargs = self._args_model.model_config.get("extra") == "allow"
        dropped = [] if accepts_kwargs else sorted(declared - fields.keys())
        missing = sorted(
            name
            for name, field in fields.items()
            if field.is_required() and name not in declared
        )
        problems = []
        if dropped:
            problems.append(f"does not accept {', '.join(dropped)}")
        if missing:
            problems.append(
                f"requires {', '.join(missing)}, which the model never sends"
            )
        return "; ".join(problems) or None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.fn(*args, **kwargs)


def function_tool(
    fn: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    filler: StaticToolFiller | dict[str, Any] | None = None,
    timeout_ms: int = 15000,
) -> Any:
    """Turn a function into a locally executed function tool.

    The parameter JSON Schema is derived from the function's type hints and the
    description from its docstring. Calls always await the handler result.
    Usable bare or with overrides::

        @function_tool
        def log_message(message: str) -> None:
            \"\"\"Log a message to the console.\"\"\"
            print(message)

        @function_tool(name="getWeather")
        async def get_weather(city: str) -> dict:
            \"\"\"Return the current weather for a city.\"\"\"
            return await weather_api(city)

        @function_tool
        def show_map(lat: float, lng: float) -> None:
            \"\"\"Display a map centered on the given coordinates.\"\"\"
            render_map(lat, lng)
    """

    def wrap(f: Callable[..., Any]) -> FunctionHandler:
        return FunctionHandler(
            f, name=name, description=description, filler=filler, timeout_ms=timeout_ms
        )

    return wrap(fn) if fn is not None else wrap


def _build_args_model(fn: Callable[..., Any], name: str) -> type[BaseModel]:
    fields: dict[str, Any] = {}
    signature = inspect.signature(fn)
    accepts_kwargs = any(
        param.kind == param.VAR_KEYWORD for param in signature.parameters.values()
    )
    for pname, param in signature.parameters.items():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        annotation = (
            param.annotation if param.annotation is not inspect.Parameter.empty else Any
        )
        default = param.default if param.default is not inspect.Parameter.empty else ...
        fields[pname] = (annotation, default)
    return create_model(
        f"{name}_Args",
        __config__=ConfigDict(extra="allow" if accepts_kwargs else "ignore"),
        **fields,
    )


Tool = (
    WebSearchTool
    | DocumentLibraryTool
    | CustomConnector
    | FunctionTool
    | TransferCallTool
    | HangUpTool
    | VoiceAgentTool
)


def check_function_handlers(
    definitions: list[VoiceAgentFunctionTool], handlers: list[FunctionHandler]
) -> VoiceAgentErrorEvent | None:
    """Raise on handlers that can't serve their declaration; report unpaired ones.

    Unpaired handlers and declarations are returned as a recoverable error event:
    the session works, but calls to an unhandled function fail.
    """
    by_name = {
        definition.function.name: definition.function for definition in definitions
    }
    mismatches = []
    problems = []
    for handler in handlers:
        definition = by_name.get(handler.name)
        if definition is None:
            problems.append(f"Handler `{handler.name}` has no function declaration")
            continue
        mismatch = handler.signature_mismatch(definition.parameters)
        if mismatch is not None:
            mismatches.append(f"Handler `{handler.name}` {mismatch}")
    if mismatches:
        raise VoiceAgentConfigurationError(
            "Invalid function handlers: " + "; ".join(mismatches)
        )
    for name in sorted(by_name.keys() - {handler.name for handler in handlers}):
        problems.append(f"Function `{name}` has no local handler")
    if problems:
        return VoiceAgentErrorEvent(
            source="transport",
            code="function_handler_configuration_error",
            message="Invalid function handlers: " + "; ".join(problems),
            fatal=False,
        )
    return None
