import logging
import weakref
from typing import Any, Optional, Tuple, Union

import httpx
from opentelemetry import trace
from opentelemetry.trace import Span

from mistralai.extra.observability.otel import (
    get_or_create_otel_tracer,
    get_response_and_error,
    get_traced_request_and_span,
    get_traced_response,
)
from mistralai.extra.observability.telemetry import configure_telemetry_for_hook
from .types import (
    AfterErrorContext,
    AfterErrorHook,
    AfterSuccessContext,
    AfterSuccessHook,
    BeforeRequestContext,
    BeforeRequestHook,
)

logger = logging.getLogger(__name__)


_SPAN_EXT_KEY = "_tracing_span"


class TracingHook(BeforeRequestHook, AfterSuccessHook, AfterErrorHook):
    def __init__(self) -> None:
        self.tracer_provider: Optional[trace.TracerProvider] = None
        self._auto_telemetry_provider: Optional[Any] = None
        self._telemetry_finalizer: Optional[weakref.finalize] = None
        self._telemetry_auto_disabled: bool = False
        self.tracing_enabled, self.tracer = get_or_create_otel_tracer()

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        configure_telemetry_for_hook(
            self,
            hook_ctx.config,
            respect_global_provider=True,
        )
        # Refresh tracer/provider per request so tracing can be enabled if the
        # application configures OpenTelemetry after the client is instantiated.
        self.tracing_enabled, self.tracer = get_or_create_otel_tracer(
            provider=self.tracer_provider,
        )
        request, span = get_traced_request_and_span(
            tracing_enabled=self.tracing_enabled,
            tracer=self.tracer,
            span=None,
            operation_id=hook_ctx.operation_id,
            request=request,
        )
        request.extensions[_SPAN_EXT_KEY] = span
        return request

    @staticmethod
    def _get_span(response: Optional[httpx.Response]) -> Optional[Span]:
        try:
            return response.request.extensions.get(_SPAN_EXT_KEY) if response is not None else None
        except RuntimeError:
            return None

    def after_success(
        self, hook_ctx: AfterSuccessContext, response: httpx.Response
    ) -> Union[httpx.Response, Exception]:
        span = self._get_span(response)
        response = get_traced_response(
            tracing_enabled=self.tracing_enabled,
            tracer=self.tracer,
            span=span,
            operation_id=hook_ctx.operation_id,
            response=response,
        )
        return response

    def after_error(
        self,
        hook_ctx: AfterErrorContext,
        response: Optional[httpx.Response],
        error: Optional[Exception],
    ) -> Union[Tuple[Optional[httpx.Response], Optional[Exception]], Exception]:
        if response:
            span = self._get_span(response)
            response, error = get_response_and_error(
                tracing_enabled=self.tracing_enabled,
                tracer=self.tracer,
                span=span,
                operation_id=hook_ctx.operation_id,
                response=response,
                error=error,
            )
        return response, error
