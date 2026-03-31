import random
from typing import Dict, Union

import httpx
from opentelemetry.propagate import inject

from .types import BeforeRequestContext, BeforeRequestHook


_EXECUTE_OPERATION_IDS = {
    "execute_workflow_v1_workflows__workflow_identifier__execute_post",
    "execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post",
}


class TraceparentInjectionHook(BeforeRequestHook):
    """Inject a sampled traceparent on /execute requests so worker traces are always recorded."""

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        if hook_ctx.operation_id not in _EXECUTE_OPERATION_IDS:
            return request

        # Don't overwrite an explicitly provided traceparent.
        if "traceparent" in request.headers:
            return request

        carrier: Dict[str, str] = {}
        inject(carrier)
        traceparent = carrier.get("traceparent", "")
        if not traceparent.endswith("-01"):
            trace_id = random.getrandbits(128)
            span_id = random.getrandbits(64)
            traceparent = f"00-{trace_id:032x}-{span_id:016x}-01"

        request.headers["traceparent"] = traceparent
        return request
