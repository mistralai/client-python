import random
from typing import Dict, Union

import httpx
from opentelemetry.propagate import inject

from .types import BeforeRequestContext, BeforeRequestHook


class TraceparentInjectionHook(BeforeRequestHook):
    """Inject a sampled W3C traceparent header on workflow execute requests.

    Forwards the current OTEL span context if one is active and sampled,
    otherwise generates a fresh sampled traceparent. This ensures worker traces
    are always recorded regardless of the caller's sampling configuration.
    """

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        if not request.url.path.endswith("/execute"):
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
