import json
import random
from typing import Any, Dict, Optional, Union

import httpx
from opentelemetry.propagate import inject

from .types import BeforeRequestContext, BeforeRequestHook


_EXECUTE_OPERATION_IDS = {
    "execute_workflow_v1_workflows__workflow_identifier__execute_post",
    "execute_workflow_registration_v1_workflows_registrations__workflow_registration_id__execute_post",
}

_SAMPLED_FLAG = 0x01


# https://www.w3.org/TR/trace-context/#traceparent-header
def _is_sampled(traceparent: str) -> bool:
    parts = traceparent.split("-")
    if len(parts) != 4:
        return False
    try:
        return bool(int(parts[3], 16) & _SAMPLED_FLAG)
    except ValueError:
        return False


def _json_body(request: httpx.Request) -> Optional[Dict[str, Any]]:
    if "application/json" not in request.headers.get("content-type", ""):
        return None
    try:
        body = json.loads(request.content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return body if isinstance(body, dict) else None


def _sampled_traceparent() -> str:
    carrier: Dict[str, str] = {}
    inject(carrier)
    traceparent = carrier.get("traceparent", "")
    if _is_sampled(traceparent):
        return traceparent
    return f"00-{random.getrandbits(128):032x}-{random.getrandbits(64):016x}-01"


class TraceparentInjectionHook(BeforeRequestHook):
    """Send a sampled traceparent on /execute requests so worker traces are always recorded.

    Sent in both the request body and the header. The body param is authoritative; the header is
    kept for API versions that predate it.
    """

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        if hook_ctx.operation_id not in _EXECUTE_OPERATION_IDS:
            return request

        body = _json_body(request)
        caller_traceparent = (body or {}).get("traceparent") or request.headers.get(
            "traceparent"
        )
        traceparent = caller_traceparent or _sampled_traceparent()

        request.headers["traceparent"] = traceparent

        if body is None or body.get("traceparent"):
            return request

        body["traceparent"] = traceparent
        content = json.dumps(body).encode("utf-8")
        headers = httpx.Headers(request.headers)
        headers["content-length"] = str(len(content))

        return httpx.Request(
            method=request.method,
            url=request.url,
            headers=headers,
            content=content,
            extensions=request.extensions,
        )
