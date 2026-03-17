"""OTEL conventions for gen AI may be found at:

https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/
https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/
"""

import copy
import json
import logging
import os
import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import httpx
import opentelemetry.semconv._incubating.attributes.gen_ai_attributes as gen_ai_attributes
import opentelemetry.semconv._incubating.attributes.http_attributes as http_attributes
import opentelemetry.semconv.attributes.error_attributes as error_attributes
import opentelemetry.semconv.attributes.server_attributes as server_attributes
from opentelemetry import context as context_api
from opentelemetry import propagate, trace
from opentelemetry.baggage import get_baggage
from opentelemetry.trace import Span, Status, StatusCode, Tracer, set_span_in_context

from .serialization import (
    serialize_input_message,
    serialize_output_message,
    serialize_tool_definition,
)
from .streaming import accumulate_chunks_to_response_dict, parse_sse_chunks

logger = logging.getLogger(__name__)


OTEL_SERVICE_NAME: str = "mistralai_sdk"
MISTRAL_SDK_OTEL_TRACER_NAME: str = OTEL_SERVICE_NAME + "_tracer"

MISTRAL_SDK_DEBUG_TRACING: bool = (
    os.getenv("MISTRAL_SDK_DEBUG_TRACING", "false").lower() == "true"
)
DEBUG_HINT: str = "To see detailed tracing logs, set MISTRAL_SDK_DEBUG_TRACING=true."


class MistralAIAttributes:
    MISTRAL_AI_OCR_USAGE_PAGES_PROCESSED = "mistral_ai.ocr.usage.pages_processed"
    MISTRAL_AI_OCR_USAGE_DOC_SIZE_BYTES = "mistral_ai.ocr.usage.doc_size_bytes"
    MISTRAL_AI_ERROR_CODE = "mistral_ai.error.code"


class MistralAINameValues(Enum):
    OCR = "ocr"


class TracingErrors(Exception, Enum):
    FAILED_TO_CREATE_SPAN_FOR_REQUEST = "Failed to create span for request."
    FAILED_TO_ENRICH_SPAN_WITH_RESPONSE = "Failed to enrich span with response."
    FAILED_TO_HANDLE_ERROR_IN_SPAN = "Failed to handle error in span."
    FAILED_TO_END_SPAN = "Failed to end span."

    def __str__(self):
        return str(self.value)


class GenAISpanEnum(str, Enum):
    CONVERSATION = "conversation"
    VALIDATE_RUN = "validate_run"


def parse_time_to_nanos(ts: str) -> int:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    return int(dt.timestamp() * 1e9)


def _infer_gen_ai_operation_name(
    operation_id: str,
) -> gen_ai_attributes.GenAiOperationNameValues | None:
    """Infer the GenAI operation name from the operation_id using rule-based matching."""
    if "chat_completion" in operation_id or operation_id == "stream_chat":
        return gen_ai_attributes.GenAiOperationNameValues.CHAT
    if (
        "agents_create" in operation_id or "agents_update" in operation_id
    ) and "alias" not in operation_id:
        return gen_ai_attributes.GenAiOperationNameValues.CREATE_AGENT
    if "agents_completion" in operation_id or operation_id == "stream_agents":
        return gen_ai_attributes.GenAiOperationNameValues.INVOKE_AGENT
    if "conversations" in operation_id and any(
        action in operation_id for action in ("start", "append", "restart")
    ):
        return gen_ai_attributes.GenAiOperationNameValues.INVOKE_AGENT
    if "fim" in operation_id:
        return gen_ai_attributes.GenAiOperationNameValues.TEXT_COMPLETION
    if "embeddings" in operation_id:
        return gen_ai_attributes.GenAiOperationNameValues.EMBEDDINGS
    if "ocr_post" in operation_id:
        return gen_ai_attributes.GenAiOperationNameValues.GENERATE_CONTENT
    # TODO: Handle transcriptions (audio_api_v1_transcriptions_post[_stream])
    return None


def _build_genai_span_name(
    gen_ai_op: gen_ai_attributes.GenAiOperationNameValues, body: dict[str, Any]
) -> str:
    """Build span name per GenAI semantic conventions.

    - Chat/text_completion/embeddings: "{operation_name} {model}"
    - create_agent/invoke_agent: "{operation_name} {agent_name}"
    - execute_tool: "execute_tool {gen_ai.tool.name}"
    """
    op_name = gen_ai_op.value
    if gen_ai_op in {
        gen_ai_attributes.GenAiOperationNameValues.CREATE_AGENT,
        gen_ai_attributes.GenAiOperationNameValues.INVOKE_AGENT,
    }:
        agent_name = body.get("name", "")
        return f"{op_name} {agent_name}" if agent_name else op_name
    if gen_ai_op is gen_ai_attributes.GenAiOperationNameValues.EXECUTE_TOOL:
        tool_name = body.get("name", "")
        return f"{op_name} {tool_name}" if tool_name else op_name
    model = body.get("model", "")
    return f"{op_name} {model}" if model else op_name


def set_available_attributes(span: Span, attributes: dict[str, Any]) -> None:
    for attribute, value in attributes.items():
        if value:
            span.set_attribute(attribute, value)


def _set_http_attributes(span: Span, operation_id: str, request: httpx.Request) -> None:
    """Set HTTP and server attributes on the span."""
    if not request.url.port:
        # From httpx doc:
        # Note that the URL class performs port normalization as per the WHATWG spec.
        # Default ports for "http", "https", "ws", "wss", and "ftp" schemes are always treated as None.
        # Handling default ports since most of the time we are using https
        if request.url.scheme == "https":
            port = 443
        elif request.url.scheme == "http":
            port = 80
        else:
            port = -1
    else:
        port = request.url.port

    span.set_attributes(
        {
            http_attributes.HTTP_REQUEST_METHOD: request.method,
            http_attributes.HTTP_URL: str(request.url),
            server_attributes.SERVER_ADDRESS: request.headers.get("host", ""),
            server_attributes.SERVER_PORT: port,
        }
    )


def _enrich_request_genai_attrs(
    span: Span,
    gen_ai_op: gen_ai_attributes.GenAiOperationNameValues,
    request_body: dict[str, Any],
) -> None:
    """Set GenAI request attributes: model params, input messages, tool definitions."""
    # Update span name per GenAI semantic conventions, now that we have the parsed request body.
    span.update_name(_build_genai_span_name(gen_ai_op, request_body))

    attributes = {
        gen_ai_attributes.GEN_AI_REQUEST_CHOICE_COUNT: request_body.get("n"),
        gen_ai_attributes.GEN_AI_REQUEST_ENCODING_FORMATS: request_body.get(
            "encoding_formats"
        ),
        gen_ai_attributes.GEN_AI_REQUEST_FREQUENCY_PENALTY: request_body.get(
            "frequency_penalty"
        ),
        gen_ai_attributes.GEN_AI_REQUEST_MAX_TOKENS: request_body.get("max_tokens"),
        gen_ai_attributes.GEN_AI_REQUEST_MODEL: request_body.get("model"),
        gen_ai_attributes.GEN_AI_REQUEST_PRESENCE_PENALTY: request_body.get(
            "presence_penalty"
        ),
        gen_ai_attributes.GEN_AI_REQUEST_SEED: request_body.get("random_seed"),
        gen_ai_attributes.GEN_AI_REQUEST_STOP_SEQUENCES: request_body.get("stop"),
        gen_ai_attributes.GEN_AI_REQUEST_TEMPERATURE: request_body.get("temperature"),
        gen_ai_attributes.GEN_AI_REQUEST_TOP_P: request_body.get("top_p"),
        gen_ai_attributes.GEN_AI_REQUEST_TOP_K: request_body.get("top_k"),
    }

    # Chat/agent completion API uses messages in request body; conversation API uses inputs
    input_messages = request_body.get("messages") or request_body.get("inputs")
    if isinstance(input_messages, str):
        attributes[gen_ai_attributes.GEN_AI_INPUT_MESSAGES] = [
            serialize_input_message({"role": "user", "content": input_messages})
        ]
    elif isinstance(input_messages, list):
        attributes[gen_ai_attributes.GEN_AI_INPUT_MESSAGES] = list(
            map(serialize_input_message, input_messages)
        )
    # Tool definitions
    if tools := request_body.get("tools"):
        attributes[gen_ai_attributes.GEN_AI_TOOL_DEFINITIONS] = list(
            filter(None, map(serialize_tool_definition, tools))
        )
    # TODO: For agent start conversation, add agent id and version attributes here ?

    set_available_attributes(span, attributes)


def enrich_span_from_request(
    span: Span, operation_id: str, request: httpx.Request
) -> Span:
    _set_http_attributes(span, operation_id, request)

    gen_ai_op = _infer_gen_ai_operation_name(operation_id)
    if gen_ai_op is None:
        return span

    span.set_attributes(
        {
            gen_ai_attributes.GEN_AI_OPERATION_NAME: gen_ai_op.value,
            gen_ai_attributes.GEN_AI_PROVIDER_NAME: gen_ai_attributes.GenAiProviderNameValues.MISTRAL_AI.value,
        }
    )

    if request.content:
        request_body = json.loads(request.content)
        _enrich_request_genai_attrs(span, gen_ai_op, request_body)

    return span


def _enrich_response_genai_attrs(
    span: Span,
    gen_ai_op: gen_ai_attributes.GenAiOperationNameValues,
    response_data: dict[str, Any],
) -> None:
    """Set common GenAI response attributes: response ID, model, choices, usage."""
    attributes: dict[str, Any] = {}

    if gen_ai_op is not gen_ai_attributes.GenAiOperationNameValues.CREATE_AGENT:
        # id has another meaning for create agent operation (id of the agent)
        attributes[gen_ai_attributes.GEN_AI_RESPONSE_ID] = response_data.get("id")
    attributes[gen_ai_attributes.GEN_AI_RESPONSE_MODEL] = response_data.get("model")

    # Finish reasons and output messages from choices
    choices = response_data.get("choices", [])
    finish_reasons = [c.get("finish_reason") for c in choices if c.get("finish_reason")]
    if finish_reasons:
        attributes[gen_ai_attributes.GEN_AI_RESPONSE_FINISH_REASONS] = finish_reasons
    if choices:
        attributes[gen_ai_attributes.GEN_AI_OUTPUT_MESSAGES] = list(
            map(serialize_output_message, choices)
        )

    # Usage
    usage = response_data.get("usage", {})
    if usage:
        attributes.update(
            {
                gen_ai_attributes.GEN_AI_USAGE_INPUT_TOKENS: usage.get(
                    "prompt_tokens", 0
                ),
                gen_ai_attributes.GEN_AI_USAGE_OUTPUT_TOKENS: usage.get(
                    "completion_tokens", 0
                ),
            }
        )

    set_available_attributes(span, attributes)


def _enrich_create_agent(span: Span, response_data: dict[str, Any]) -> None:
    """Set agent-specific attributes from create_agent response.

    Semantics: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/#create-agent-span
    """
    agent_attributes = {
        gen_ai_attributes.GEN_AI_AGENT_DESCRIPTION: response_data.get("description"),
        gen_ai_attributes.GEN_AI_AGENT_ID: response_data.get("id"),
        gen_ai_attributes.GEN_AI_AGENT_NAME: response_data.get("name"),
        # As of 2026-03-02: in convention, but not yet in opentelemetry-semantic-conventions
        "gen_ai.agent.version": str(response_data.get("version")),
        gen_ai_attributes.GEN_AI_REQUEST_MODEL: response_data.get("model"),
        gen_ai_attributes.GEN_AI_SYSTEM_INSTRUCTIONS: response_data.get("instructions"),
    }
    set_available_attributes(span, agent_attributes)


def _create_tool_execution_child_span(
    tracer: trace.Tracer, parent_context: context_api.Context, output: dict[str, Any]
) -> None:
    """Create a child span for a tool.execution conversation output."""
    start_ns = parse_time_to_nanos(output["created_at"])
    end_ns = parse_time_to_nanos(output["completed_at"])
    op_name = gen_ai_attributes.GenAiOperationNameValues.EXECUTE_TOOL
    span_name = _build_genai_span_name(op_name, output)
    child_span = tracer.start_span(
        span_name, start_time=start_ns, context=parent_context
    )
    child_span.set_attributes({"agent.trace.public": ""})
    tool_arguments = output.get("arguments")
    # The tool call result is in the "info" field, if provided
    tool_result = output.get("info")
    tool_attributes = {
        gen_ai_attributes.GEN_AI_OPERATION_NAME: op_name.value,
        gen_ai_attributes.GEN_AI_PROVIDER_NAME: gen_ai_attributes.GenAiProviderNameValues.MISTRAL_AI.value,
        gen_ai_attributes.GEN_AI_TOOL_CALL_ID: output.get("id"),
        gen_ai_attributes.GEN_AI_TOOL_CALL_ARGUMENTS: tool_arguments
        if isinstance(tool_arguments, str)
        else (json.dumps(tool_arguments) if tool_arguments else None),
        gen_ai_attributes.GEN_AI_TOOL_CALL_RESULT: tool_result
        and json.dumps(tool_result),
        gen_ai_attributes.GEN_AI_TOOL_NAME: output.get("name"),
        gen_ai_attributes.GEN_AI_TOOL_TYPE: "extension",
    }
    set_available_attributes(child_span, tool_attributes)
    child_span.end(end_time=end_ns)


def _create_message_output_child_span(
    tracer: trace.Tracer, parent_context: context_api.Context, output: dict[str, Any]
) -> None:
    """Create a child span for a message.output conversation output."""
    start_ns = parse_time_to_nanos(output["created_at"])
    end_ns = parse_time_to_nanos(output["completed_at"])
    op_name = gen_ai_attributes.GenAiOperationNameValues.CHAT
    span_name = _build_genai_span_name(op_name, output)
    child_span = tracer.start_span(
        span_name, start_time=start_ns, context=parent_context
    )
    child_span.set_attributes({"agent.trace.public": ""})
    # Wrap the flat conversation output as a choice dict so we
    # can reuse serialize_output_message (which also handles
    # tool_calls, not just content).
    choice_wrapper: dict = {
        "message": output,
        "finish_reason": output.get("finish_reason", ""),
    }
    message_attributes = {
        gen_ai_attributes.GEN_AI_OPERATION_NAME: op_name.value,
        gen_ai_attributes.GEN_AI_PROVIDER_NAME: gen_ai_attributes.GenAiProviderNameValues.MISTRAL_AI.value,
        gen_ai_attributes.GEN_AI_RESPONSE_ID: output.get("id"),
        gen_ai_attributes.GEN_AI_AGENT_ID: output.get("agent_id"),
        gen_ai_attributes.GEN_AI_RESPONSE_MODEL: output.get("model"),
        gen_ai_attributes.GEN_AI_OUTPUT_MESSAGES: [
            serialize_output_message(choice_wrapper)
        ],
    }
    set_available_attributes(child_span, message_attributes)
    child_span.end(end_time=end_ns)


def _enrich_invoke_agent(
    tracer: trace.Tracer, span: Span, response_data: dict[str, Any]
) -> None:
    """Set invoke_agent attributes and create child spans for conversation outputs."""
    conversation_attributes = {
        gen_ai_attributes.GEN_AI_CONVERSATION_ID: response_data.get("conversation_id"),
        # We don't have more agent attributes available in the response data
        # (agent id, name, version, description). For start conversation operation,
        # we could get it from the request; see associated TODO
    }
    set_available_attributes(span, conversation_attributes)

    outputs = response_data.get("outputs", [])
    parent_context = set_span_in_context(span)
    for output in outputs:
        output_type = output.get("type")
        if not output_type:
            continue  # Safety net
        if output_type == "function.call":
            # handled in the extra.run.tools.create_function_result function
            continue
        elif output_type == "tool.execution":
            _create_tool_execution_child_span(tracer, parent_context, output)
        elif output_type == "message.output":
            _create_message_output_child_span(tracer, parent_context, output)
        # TODO: do type agent.handoff


def _enrich_ocr(span: Span, response_data: dict[str, Any]) -> None:
    """Set OCR-specific usage attributes."""
    usage_info = response_data.get("usage_info", {})
    ocr_attributes = {
        MistralAIAttributes.MISTRAL_AI_OCR_USAGE_PAGES_PROCESSED: usage_info.get(
            "pages_processed"
        ),
        MistralAIAttributes.MISTRAL_AI_OCR_USAGE_DOC_SIZE_BYTES: usage_info.get(
            "doc_size_bytes"
        ),
    }
    set_available_attributes(span, ocr_attributes)


def _enrich_span_from_response(
    tracer: Tracer,
    span: Span,
    operation_id: str,
    response_data: dict[str, Any],
) -> None:
    """Enrich span with GenAI response attributes and operation-specific data.

    Used by both the non-streaming and streaming paths so that the same
    attributes are set regardless of response type.
    """
    gen_ai_op = _infer_gen_ai_operation_name(operation_id)
    if gen_ai_op is None:
        return

    _enrich_response_genai_attrs(span, gen_ai_op, response_data)

    if gen_ai_op is gen_ai_attributes.GenAiOperationNameValues.CREATE_AGENT:
        _enrich_create_agent(span, response_data)
    elif gen_ai_op is gen_ai_attributes.GenAiOperationNameValues.INVOKE_AGENT:
        _enrich_invoke_agent(tracer, span, response_data)

    if operation_id == "ocr_v1_ocr_post":
        _enrich_ocr(span, response_data)


def get_or_create_otel_tracer() -> tuple[bool, Tracer]:
    """
    Get a tracer from the current TracerProvider.

    The SDK does not set up its own TracerProvider - it relies on the application
    to configure OpenTelemetry. This follows OTEL best practices where:
    - Libraries/SDKs get tracers from the global provider
    - Applications configure the TracerProvider

    If no TracerProvider is configured, the ProxyTracerProvider (default) will
    return a NoOp tracer, effectively disabling tracing. Once the application
    sets up a real TracerProvider, subsequent spans will be recorded.

    Returns:
        Tuple[bool, Tracer]: (tracing_enabled, tracer)
            - tracing_enabled is True if a real TracerProvider is configured
            - tracer is always valid (may be NoOp if no provider configured)
    """
    tracer_provider = trace.get_tracer_provider()
    tracer = tracer_provider.get_tracer(MISTRAL_SDK_OTEL_TRACER_NAME)

    # Tracing is considered enabled if we have a real TracerProvider (not the default proxy)
    tracing_enabled = not isinstance(tracer_provider, trace.ProxyTracerProvider)

    return tracing_enabled, tracer


def get_traced_request_and_span(
    tracing_enabled: bool,
    tracer: Tracer,
    span: Span | None,
    operation_id: str,
    request: httpx.Request,
) -> tuple[httpx.Request, Span | None]:
    if not tracing_enabled:
        return request, span

    try:
        span = tracer.start_span(name=operation_id)
        span.set_attributes({"agent.trace.public": ""})
        # Propagate gen_ai.conversation.id from OTEL baggage if present
        conversation_id = get_baggage(gen_ai_attributes.GEN_AI_CONVERSATION_ID)
        if conversation_id:
            span.set_attribute(
                gen_ai_attributes.GEN_AI_CONVERSATION_ID, str(conversation_id)
            )
        # Inject the span context into the request headers to be used by the backend service to continue the trace
        propagate.inject(request.headers, context=set_span_in_context(span))
        span = enrich_span_from_request(span, operation_id, request)
    except Exception:
        logger.warning(
            "%s %s",
            TracingErrors.FAILED_TO_CREATE_SPAN_FOR_REQUEST,
            traceback.format_exc() if MISTRAL_SDK_DEBUG_TRACING else DEBUG_HINT,
        )
        if span:
            end_span(span=span)
        span = None

    return request, span


def get_traced_response(
    tracing_enabled: bool,
    tracer: Tracer,
    span: Span | None,
    operation_id: str,
    response: httpx.Response,
) -> httpx.Response:
    if not tracing_enabled or not span:
        return response
    try:
        span.set_status(Status(StatusCode.OK))
        span.set_attribute(
            http_attributes.HTTP_RESPONSE_STATUS_CODE, response.status_code
        )
        is_stream_response = not response.is_closed and not response.is_stream_consumed
        if is_stream_response:
            return TracedResponse.from_response(
                resp=response, span=span, tracer=tracer, operation_id=operation_id
            )
        if response.content:
            response_data = json.loads(response.content)
            _enrich_span_from_response(tracer, span, operation_id, response_data)
    except Exception:
        logger.warning(
            "%s %s",
            TracingErrors.FAILED_TO_ENRICH_SPAN_WITH_RESPONSE,
            traceback.format_exc() if MISTRAL_SDK_DEBUG_TRACING else DEBUG_HINT,
        )
    if span:
        end_span(span=span)
    return response


def get_response_and_error(
    tracing_enabled: bool,
    tracer: Tracer,
    span: Span | None,
    operation_id: str,
    response: httpx.Response,
    error: Exception | None,
) -> tuple[httpx.Response, Exception | None]:
    if not tracing_enabled or not span:
        return response, error
    try:
        if error:
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, str(error)))
        if response.content:
            response_body = json.loads(response.content)
            if response_body.get("object", "") == "error":
                if error_msg := response_body.get("message", ""):
                    error_type = response_body.get("type", "")
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                    span.add_event(
                        "exception",
                        {
                            "exception.type": error_type or "api_error",
                            "exception.message": error_msg,
                        },
                    )
                    attributes = {
                        http_attributes.HTTP_RESPONSE_STATUS_CODE: response.status_code,
                        error_attributes.ERROR_TYPE: error_type,
                        MistralAIAttributes.MISTRAL_AI_ERROR_CODE: response_body.get(
                            "code", ""
                        ),
                    }
                    for attribute, value in attributes.items():
                        if value:
                            span.set_attribute(attribute, value)
        span.end()
        span = None
    except Exception:
        logger.warning(
            "%s %s",
            TracingErrors.FAILED_TO_HANDLE_ERROR_IN_SPAN,
            traceback.format_exc() if MISTRAL_SDK_DEBUG_TRACING else DEBUG_HINT,
        )

        if span:
            span.end()
            span = None
    return response, error


def end_span(span: Span) -> None:
    try:
        span.end()
    except Exception:
        logger.warning(
            "%s %s",
            TracingErrors.FAILED_TO_END_SPAN,
            traceback.format_exc() if MISTRAL_SDK_DEBUG_TRACING else DEBUG_HINT,
        )


class TracedResponse(httpx.Response):
    """Subclass of httpx.Response that accumulates streamed SSE bytes and
    enriches the OTEL span with response attributes when the stream is closed.
    """

    span: Span | None
    tracer: Tracer
    operation_id: str
    _accumulated_sse: bytearray

    def __init__(
        self,
        *args,
        span: Span | None,
        tracer: Tracer,
        operation_id: str = "",
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.span = span
        self.tracer = tracer
        self.operation_id = operation_id
        self._accumulated_sse = bytearray()

    def iter_bytes(self, *args, **kwargs):
        for chunk in super().iter_bytes(*args, **kwargs):
            self._accumulated_sse.extend(chunk)
            yield chunk

    async def aiter_bytes(self, *args, **kwargs):
        async for chunk in super().aiter_bytes(*args, **kwargs):
            self._accumulated_sse.extend(chunk)
            yield chunk

    def close(self) -> None:
        self._finalize_span()
        super().close()

    async def aclose(self) -> None:
        self._finalize_span()
        await super().aclose()

    def _finalize_span(self) -> None:
        """Enrich and end the span after the stream has been fully consumed."""
        if not self.span:
            return
        try:
            chunks = parse_sse_chunks(bytes(self._accumulated_sse))
            if chunks:
                response_data = accumulate_chunks_to_response_dict(chunks)
                _enrich_span_from_response(
                    self.tracer, self.span, self.operation_id, response_data
                )
        except Exception:
            logger.warning(
                "%s %s",
                TracingErrors.FAILED_TO_ENRICH_SPAN_WITH_RESPONSE,
                traceback.format_exc() if MISTRAL_SDK_DEBUG_TRACING else DEBUG_HINT,
            )
        end_span(span=self.span)
        self.span = None

    @classmethod
    def from_response(
        cls,
        resp: httpx.Response,
        span: Span | None,
        tracer: Tracer,
        operation_id: str = "",
    ) -> "TracedResponse":
        # Bypass __init__ to steal the live httpx stream/connection via __dict__ copy.
        # Keep tracing field assignments in sync with __init__.
        traced_resp = cls.__new__(cls)
        traced_resp.__dict__ = copy.copy(resp.__dict__)
        traced_resp.span = span
        traced_resp.tracer = tracer
        traced_resp.operation_id = operation_id
        traced_resp._accumulated_sse = bytearray()

        return traced_resp
