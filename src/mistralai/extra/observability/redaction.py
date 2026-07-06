"""Client-side redaction of telemetry spans before they are exported.

This module provides a configurable,  export-time masking layer for OpenTelemetry
spans so PII/secrets never leave the client. It is the primary, reusable
primitive: any OTEL application can wrap the exporter it owns with
RedactingSpanExporter, and the Mistral SDK installs it automatically in dedicated
telemetry mode (see configure_telemetry). Several redaction policies are
implemented in redaction_policies.py.

Requires the telemetry dependency extra to run, not to import.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Union

from .redaction_policies import (
    AttributeMaskCallback,
    CallbackRedactionPolicy,
    RedactionPolicy,
    default_redaction_policy,
)

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import ReadableSpan
    from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

    # Inherit from the real base only for static analysis: linters verify our
    # export/shutdown/force_flush signatures. At runtime the base is object so
    # the optional OpenTelemetry SDK is not required to import this module.
    _SpanExporterBase = SpanExporter
else:
    _SpanExporterBase = object


RedactionPolicyLike = Union["RedactionPolicy", AttributeMaskCallback]


def _resolve_redaction(redaction: RedactionPolicyLike | bool) -> RedactionPolicy | None:
    """Resolve redaction setting into a policy or None to disable redaction.

    True yields the default policy, False disables redaction entirely,
    and a policy or (key, value)->value | None callback is used as-is.
    """
    if redaction is False:
        return None
    if redaction is True:
        return default_redaction_policy()
    return _resolve_policy(redaction)


def _resolve_policy(policy: RedactionPolicyLike | None) -> RedactionPolicy:
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


# SpanExporter wrapper
class RedactingSpanExporter(_SpanExporterBase):
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
        self._policy = _resolve_policy(policy)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        redacted = [_redact_span(span, self._policy) for span in spans]
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


def _redact_span(span: ReadableSpan, policy: RedactionPolicy) -> ReadableSpan:
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
