import logging
import threading
import weakref
from functools import wraps
from typing import Any, Optional, Tuple, Union

import httpx
from opentelemetry import context as context_api
from opentelemetry import trace
from opentelemetry.trace import Span, Status, StatusCode, set_span_in_context

from mistralai.extra.observability.otel import (
    TracedResponse,
    end_span,
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
_SPAN_CONTEXT_EXT_KEY = "_tracing_span_context"
_SPAN_FINISHED_EXT_KEY = "_tracing_span_finished"
_SYNC_SEND_WRAPPED_ATTR = "_mistral_tracing_sync_send_wrapped"
_ASYNC_SEND_WRAPPED_ATTR = "_mistral_tracing_async_send_wrapped"
_WRAP_LOCK = threading.Lock()


class TracingHook(BeforeRequestHook, AfterSuccessHook, AfterErrorHook):
    def __init__(self) -> None:
        self.tracer_provider: Optional[trace.TracerProvider] = None
        self._auto_telemetry_provider: Optional[Any] = None
        self._telemetry_finalizer: Optional[weakref.finalize] = None
        self._telemetry_auto_disabled: bool = False
        self._telemetry_use_global_provider: bool = False
        self.tracing_enabled, self.tracer = get_or_create_otel_tracer()

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        telemetry_configured = configure_telemetry_for_hook(
            self,
            hook_ctx.config,
            respect_global_provider=True,
        )
        should_trace = (
            telemetry_configured
            or self.tracer_provider is not None
            or self._telemetry_use_global_provider
        )
        if should_trace:
            # Refresh tracer/provider per request so tracing can be enabled if the
            # application configures OpenTelemetry after the client is instantiated.
            self.tracing_enabled, self.tracer = get_or_create_otel_tracer(
                provider=self.tracer_provider,
            )
        else:
            self.tracing_enabled = False
        request, span = get_traced_request_and_span(
            tracing_enabled=self.tracing_enabled,
            tracer=self.tracer,
            span=None,
            operation_id=hook_ctx.operation_id,
            request=request,
        )
        self._store_span_on_request(request, span)
        # The GenAI span is created in this hook, but HTTPX creates its own
        # auto-instrumented span later inside send(). Wrap the configured
        # clients so each request's stored GenAI span is current only while
        # that request is being sent.
        if span is not None:
            self._ensure_client_send_wrapped(getattr(hook_ctx.config, "client", None))
            self._ensure_async_client_send_wrapped(
                getattr(hook_ctx.config, "async_client", None)
            )
        return request

    @staticmethod
    def _get_span(response: Optional[httpx.Response]) -> Optional[Span]:
        try:
            if response is None:
                return None
            return response.request.extensions.get(_SPAN_EXT_KEY)
        except RuntimeError:
            return None

    @staticmethod
    def _store_span_on_request(request: httpx.Request, span: Optional[Span]) -> None:
        request.extensions[_SPAN_EXT_KEY] = span
        request.extensions[_SPAN_FINISHED_EXT_KEY] = False
        if span:
            request.extensions[_SPAN_CONTEXT_EXT_KEY] = set_span_in_context(span)
            return
        request.extensions.pop(_SPAN_CONTEXT_EXT_KEY, None)

    @staticmethod
    def _get_request_span(request: httpx.Request) -> Optional[Span]:
        try:
            return request.extensions.get(_SPAN_EXT_KEY)
        except RuntimeError:
            return None

    @staticmethod
    def _mark_span_finished(request: httpx.Request) -> None:
        try:
            request.extensions[_SPAN_FINISHED_EXT_KEY] = True
            request.extensions[_SPAN_EXT_KEY] = None
        except RuntimeError:
            return

    @staticmethod
    def _attach_request_span_context(request: httpx.Request):
        try:
            span_context = request.extensions.get(_SPAN_CONTEXT_EXT_KEY)
        except RuntimeError:
            return None
        if span_context is None:
            return None
        return context_api.attach(span_context)

    @staticmethod
    def _detach_request_span_context(token) -> None:
        if token is not None:
            context_api.detach(token)

    @classmethod
    def _finish_request_span_with_error(
        cls, request: httpx.Request, error: Exception
    ) -> None:
        try:
            if request.extensions.get(_SPAN_FINISHED_EXT_KEY):
                return
        except RuntimeError:
            return

        span = cls._get_request_span(request)
        if not span:
            return

        try:
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, str(error)))
        finally:
            end_span(span)
            cls._mark_span_finished(request)

    @classmethod
    def _ensure_client_send_wrapped(cls, client: Any) -> None:
        if client is None or getattr(client, _SYNC_SEND_WRAPPED_ATTR, False):
            return

        with _WRAP_LOCK:
            if getattr(client, _SYNC_SEND_WRAPPED_ATTR, False):
                return

            original_send = client.send

            @wraps(original_send)
            def traced_send(request: httpx.Request, *args, **kwargs):
                token = cls._attach_request_span_context(request)
                try:
                    return original_send(request, *args, **kwargs)
                except Exception as exc:
                    cls._finish_request_span_with_error(request, exc)
                    raise
                finally:
                    cls._detach_request_span_context(token)

            try:
                client.send = traced_send
                setattr(client, _SYNC_SEND_WRAPPED_ATTR, True)
            except Exception:
                logger.debug("Failed to wrap sync HTTP client for tracing.")

    @classmethod
    def _ensure_async_client_send_wrapped(cls, async_client: Any) -> None:
        if async_client is None or getattr(
            async_client, _ASYNC_SEND_WRAPPED_ATTR, False
        ):
            return

        with _WRAP_LOCK:
            if getattr(async_client, _ASYNC_SEND_WRAPPED_ATTR, False):
                return

            original_send = async_client.send

            @wraps(original_send)
            async def traced_send(request: httpx.Request, *args, **kwargs):
                token = cls._attach_request_span_context(request)
                try:
                    return await original_send(request, *args, **kwargs)
                except Exception as exc:
                    cls._finish_request_span_with_error(request, exc)
                    raise
                finally:
                    cls._detach_request_span_context(token)

            try:
                async_client.send = traced_send
                setattr(async_client, _ASYNC_SEND_WRAPPED_ATTR, True)
            except Exception:
                logger.debug("Failed to wrap async HTTP client for tracing.")

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
        if span and not isinstance(response, TracedResponse):
            self._mark_span_finished(response.request)
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
            if span and response:
                self._mark_span_finished(response.request)
        return response, error
