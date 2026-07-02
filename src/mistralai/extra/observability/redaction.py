"""Client-side redaction of telemetry spans before they are exported.

This module provides an export-time masking layer for OpenTelemetry spans so
PII/secrets never leave the client. It is the primary, reusable primitive:
any OTEL application can wrap the exporter it owns with RedactingSpanExporter,
and the Mistral SDK installs it automatically in dedicated telemetry mode (see
``configure_telemetry``).

Requires the telemetry dependency extra to run, not to import.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Callable, Final, Union

from opentelemetry.util.types import AttributeValue

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import ReadableSpan
    from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


# User-supplied per-attribute masker: given (key, value), return the value
# to keep. Return the value unchanged to keep it, a redacted value to mask it,
# or None to drop the attribute entirely
AttributeMaskCallback = Callable[[str, AttributeValue], AttributeValue | None]
RedactionPolicyLike = Union["RedactionPolicy", AttributeMaskCallback]
DEFAULT_REDACTED_VALUE: Final[str] = "[REDACTED]"


class RedactionPolicy(ABC):
    """Base class for redaction policies."""

    @abstractmethod
    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        """Return a new attribute mapping with sensitive data removed."""
        raise NotImplementedError

    def redact_span_name(self, name: str) -> str:
        """Return the span name to export. Defaults to unchanged."""
        return name

    def redact_status_description(self, description: str | None) -> str | None:
        """Return the status description to export. Defaults to unchanged."""
        return description


DEFAULT_SENSITIVE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "client.address",
        "db.query.text",
        "db.statement",
        "exception.message",
        "exception.stacktrace",
        "gen_ai.input.messages",
        "gen_ai.output.messages",
        "gen_ai.tool.definitions",
        "http.request.body",
        "http.request.header.authorization",
        "http.request.header.cookie",
        "http.response.body",
        "http.response.header.set-cookie",
        "http.target",
        "http.url",
        "server.address",
        "url.full",
        "url.path",
        "url.query",
    }
)
DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "argument",
        "arguments",
        "authorization",
        "body",
        "completion",
        "content",
        "cookie",
        "input",
        "message",
        "messages",
        "output",
        "password",
        "payload",
        "prompt",
        "secret",
        "set_cookie",
        "token",
    }
)
DEFAULT_SAFE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "agent.trace.public",
        "client.port",
        "error.type",
        "exception.type",
        "gen_ai.agent.name",
        "gen_ai.conversation.id",
        "gen_ai.operation.name",
        "gen_ai.provider.name",
        "gen_ai.request.model",
        "gen_ai.response.finish_reasons",
        "gen_ai.response.id",
        "gen_ai.response.model",
        "gen_ai.tool.call.id",
        "gen_ai.tool.name",
        "gen_ai.tool.type",
        "http.request.method",
        "http.response.status_code",
        "network.protocol.name",
        "network.protocol.version",
        "server.port",
        "url.scheme",
    }
)
DEFAULT_TOKEN_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{10,}\b"),
)
_SAFE_KEY_PREFIXES: Final[tuple[str, ...]] = ("gen_ai.usage.",)
_PRIMITIVE_TYPES: Final[tuple[type, ...]] = (str, bool, int, float)


# TODO: also redact Sequence[str] ?


class AttributeRedactionPolicy(RedactionPolicy):
    """Key-oriented hybrid policy.

    This is the default policy: high recall, "safe by default", at the cost of erasing most
    prompt/response content. It redacts whole values for keys judged sensitive (explicit set,
    fragment match, or non-primitive value), then runs token_patterns over the values it keeps
    to redact values.
    """

    def __init__(
        self,
        *,
        sensitive_keys: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
        safe_keys: frozenset[str] = DEFAULT_SAFE_ATTRIBUTE_KEYS,
        sensitive_fragments: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
        token_patterns: Sequence[re.Pattern[str]] = DEFAULT_TOKEN_PATTERNS,
        redact_non_primitive: bool = True,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
    ) -> None:
        self._sensitive_keys = sensitive_keys
        self._safe_keys = safe_keys
        self._sensitive_fragments = sensitive_fragments
        self._token_patterns = tuple(token_patterns)
        self._redact_non_primitive = redact_non_primitive
        self._redacted_value = redacted_value

    def _should_redact(self, key: str, value: object) -> bool:
        normalized_key = key.lower()
        if normalized_key in self._safe_keys:
            return False
        if normalized_key.startswith(_SAFE_KEY_PREFIXES):
            return False
        if normalized_key in self._sensitive_keys:
            return True
        if self._has_sensitive_fragment(normalized_key):
            return True
        return self._redact_non_primitive and not isinstance(value, _PRIMITIVE_TYPES)

    def _has_sensitive_fragment(self, normalized_key: str) -> bool:
        normalized_words = normalized_key.replace("-", "_").replace(".", "_")
        key_fragments = {word for word in normalized_words.split("_") if word}
        return any(
            fragment in key_fragments or fragment in normalized_words
            for fragment in self._sensitive_fragments
        )

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            if self._should_redact(key, value):
                redacted[key] = self._redacted_value
                continue
            if isinstance(value, str):
                redacted[key] = _redact_text(
                    value, self._token_patterns, self._redacted_value
                )
                continue
            redacted[key] = value

        return redacted

    def redact_status_description(self, description: str | None) -> str | None:
        """Redact error descriptions (they often carry request/response text)."""
        if description is None:
            return None
        return self._redacted_value


DEFAULT_PII_SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    *DEFAULT_TOKEN_PATTERNS,
    # Email addresses
    re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    # Credit-card-like sequences (13-16 digits, optional spaces/dashes)
    re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    # IPv4 addresses
    re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
    ),
)


class RegexRedactionPolicy(RedactionPolicy):
    """Content-oriented policy based on regexes.

    Leaves keys and structure intact, scans string values and redacts matched substrings.
    Fewer false positives than default policy and aims to preserve observability value;
    may miss free-form PII or secrets not in the default patterns.
    """

    def __init__(
        self,
        patterns: Sequence[re.Pattern[str]] = DEFAULT_PII_SECRET_PATTERNS,
        *,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
    ) -> None:
        self._patterns = tuple(patterns)
        self._redacted_value = redacted_value

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            if isinstance(value, str):
                redacted[key] = _redact_text(
                    value, self._patterns, self._redacted_value
                )
                continue
            redacted[key] = value

        return redacted

    def redact_span_name(self, name: str) -> str:
        return _redact_text(name, self._patterns, self._redacted_value)

    def redact_status_description(self, description: str | None) -> str | None:
        if description is None:
            return None
        return _redact_text(description, self._patterns, self._redacted_value)


class CallbackRedactionPolicy(RedactionPolicy):
    """Callback-based policy for users to provide custom redaction capabilities.

    The callback is invoked per attribute and should return the value to keep or None to drop the attribute.
    Span name and status description are left unchanged (the callback operates on attributes only).
    """

    def __init__(self, mask_function: AttributeMaskCallback) -> None:
        self._mask_function = mask_function

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            masked = self._mask_function(key, value)
            if masked is None:
                continue
            redacted[key] = masked

        return redacted


# Helpers
def default_redaction_policy() -> RedactionPolicy:
    return AttributeRedactionPolicy()


def resolve_policy(policy: RedactionPolicyLike | None) -> RedactionPolicy:
    if policy is None:
        return default_redaction_policy()
    if isinstance(policy, RedactionPolicy):
        return policy
    if callable(policy):
        return CallbackRedactionPolicy(policy)
    raise TypeError(
        "redaction policy must be a RedactionPolicy, a callable, or None; "
        f"got {type(policy).__name__}."
    )


def resolve_redaction(redaction: RedactionPolicyLike | bool) -> RedactionPolicy | None:
    """Resolve redaction setting into a policy or None to disable redaction.

    True yields the default policy, False disables redaction entirely,
    and a policy or (key, value)->value | None callback is used as-is.
    """
    if redaction is False:
        return None
    if redaction is True:
        return default_redaction_policy()
    return resolve_policy(redaction)


# SpanExporter wrapper
# NOTE: in essence this is a subclass of SpanExporter. It's not typed as such because
# the opentelemetry SDK is an optional dependency, so to keep it importable we duck-type it
# TODO: can't we rely on typing to have static linters verify that ? (i.e. don't inherit, but type)
class RedactingSpanExporter:
    """Wrap any SpanExporter to redact spans before delegating export.

    Example
    -------
    >>> exporter = RedactingSpanExporter(OTLPSpanExporter(...))
    >>> provider.add_span_processor(BatchSpanProcessor(exporter))
    """

    def __init__(
        self,
        exporter: SpanExporter,
        policy: RedactionPolicyLike | None = None,
    ) -> None:
        _load_span_types()  # fail fast if the SDK is unavailable
        self._exporter = exporter
        self._policy = resolve_policy(policy)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        redacted = [redact_span(span, self._policy) for span in spans]
        return self._exporter.export(redacted)

    def shutdown(self) -> None:
        self._exporter.shutdown()

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        return self._exporter.force_flush(timeout_millis)


def _load_span_types() -> Any:
    """Import the OpenTelemetry SDK span classes needed to rebuild spans.

    Raises a helpful error when the optional ``[telemetry]`` extra is missing.
    """
    try:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import Event, ReadableSpan
        from opentelemetry.trace import Link, SpanKind, Status, StatusCode
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Telemetry redaction requires the optional OpenTelemetry SDK "
            "dependencies. Install them with `pip install 'mistralai[telemetry]'` "
            "or `uv add 'mistralai[telemetry]'`."
        ) from exc

    return _SpanTypes(
        Event=Event,
        Link=Link,
        ReadableSpan=ReadableSpan,
        Resource=Resource,
        SpanKind=SpanKind,
        Status=Status,
        StatusCode=StatusCode,
    )


class _SpanTypes:
    __slots__ = (
        "Event",
        "Link",
        "ReadableSpan",
        "Resource",
        "SpanKind",
        "Status",
        "StatusCode",
    )

    def __init__(self, **types: Any) -> None:
        for name, value in types.items():
            setattr(self, name, value)


def redact_span(span: ReadableSpan, policy: RedactionPolicy) -> ReadableSpan:
    types = _load_span_types()

    attributes = policy.redact_attributes(getattr(span, "attributes", None))
    events = _redact_events(getattr(span, "events", ()) or (), policy, types)
    links = _redact_links(getattr(span, "links", ()) or (), policy, types)
    resource = _redact_resource(getattr(span, "resource", None), policy, types)
    status = _redact_status(getattr(span, "status", None), policy, types)
    name = policy.redact_span_name(getattr(span, "name", "") or "")

    return types.ReadableSpan(
        name=name,
        context=getattr(span, "context", None),
        parent=getattr(span, "parent", None),
        resource=resource,
        attributes=attributes,
        events=events,
        links=links,
        kind=getattr(span, "kind", None) or types.SpanKind.INTERNAL,
        status=status,
        start_time=getattr(span, "start_time", None),
        end_time=getattr(span, "end_time", None),
        instrumentation_scope=getattr(span, "instrumentation_scope", None),
    )


def _redact_events(
    events: Sequence[Any], policy: RedactionPolicy, types: Any
) -> list[Any]:
    return [
        types.Event(
            name=getattr(event, "name", ""),
            attributes=policy.redact_attributes(getattr(event, "attributes", None)),
            timestamp=getattr(event, "timestamp", None),
        )
        for event in events
    ]


def _redact_links(
    links: Sequence[Any], policy: RedactionPolicy, types: Any
) -> list[Any]:
    return [
        types.Link(
            context=getattr(link, "context", None),
            attributes=policy.redact_attributes(getattr(link, "attributes", None)),
        )
        for link in links
    ]


def _redact_resource(resource: Any, policy: RedactionPolicy, types: Any) -> Any:
    if resource is None:
        return None
    return types.Resource(
        attributes=policy.redact_attributes(getattr(resource, "attributes", None)),
        schema_url=getattr(resource, "schema_url", ""),
    )


def _redact_status(status: Any, policy: RedactionPolicy, types: Any) -> Any:
    if status is None:
        return types.Status()
    status_code = getattr(status, "status_code", None) or types.StatusCode.UNSET
    description = policy.redact_status_description(getattr(status, "description", None))
    return types.Status(status_code, description)


def _redact_text(
    text: str,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str = DEFAULT_REDACTED_VALUE,
) -> str:
    redacted = text
    for pattern in patterns:
        redacted = pattern.sub(redacted_value, redacted)
    return redacted
