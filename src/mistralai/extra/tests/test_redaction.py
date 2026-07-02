"""Tests for client-side telemetry redaction."""

import unittest

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExportResult
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, Status, StatusCode

from mistralai.extra.observability.redaction import (
    DEFAULT_PII_SECRET_PATTERNS,
    DEFAULT_REDACTED_VALUE,
    DEFAULT_TOKEN_PATTERNS,
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    RedactingSpanExporter,
    RedactionPolicy,
    RegexRedactionPolicy,
    default_redaction_policy,
    redact_span,
    resolve_policy,
)


class TestAttributeRedactionPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = AttributeRedactionPolicy()

    def test_sensitive_key_redacted_wholesale(self):
        out = self.policy.redact_attributes({"gen_ai.input.messages": "hello"})
        self.assertEqual(out["gen_ai.input.messages"], DEFAULT_REDACTED_VALUE)

    def test_safe_key_kept(self):
        out = self.policy.redact_attributes({"gen_ai.request.model": "mistral-large"})
        self.assertEqual(out["gen_ai.request.model"], "mistral-large")

    def test_usage_prefix_kept(self):
        out = self.policy.redact_attributes({"gen_ai.usage.input_tokens": 42})
        self.assertEqual(out["gen_ai.usage.input_tokens"], 42)

    def test_fragment_match_redacted(self):
        out = self.policy.redact_attributes({"custom.prompt.text": "secret prompt"})
        self.assertEqual(out["custom.prompt.text"], DEFAULT_REDACTED_VALUE)

    def test_token_pattern_on_kept_string(self):
        out = self.policy.redact_attributes(
            {"note": "call token ghp_abcdefghijklmnopqrstuvwxyz0123 now"}
        )
        self.assertEqual(out["note"], "call token [REDACTED] now")

    def test_non_primitive_redacted(self):
        out = self.policy.redact_attributes({"data": ("a", "b")})
        self.assertEqual(out["data"], DEFAULT_REDACTED_VALUE)

    def test_non_primitive_kept_when_disabled(self):
        policy = AttributeRedactionPolicy(redact_non_primitive=False)
        out = policy.redact_attributes({"safeish.list": ("a", "b")})
        self.assertEqual(out["safeish.list"], ("a", "b"))

    def test_string_sequence_scanned_element_wise_when_kept(self):
        policy = AttributeRedactionPolicy(redact_non_primitive=False)
        out = policy.redact_attributes(
            {"tags": ["plain", "ghp_abcdefghijklmnopqrstuvwxyz0123"]}
        )
        self.assertEqual(out["tags"], ["plain", DEFAULT_REDACTED_VALUE])

    def test_safe_key_string_sequence_scanned(self):
        out = self.policy.redact_attributes(
            {"gen_ai.response.finish_reasons": ("stop", "Bearer abc.def")}
        )
        self.assertEqual(
            out["gen_ai.response.finish_reasons"], ("stop", DEFAULT_REDACTED_VALUE)
        )

    def test_none_attributes_returns_empty(self):
        self.assertEqual(self.policy.redact_attributes(None), {})

    def test_status_description_redacted(self):
        self.assertEqual(
            self.policy.redact_status_description("boom: user@x.com"),
            DEFAULT_REDACTED_VALUE,
        )
        self.assertIsNone(self.policy.redact_status_description(None))

    def test_span_name_unchanged(self):
        self.assertEqual(self.policy.redact_span_name("chat mistral-large"), "chat mistral-large")

    def test_custom_redacted_value(self):
        policy = AttributeRedactionPolicy(redacted_value="XXX")
        out = policy.redact_attributes({"http.url": "https://x"})
        self.assertEqual(out["http.url"], "XXX")


class TestRegexRedactionPolicy(unittest.TestCase):
    def setUp(self):
        self.policy = RegexRedactionPolicy()

    def test_email_redacted_inline_preserving_structure(self):
        out = self.policy.redact_attributes(
            {"gen_ai.input.messages": '{"content":"reach me at a@b.com"}'}
        )
        self.assertEqual(
            out["gen_ai.input.messages"], '{"content":"reach me at [REDACTED]"}'
        )

    def test_token_redacted(self):
        out = self.policy.redact_attributes({"h": "Bearer abc.def-ghi"})
        self.assertEqual(out["h"], "[REDACTED]")

    def test_non_matching_string_kept(self):
        out = self.policy.redact_attributes({"server.address": "prod-host-1"})
        self.assertEqual(out["server.address"], "prod-host-1")

    def test_non_string_untouched(self):
        out = self.policy.redact_attributes({"n": 5, "b": True})
        self.assertEqual(out, {"n": 5, "b": True})

    def test_string_sequence_scanned_preserving_container(self):
        out = self.policy.redact_attributes(
            {"msgs": ["hello", "reach me at a@b.com"]}
        )
        self.assertEqual(out["msgs"], ["hello", "reach me at [REDACTED]"])

    def test_tuple_sequence_stays_tuple(self):
        out = self.policy.redact_attributes({"msgs": ("hi", "a@b.com")})
        self.assertEqual(out["msgs"], ("hi", "[REDACTED]"))

    def test_numeric_sequence_untouched(self):
        out = self.policy.redact_attributes({"nums": [1, 2, 3]})
        self.assertEqual(out["nums"], [1, 2, 3])

    def test_span_name_scanned(self):
        self.assertEqual(self.policy.redact_span_name("op a@b.com"), "op [REDACTED]")

    def test_status_description_scanned(self):
        self.assertEqual(
            self.policy.redact_status_description("failed for a@b.com"),
            "failed for [REDACTED]",
        )

    def test_secret_patterns_redacted(self):
        secrets = {
            "aws": "AKIAIOSFODNN7EXAMPLE",
            "google": "AIzaabcdefghijklmnopqrstuvwxyz012345678",
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123",
            "pem": "-----BEGIN RSA PRIVATE KEY-----",
            "stripe": "sk_live_0123456789abcdefghij",
        }
        for name, secret in secrets.items():
            with self.subTest(secret=name):
                out = self.policy.redact_attributes({"v": f"leak {secret} here"})
                self.assertNotIn(secret, out["v"])
                self.assertIn(DEFAULT_REDACTED_VALUE, out["v"])


class TestDefaultPatternComposition(unittest.TestCase):
    def test_pii_patterns_extend_token_patterns(self):
        prefix = DEFAULT_PII_SECRET_PATTERNS[: len(DEFAULT_TOKEN_PATTERNS)]
        self.assertEqual(prefix, DEFAULT_TOKEN_PATTERNS)
        self.assertGreater(
            len(DEFAULT_PII_SECRET_PATTERNS), len(DEFAULT_TOKEN_PATTERNS)
        )


class TestCallbackRedactionPolicy(unittest.TestCase):
    def test_mask_applied_per_attribute(self):
        policy = CallbackRedactionPolicy(
            lambda key, value: "[X]" if "message" in key else value
        )
        out = policy.redact_attributes(
            {"gen_ai.output.messages": "hi", "gen_ai.request.model": "m"}
        )
        self.assertEqual(out, {"gen_ai.output.messages": "[X]", "gen_ai.request.model": "m"})

    def test_returning_none_drops_attribute(self):
        policy = CallbackRedactionPolicy(
            lambda key, value: None if key == "drop" else value
        )
        out = policy.redact_attributes({"drop": "x", "keep": "y"})
        self.assertEqual(out, {"keep": "y"})


class TestRedactionPolicyABC(unittest.TestCase):
    def test_base_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            RedactionPolicy()  # type: ignore[abstract]

    def test_subclass_without_redact_attributes_cannot_be_instantiated(self):
        class Incomplete(RedactionPolicy):
            pass

        with self.assertRaises(TypeError):
            Incomplete()  # type: ignore[abstract]

    def test_subclass_implementing_redact_attributes_instantiates(self):
        class Minimal(RedactionPolicy):
            def redact_attributes(self, attributes):
                return dict(attributes or {})

        policy = Minimal()
        # Concrete identity defaults remain available.
        self.assertEqual(policy.redact_span_name("span"), "span")
        self.assertEqual(policy.redact_status_description("desc"), "desc")


class TestResolvePolicy(unittest.TestCase):
    def test_none_returns_default(self):
        self.assertIsInstance(resolve_policy(None), AttributeRedactionPolicy)
        self.assertIsInstance(default_redaction_policy(), AttributeRedactionPolicy)

    def test_policy_passthrough(self):
        policy = RegexRedactionPolicy()
        self.assertIs(resolve_policy(policy), policy)

    def test_callable_wrapped(self):
        resolved = resolve_policy(lambda k, v: v)
        self.assertIsInstance(resolved, CallbackRedactionPolicy)

    def test_invalid_raises_type_error(self):
        with self.assertRaises(TypeError):
            resolve_policy(123)  # type: ignore[arg-type]


class TestRedactSpan(unittest.TestCase):
    def _make_span(self):
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

    def test_rebuilds_genuine_readable_span(self):
        from opentelemetry.sdk.trace import ReadableSpan

        original = self._make_span()
        redacted = redact_span(original, default_redaction_policy())
        self.assertIsInstance(redacted, ReadableSpan)

    def test_attributes_redacted(self):
        redacted = redact_span(self._make_span(), default_redaction_policy())
        self.assertEqual(redacted.attributes["gen_ai.input.messages"], DEFAULT_REDACTED_VALUE)
        self.assertEqual(redacted.attributes["gen_ai.request.model"], "mistral-large")

    def test_event_attributes_redacted(self):
        redacted = redact_span(self._make_span(), default_redaction_policy())
        event = redacted.events[0]
        self.assertEqual(event.name, "exception")
        self.assertEqual(event.attributes["exception.message"], DEFAULT_REDACTED_VALUE)

    def test_status_description_redacted(self):
        redacted = redact_span(self._make_span(), default_redaction_policy())
        self.assertEqual(redacted.status.status_code, StatusCode.ERROR)
        self.assertEqual(redacted.status.description, DEFAULT_REDACTED_VALUE)

    def test_identity_preserved(self):
        original = self._make_span()
        redacted = redact_span(original, default_redaction_policy())
        self.assertEqual(redacted.context.span_id, original.context.span_id)
        self.assertEqual(redacted.context.trace_id, original.context.trace_id)


class TestRedactingSpanExporter(unittest.TestCase):
    def _export_through(self, policy=None):
        wrapped = InMemorySpanExporter()
        provider = TracerProvider()
        provider.add_span_processor(
            SimpleSpanProcessor(RedactingSpanExporter(wrapped, policy))
        )
        tracer = provider.get_tracer("test")
        with tracer.start_as_current_span("chat") as span:
            span.set_attribute("gen_ai.output.messages", "leak")
            span.set_attribute("gen_ai.request.model", "mistral-large")
        provider.force_flush()
        return wrapped.get_finished_spans()

    def test_wrapped_exporter_receives_redacted_spans(self):
        spans = self._export_through()
        self.assertEqual(len(spans), 1)
        attrs = spans[0].attributes
        self.assertEqual(attrs["gen_ai.output.messages"], DEFAULT_REDACTED_VALUE)
        self.assertEqual(attrs["gen_ai.request.model"], "mistral-large")

    def test_custom_policy_used(self):
        spans = self._export_through(RegexRedactionPolicy())
        # Regex policy keeps structure; "leak" has no PII pattern -> unchanged.
        self.assertEqual(spans[0].attributes["gen_ai.output.messages"], "leak")

    def test_export_returns_wrapped_result(self):
        wrapped = InMemorySpanExporter()
        exporter = RedactingSpanExporter(wrapped)
        self.assertEqual(exporter.export([]), SpanExportResult.SUCCESS)

    def test_shutdown_and_force_flush_delegate(self):
        class _Recorder(InMemorySpanExporter):
            def __init__(self):
                super().__init__()
                self.shutdown_called = False
                self.flush_called = False

            def shutdown(self):
                self.shutdown_called = True
                super().shutdown()

            def force_flush(self, timeout_millis=30000):
                self.flush_called = True
                return True

        recorder = _Recorder()
        exporter = RedactingSpanExporter(recorder)
        self.assertTrue(exporter.force_flush())
        exporter.shutdown()
        self.assertTrue(recorder.flush_called)
        self.assertTrue(recorder.shutdown_called)


if __name__ == "__main__":
    unittest.main()
