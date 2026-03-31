import re
import unittest
from unittest.mock import MagicMock

import httpx
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF

from mistralai.client._hooks.traceparent import TraceparentInjectionHook
from mistralai.client._hooks.types import BeforeRequestContext, HookContext


TRACEPARENT_RE = re.compile(r"^00-[0-9a-f]{32}-[0-9a-f]{16}-01$")

_EXECUTE_OP_ID = "execute_workflow_v1_workflows__workflow_identifier__execute_post"
_EXECUTE_REG_OP_ID = "execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post"
_OTHER_OP_ID = "list_executions_v1_workflows__workflow_identifier__executions_get"


def _make_hook_ctx(operation_id: str = _EXECUTE_OP_ID) -> BeforeRequestContext:
    ctx = HookContext(
        config=MagicMock(),
        base_url="https://api.mistral.ai",
        operation_id=operation_id,
        oauth2_scopes=None,
        security_source=None,
    )
    return BeforeRequestContext(ctx)


def _make_request(path: str, traceparent: str | None = None) -> httpx.Request:
    headers = {}
    if traceparent is not None:
        headers["traceparent"] = traceparent
    return httpx.Request("POST", f"https://api.mistral.ai{path}", headers=headers)


class TestTraceparentInjectionHook(unittest.TestCase):
    def setUp(self):
        self.hook = TraceparentInjectionHook()

    # --- non-execute operations must NOT be touched ---

    def test_other_operation_is_unchanged(self):
        req = _make_request("/v1/workflows/my-wf/executions")
        result = self.hook.before_request(_make_hook_ctx(_OTHER_OP_ID), req)
        assert isinstance(result, httpx.Request)
        self.assertNotIn("traceparent", result.headers)

    # --- execute operations: header injected ---

    def test_execute_gets_sampled_traceparent(self):
        req = _make_request("/v1/workflows/my-wf/execute")
        result = self.hook.before_request(_make_hook_ctx(_EXECUTE_OP_ID), req)
        assert isinstance(result, httpx.Request)
        self.assertIn("traceparent", result.headers)
        self.assertRegex(result.headers["traceparent"], TRACEPARENT_RE)

    def test_execute_registration_gets_sampled_traceparent(self):
        req = _make_request("/v1/workflows/registrations/reg-id/execute")
        result = self.hook.before_request(_make_hook_ctx(_EXECUTE_REG_OP_ID), req)
        assert isinstance(result, httpx.Request)
        self.assertIn("traceparent", result.headers)
        self.assertRegex(result.headers["traceparent"], TRACEPARENT_RE)

    def test_explicit_traceparent_is_not_overwritten(self):
        explicit = "00-aabbccddeeff00112233445566778899-0102030405060708-01"
        req = _make_request("/v1/workflows/my-wf/execute", traceparent=explicit)
        result = self.hook.before_request(_make_hook_ctx(_EXECUTE_OP_ID), req)
        assert isinstance(result, httpx.Request)
        self.assertEqual(result.headers["traceparent"], explicit)

    # --- OTEL context propagation ---

    def test_propagates_sampled_active_span(self):
        exporter = InMemorySpanExporter()
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("parent") as span:
            req = _make_request("/v1/workflows/my-wf/execute")
            result = self.hook.before_request(_make_hook_ctx(_EXECUTE_OP_ID), req)

        assert isinstance(result, httpx.Request)
        injected = result.headers["traceparent"]
        self.assertTrue(injected.endswith("-01"))
        trace_id_hex = f"{span.get_span_context().trace_id:032x}"
        self.assertIn(trace_id_hex, injected)

    def test_generates_fresh_traceparent_when_no_active_span(self):
        req = _make_request("/v1/workflows/my-wf/execute")
        result = self.hook.before_request(_make_hook_ctx(_EXECUTE_OP_ID), req)
        assert isinstance(result, httpx.Request)
        self.assertRegex(result.headers["traceparent"], TRACEPARENT_RE)

    def test_generates_fresh_traceparent_when_span_is_unsampled(self):
        provider = TracerProvider(sampler=ALWAYS_OFF)
        tracer = provider.get_tracer("test")

        with tracer.start_as_current_span("unsampled-parent"):
            req = _make_request("/v1/workflows/my-wf/execute")
            result = self.hook.before_request(_make_hook_ctx(_EXECUTE_OP_ID), req)

        assert isinstance(result, httpx.Request)
        injected = result.headers["traceparent"]
        self.assertTrue(injected.endswith("-01"), f"Expected sampled, got: {injected}")

if __name__ == "__main__":
    unittest.main()
