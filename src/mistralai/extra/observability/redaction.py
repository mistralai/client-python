"""Client-side redaction of telemetry spans before they are exported.

This module provides an export-time masking layer for OpenTelemetry spans so
PII/secrets never leave the client. It is the primary, reusable primitive:
any OTEL application can wrap the exporter it owns with
:class:`RedactingSpanExporter`, and the Mistral SDK installs it automatically
in ``dedicated`` telemetry mode (see ``configure_telemetry``).

Design notes
------------
* Redaction happens at *export* time (inside the batch export thread), off the
  request hot path, and covers every span that reaches the wrapped exporter --
  including spans the application itself produces (e.g. tool input/output),
  not just spans created by the Mistral SDK.
* Because masking is per-pipeline, it only protects the exporter it wraps. In
  ``global``/``custom`` provider modes the application owns the pipeline and
  must install the wrapper itself (one line); in ``dedicated`` mode the SDK
  owns the exporter and wraps it for you.

Requires the optional OpenTelemetry SDK dependencies
(``pip install 'mistralai[telemetry]'``). The policy classes are importable
without the SDK; only :class:`RedactingSpanExporter` needs it.
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


__all__ = [
    "AttributeMaskCallback",
    "AttributeRedactionPolicy",
    "CallbackRedactionPolicy",
    "DEFAULT_PII_SECRET_PATTERNS",
    "DEFAULT_REDACTED_VALUE",
    "DEFAULT_SAFE_ATTRIBUTE_KEYS",
    "DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS",
    "DEFAULT_SENSITIVE_ATTRIBUTE_KEYS",
    "DEFAULT_TOKEN_PATTERNS",
    "RedactingSpanExporter",
    "RedactionPolicy",
    "RedactionPolicyLike",
    "RegexRedactionPolicy",
    "default_redaction_policy",
    "redact_span",
    "resolve_policy",
]


# --------------------------------------------------------------------------- #
# Types
# --------------------------------------------------------------------------- #

#: A user-supplied per-attribute masker: given (key, value), return the value
#: to keep. Return the value unchanged to keep it, a redacted value to mask it,
#: or ``None`` to drop the attribute entirely. Mirrors the langfuse/braintrust
#: ``mask`` callback style.
AttributeMaskCallback = Callable[[str, object], object]

#: Anything accepted where a policy is expected: a full policy or a callback.
RedactionPolicyLike = Union["RedactionPolicy", AttributeMaskCallback]

DEFAULT_REDACTED_VALUE: Final[str] = "[REDACTED]"


# --------------------------------------------------------------------------- #
# Policy interface
# --------------------------------------------------------------------------- #


class RedactionPolicy(ABC):
    """Base class for redaction policies.

    Subclasses must implement :meth:`redact_attributes`. Span-name and
    status-description redaction default to identity so most policies only
    override the attribute logic.

    This is an abstract base class: a subclass that omits
    :meth:`redact_attributes` fails at instantiation rather than at export
    time (redaction runs in the background batch-export thread, where a late
    error is easy to miss). Callers that just want a per-attribute masker can
    pass a plain ``(key, value)`` callable instead of subclassing; see
    :data:`RedactionPolicyLike` and :func:`resolve_policy`.
    """

    @abstractmethod
    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        """Return a new attribute mapping with sensitive data removed.

        Implementations may add ``<key>.redacted_*`` metadata attributes to
        preserve non-sensitive shape information (length, count, type).
        """
        raise NotImplementedError

    def redact_span_name(self, name: str) -> str:
        """Return the span name to export. Defaults to unchanged."""
        return name

    def redact_status_description(self, description: str | None) -> str | None:
        """Return the status description to export. Defaults to unchanged."""
        return description


# --------------------------------------------------------------------------- #
# Default (blunt, hybrid) policy -- lifted & hardened from
# vibe_sdk/.../otel/attribute_redaction.py
# --------------------------------------------------------------------------- #

#: Attribute keys whose values are always redacted wholesale.
DEFAULT_SENSITIVE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset({
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
})

#: Attribute keys explicitly known to be safe (never redacted).
DEFAULT_SAFE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset({
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
})

#: Substrings that, when present in a key, mark its value as sensitive
#: (e.g. ``content``, ``prompt``, ``arguments``, ``token``...).
DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS: Final[frozenset[str]] = frozenset({
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
})

#: Regexes applied to the *content* of otherwise-kept string values, catching
#: inline secrets (bearer tokens, ``ghp_``/``xox`` tokens, ...).
DEFAULT_TOKEN_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
)

#: Attribute key prefixes never redacted (metrics/usage counters).
_SAFE_KEY_PREFIXES: Final[tuple[str, ...]] = ("gen_ai.usage.",)

_PRIMITIVE_TYPES: Final[tuple[type, ...]] = (str, bool, int, float)


def _redact_text(
    text: str, patterns: Sequence[re.Pattern[str]], redacted_value: str
) -> str:
    """Return *text* with every match of *patterns* replaced by *redacted_value*."""
    redacted = text
    for pattern in patterns:
        redacted = pattern.sub(redacted_value, redacted)
    return redacted


class AttributeRedactionPolicy(RedactionPolicy):
    """Key-oriented hybrid policy. Redacts whole values for keys judged
    sensitive (explicit set, fragment match, or non-primitive value), then
    runs :attr:`token_patterns` over the values it keeps.

    This is the out-of-the-box default: high recall / "safe by default", at
    the cost of erasing most prompt/response content. Prefer
    :class:`RegexRedactionPolicy` when you need to keep trace utility.
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

    def _should_redact(self, normalized_key: str, value: object) -> bool:
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
            attribute_key = str(key)
            normalized_key = attribute_key.lower()
            if self._should_redact(normalized_key, value):
                redacted[attribute_key] = self._redacted_value
                continue
            if isinstance(value, str):
                redacted[attribute_key] = _redact_text(
                    value, self._token_patterns, self._redacted_value
                )
                continue
            redacted[attribute_key] = value

        return redacted

    def redact_status_description(self, description: str | None) -> str | None:
        """Redact error descriptions (they often carry request/response text)."""
        if description is None:
            return None
        return self._redacted_value


# --------------------------------------------------------------------------- #
# Content-aware policy (lighter, opt-in)
# --------------------------------------------------------------------------- #

#: PII/secret content patterns: emails, credit cards, IPs, bearer/api tokens...
DEFAULT_PII_SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    # Secrets / tokens
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    # Email addresses
    re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    # Credit-card-like sequences (13-16 digits, optional spaces/dashes)
    re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    # IPv4 addresses
    re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
)


class RegexRedactionPolicy(RedactionPolicy):
    """Content-only policy: leaves keys and structure intact, scans string
    values and redacts matched substrings. Lower false-positive, preserves
    observability value; may miss free-form PII (names, addresses).
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
            attribute_key = str(key)
            if isinstance(value, str):
                redacted[attribute_key] = _redact_text(
                    value, self._patterns, self._redacted_value
                )
                continue
            redacted[attribute_key] = value

        return redacted

    def redact_span_name(self, name: str) -> str:
        return _redact_text(name, self._patterns, self._redacted_value)

    def redact_status_description(self, description: str | None) -> str | None:
        if description is None:
            return None
        return _redact_text(description, self._patterns, self._redacted_value)


# --------------------------------------------------------------------------- #
# Callback adapter (langfuse-style)
# --------------------------------------------------------------------------- #


class CallbackRedactionPolicy(RedactionPolicy):
    """Adapt a plain ``Callable[[key, value], value]`` into a policy.

    The callback is invoked per attribute; return the value to keep, a
    redacted value, or ``None`` to drop the attribute. Span name and status
    description are left unchanged (the callback operates on attributes only).
    """

    def __init__(self, mask: AttributeMaskCallback) -> None:
        self._mask = mask

    def redact_attributes(
        self, attributes: Mapping[str, AttributeValue] | None
    ) -> dict[str, AttributeValue]:
        redacted: dict[str, AttributeValue] = {}
        if attributes is None:
            return redacted

        for key, value in attributes.items():
            attribute_key = str(key)
            masked = self._mask(attribute_key, value)
            if masked is None:
                continue
            redacted[attribute_key] = masked

        return redacted


# --------------------------------------------------------------------------- #
# Resolution helpers
# --------------------------------------------------------------------------- #


def default_redaction_policy() -> RedactionPolicy:
    """Return the default policy (an :class:`AttributeRedactionPolicy`)."""
    return AttributeRedactionPolicy()


def resolve_policy(policy: RedactionPolicyLike | None) -> RedactionPolicy:
    """Coerce a policy/callback/None into a concrete :class:`RedactionPolicy`.

    ``None`` -> :func:`default_redaction_policy`; a callable is wrapped in
    :class:`CallbackRedactionPolicy`; a policy is returned as-is.
    """
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


# --------------------------------------------------------------------------- #
# Span reconstruction + exporter wrapper
#   span rebuild lifted & hardened from vibe_sdk/.../otel/sanitizer.py
# --------------------------------------------------------------------------- #


def _load_span_types() -> Any:
    """Import the OpenTelemetry SDK span classes needed to rebuild spans.

    Raises a helpful error when the optional ``[telemetry]`` extra is missing.
    """
    try:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import Event, ReadableSpan
        from opentelemetry.trace import Link, SpanKind, Status, StatusCode
    except ImportError as exc:  # pragma: no cover - exercised via install matrix
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
    """Return a redacted copy of a readable span.

    Rebuilds a genuine :class:`ReadableSpan` (attributes, events, links,
    resource, status, name) so the wrapped exporter's serialization keeps
    working. ReadableSpans are frozen at export, hence reconstruction.
    """
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


class RedactingSpanExporter:
    """Wrap any ``SpanExporter``; redact every span before delegating export.

    Not a subclass of ``SpanExporter``: it duck-types the exporter interface
    (``export`` / ``shutdown`` / ``force_flush``), which is all a span
    processor calls. This keeps the module importable without the optional
    OpenTelemetry SDK; only actual export needs it.

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
        """Raises ``ImportError`` if the OpenTelemetry SDK extra is missing."""
        _load_span_types()  # fail fast if the SDK is unavailable
        self._exporter = exporter
        self._policy = resolve_policy(policy)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """Redact each span, then delegate to the wrapped exporter."""
        redacted = [redact_span(span, self._policy) for span in spans]
        return self._exporter.export(redacted)

    def shutdown(self) -> None:
        """Delegate to the wrapped exporter."""
        self._exporter.shutdown()

    def force_flush(self, timeout_millis: int = 30_000) -> bool:
        """Delegate to the wrapped exporter."""
        return self._exporter.force_flush(timeout_millis)
