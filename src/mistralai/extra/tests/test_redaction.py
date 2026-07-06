import pytest
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, Status, StatusCode

from mistralai.extra.observability.redaction import (
    RedactingSpanExporter,
    _redact_span,
    _resolve_policy,
    _resolve_redaction,
)
from mistralai.extra.observability.redaction_policies import (
    DEFAULT_REDACTED_VALUE,
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    RegexRedactionPolicy,
    default_redaction_policy,
)


class TestResolvePolicy:
    def test_none_returns_default(self):
        assert isinstance(default_redaction_policy(), RegexRedactionPolicy)
        assert isinstance(_resolve_policy(None), RegexRedactionPolicy)

    def test_policy_passthrough(self):
        policy = RegexRedactionPolicy()
        assert _resolve_policy(policy) is policy

    def test_callable_wrapped(self):
        resolved = _resolve_policy(lambda k, v: v)
        assert isinstance(resolved, CallbackRedactionPolicy)

    def test_invalid_raises_type_error(self):
        with pytest.raises(TypeError):
            _resolve_policy(123)  # type: ignore[arg-type]


class TestResolveRedaction:
    def test_true_returns_default_policy(self):
        assert isinstance(_resolve_redaction(True), RegexRedactionPolicy)

    def test_false_returns_none(self):
        assert _resolve_redaction(False) is None

    def test_policy_passthrough(self):
        policy = RegexRedactionPolicy()
        assert _resolve_redaction(policy) is policy

    def test_callable_wrapped(self):
        resolved = _resolve_redaction(lambda k, v: v)
        assert isinstance(resolved, CallbackRedactionPolicy)


class TestRedactSpan:
    @staticmethod
    def _make_span():
        exporter = InMemorySpanExporter()
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        tracer = provider.get_tracer("test")
        with tracer.start_as_current_span("parent", kind=SpanKind.CLIENT) as span:
            span.set_attribute("gen_ai.input.messages", "secret")
            span.set_attribute("gen_ai.request.model", "mistral-large")
            span.add_event("exception", {"exception.message": "boom"})
            span.set_status(Status(StatusCode.ERROR, "boom detail"))
        provider.force_flush()
        return exporter.get_finished_spans()[0]

    def test_attributes_redacted(self):
        redacted = _redact_span(self._make_span(), AttributeRedactionPolicy())
        assert isinstance(redacted, ReadableSpan)
        attrs = redacted.attributes
        assert attrs is not None
        assert attrs["gen_ai.input.messages"] == DEFAULT_REDACTED_VALUE
        assert attrs["gen_ai.request.model"] == "mistral-large"

    def test_event_attributes_redacted(self):
        redacted = _redact_span(self._make_span(), AttributeRedactionPolicy())
        event = redacted.events[0]
        assert event.name == "exception"
        attrs = event.attributes
        assert attrs is not None
        assert attrs["exception.message"] == DEFAULT_REDACTED_VALUE

    def test_status_description_redacted(self):
        redacted = _redact_span(self._make_span(), AttributeRedactionPolicy())
        assert redacted.status.status_code == StatusCode.ERROR
        assert redacted.status.description == DEFAULT_REDACTED_VALUE

    def test_identity_preserved(self):
        original = self._make_span()
        redacted = _redact_span(original, AttributeRedactionPolicy())
        assert redacted.context is not None
        assert original.context is not None
        assert redacted.context.span_id == original.context.span_id
        assert redacted.context.trace_id == original.context.trace_id


class TestRedactingSpanExporter:
    @staticmethod
    def _export_through(policy=None):
        wrapped = InMemorySpanExporter()
        provider = TracerProvider()
        provider.add_span_processor(
            SimpleSpanProcessor(RedactingSpanExporter(wrapped, policy))
        )
        tracer = provider.get_tracer("test")
        with tracer.start_as_current_span("chat") as span:
            span.set_attribute("gen_ai.output.messages", "leak Bearer abc.def-ghi")
            span.set_attribute("gen_ai.request.model", "mistral-large")
        provider.force_flush()
        return wrapped.get_finished_spans()

    def test_wrapped_exporter_receives_redacted_spans(self):
        spans = self._export_through()
        assert len(spans) == 1
        attrs = spans[0].attributes
        assert attrs is not None
        assert attrs["gen_ai.output.messages"] == f"leak {DEFAULT_REDACTED_VALUE}"
        assert attrs["gen_ai.request.model"] == "mistral-large"

    def test_custom_policy_used(self):
        spans = self._export_through(AttributeRedactionPolicy())
        attrs = spans[0].attributes
        assert attrs is not None
        assert attrs["gen_ai.output.messages"] == DEFAULT_REDACTED_VALUE
