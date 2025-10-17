from .types import (
    AfterErrorContext,
    AfterErrorHook,
    AfterSuccessContext,
    AfterSuccessHook,
    BeforeRequestContext,
    BeforeRequestHook,
)
from ..extra.observability.otel import (
    get_traced_request_and_span,
    get_traced_response,
    get_response_and_error,
    get_or_create_otel_tracer,
)

from opentelemetry.trace import Span
from typing import Optional, Tuple, Union

import httpx
import logging

logger = logging.getLogger(__name__)


class TracingHook(BeforeRequestHook, AfterSuccessHook, AfterErrorHook):
    def __init__(self) -> None:
        self.tracing_enabled, self.tracer = get_or_create_otel_tracer()
        self.request_span: Optional[Span] = None

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        request, self.request_span = get_traced_request_and_span(tracing_enabled=self.tracing_enabled, tracer=self.tracer, span=self.request_span, operation_id=hook_ctx.operation_id, request=request)
        return request

    def after_success(
        self, hook_ctx: AfterSuccessContext, response: httpx.Response
    ) -> Union[httpx.Response, Exception]:
        response = get_traced_response(tracing_enabled=self.tracing_enabled, tracer=self.tracer, span=self.request_span, operation_id=hook_ctx.operation_id, response=response)
        return response

    def after_error(
        self,
        hook_ctx: AfterErrorContext,
        response: Optional[httpx.Response],
        error: Optional[Exception],
    ) -> Union[Tuple[Optional[httpx.Response], Optional[Exception]], Exception]:
        if response:
            response, error = get_response_and_error(tracing_enabled=self.tracing_enabled, tracer=self.tracer, span=self.request_span, operation_id=hook_ctx.operation_id, response=response, error=error)
        return response, error
