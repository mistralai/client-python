"""Tests for OTEL tracing instrumentation.

Each test drives the real TracingHook lifecycle (before_request → after_success)
with realistic Mistral API payloads and verifies the resulting OTEL span attributes
match GenAI semantic conventions.

Fixtures are defined inline using SDK model classes so each test is self-contained.
"""

# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportArgumentType=false

import asyncio
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

import httpx
from opentelemetry import context as context_api
from opentelemetry import trace
from opentelemetry.baggage import set_baggage
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import StatusCode

from mistralai.client._hooks.tracing import TracingHook
from mistralai.client._hooks.types import (
    AfterErrorContext,
    AfterSuccessContext,
    BeforeRequestContext,
    HookContext,
)
from mistralai.client.models import (
    Agent,
    AgentsCompletionRequest,
    AssistantMessage,
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionChunk,
    CompletionEvent,
    CompletionResponseStreamChoice,
    ConversationAppendRequest,
    ConversationRequest,
    ConversationResponse,
    ConversationUsageInfo,
    CreateAgentRequest,
    DeltaMessage,
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingResponseData,
    Function,
    FunctionCall,
    FunctionCallEntry,
    FunctionResultEntry,
    FunctionTool,
    ImageURL,
    ImageURLChunk,
    MessageOutputEntry,
    SystemMessage,
    TextChunk,
    ThinkChunk,
    Tool,
    ToolCall,
    ToolExecutionEntry,
    ToolMessage,
    UsageInfo,
    UserMessage,
)
from mistralai.extra.observability.otel import TracedResponse
from mistralai.extra.run.tools import (
    RunFunction,
    create_function_result,
)

# Set up a single TracerProvider for the entire test module.
# trace.set_tracer_provider() can only be called once per process.
_EXPORTER = InMemorySpanExporter()
_PROVIDER = TracerProvider()
_PROVIDER.add_span_processor(SimpleSpanProcessor(_EXPORTER))
trace.set_tracer_provider(_PROVIDER)


# -- Helpers -------------------------------------------------------------------


def _make_httpx_request(
    body: dict,
    method: str = "POST",
    url: str = "https://api.mistral.ai/v1/chat/completions",
) -> httpx.Request:
    return httpx.Request(
        method=method,
        url=url,
        content=json.dumps(body).encode(),
        headers={"host": "api.mistral.ai", "content-type": "application/json"},
    )


def _make_httpx_response(body: dict, status_code: int = 200) -> httpx.Response:
    resp = httpx.Response(
        status_code=status_code,
        content=json.dumps(body).encode(),
    )
    # Mark the response as closed/consumed so it's treated as non-streaming
    resp.stream = httpx.ByteStream(resp.content)
    resp.stream.close()
    return resp


def _make_hook_context(operation_id: str) -> HookContext:
    return HookContext(
        config=MagicMock(),
        base_url="https://api.mistral.ai",
        operation_id=operation_id,
        oauth2_scopes=None,
        security_source=None,
    )


def _dump(model) -> dict:
    """Serialize an SDK model to a JSON-compatible dict, matching wire format."""
    return model.model_dump(mode="json", by_alias=True)


def _build_sse_body(events: list[CompletionEvent]) -> bytes:
    """Serialize a list of CompletionEvent models into an SSE byte payload."""
    lines = [f"data: {json.dumps(_dump(e.data))}" for e in events]
    lines.append("data: [DONE]")
    return ("\n\n".join(lines) + "\n\n").encode()


def _make_streaming_httpx_response(sse_body: bytes) -> httpx.Response:
    """Create an *open* httpx.Response that simulates a streaming SSE response."""
    return httpx.Response(
        status_code=200,
        stream=httpx.ByteStream(sse_body),
    )


def _parse_json_list(span_attr):
    """Parse a span attribute containing a list of JSON-encoded strings."""
    return [json.loads(m) for m in span_attr]


# -- Tests ---------------------------------------------------------------------


class TestOtelTracing(unittest.TestCase):
    def setUp(self):
        _EXPORTER.clear()

    # -- Test helpers ----------------------------------------------------------

    def _run_hook_lifecycle(
        self,
        operation_id: str,
        request_body,
        response_body,
        streaming: bool = False,
    ):
        """Drive the real TracingHook: before_request → after_success.

        ``request_body`` and ``response_body`` can be SDK model instances or
        plain dicts.  Models are serialised via ``_dump()`` automatically.

        When ``streaming=True``, ``response_body`` must be a
        ``list[CompletionEvent]``.  The helper builds an SSE byte payload,
        creates an open streaming response, and consumes + closes the stream
        so the span is finalised before returning.
        """
        hook = TracingHook()
        hook_ctx = _make_hook_context(operation_id)

        req_dict = (
            _dump(request_body) if hasattr(request_body, "model_dump") else request_body
        )

        request = _make_httpx_request(req_dict)

        if streaming:
            sse_body = _build_sse_body(response_body)
            response = _make_streaming_httpx_response(sse_body)
        else:
            resp_dict = (
                _dump(response_body)
                if hasattr(response_body, "model_dump")
                else response_body
            )
            response = _make_httpx_response(resp_dict)

        hooked_request = hook.before_request(BeforeRequestContext(hook_ctx), request)
        self.assertNotIsInstance(hooked_request, Exception)
        assert isinstance(hooked_request, httpx.Request)

        result = hook.after_success(AfterSuccessContext(hook_ctx), response)
        self.assertNotIsInstance(result, Exception)

        if streaming:
            self.assertIsInstance(result, TracedResponse)
            assert isinstance(result, TracedResponse)
            for _chunk in result.iter_bytes():
                pass
            result.close()

    def _run_hook_error_lifecycle(
        self,
        operation_id: str,
        request_body,
        response_body: dict,
        status_code: int = 400,
        error: Exception | None = None,
    ):
        """Drive the real TracingHook: before_request → after_error."""
        hook = TracingHook()
        hook_ctx = _make_hook_context(operation_id)

        req_dict = (
            _dump(request_body) if hasattr(request_body, "model_dump") else request_body
        )
        request = _make_httpx_request(req_dict)
        response = _make_httpx_response(response_body, status_code=status_code)

        hooked_request = hook.before_request(BeforeRequestContext(hook_ctx), request)
        self.assertNotIsInstance(hooked_request, Exception)
        assert isinstance(hooked_request, httpx.Request)

        result = hook.after_error(AfterErrorContext(hook_ctx), response, error)
        self.assertNotIsInstance(result, Exception)

    def _get_finished_spans(self):
        return _EXPORTER.get_finished_spans()

    def _get_single_span(self):
        spans = self._get_finished_spans()
        self.assertEqual(len(spans), 1, f"Expected 1 span, got {len(spans)}")
        return spans[0]

    def assertSpanAttributes(self, span, expected: dict):
        """Assert that *expected* is a subset of *span.attributes*."""
        actual = {k: span.attributes[k] for k in expected}
        self.assertEqual(expected, actual)

    # -- Simple chat completion ------------------------------------------------

    def test_simple_chat_completion(self):
        request = ChatCompletionRequest(
            model="mistral-large-latest",
            temperature=0.7,
            top_p=1,
            max_tokens=512,
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="What is the best French cheese?"),
            ],
        )
        response = ChatCompletionResponse(
            id="cmpl-a1b2c3d4e5f6",
            object="chat.completion",
            model="mistral-large-latest",
            created=1700000000,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="There are many great French cheeses! Camembert, Roquefort, and Brie are among the most celebrated.",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=20, completion_tokens=25, total_tokens=45),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "chat mistral-large-latest")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "chat",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.request.model": "mistral-large-latest",
                "gen_ai.request.temperature": 0.7,
                "gen_ai.request.top_p": 1,
                "gen_ai.request.max_tokens": 512,
                "http.request.method": "POST",
                "server.address": "api.mistral.ai",
                "server.port": 443,
                "http.response.status_code": 200,
                "gen_ai.response.id": "cmpl-a1b2c3d4e5f6",
                "gen_ai.response.model": "mistral-large-latest",
                "gen_ai.response.finish_reasons": ("stop",),
                "gen_ai.usage.input_tokens": 20,
                "gen_ai.usage.output_tokens": 25,
            },
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "system",
                    "parts": [
                        {"type": "text", "content": "You are a helpful assistant."}
                    ],
                },
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "What is the best French cheese?"}
                    ],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "There are many great French cheeses! Camembert, Roquefort, and Brie are among the most celebrated.",
                        }
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    # -- Chat completion with tool calls ---------------------------------------

    def test_chat_completion_with_tool_calls(self):
        request = ChatCompletionRequest(
            model="mistral-large-latest",
            messages=[
                UserMessage(content="What's the weather in Paris?"),
            ],
            tools=[
                Tool(
                    type="function",
                    function=Function(
                        name="get_weather",
                        description="Get the current weather in a given location",
                        parameters={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name",
                                },
                            },
                            "required": ["location"],
                        },
                    ),
                ),
            ],
            tool_choice="auto",
        )
        response = ChatCompletionResponse(
            id="cmpl-tool-001",
            object="chat.completion",
            model="mistral-large-latest",
            created=1700000001,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="",
                        tool_calls=[
                            ToolCall(
                                id="call_abc123",
                                function=FunctionCall(
                                    name="get_weather",
                                    arguments='{"location": "Paris"}',
                                ),
                            ),
                        ],
                    ),
                    finish_reason="tool_calls",
                ),
            ],
            usage=UsageInfo(prompt_tokens=30, completion_tokens=15, total_tokens=45),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "chat mistral-large-latest")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "chat",
                "gen_ai.response.finish_reasons": ("tool_calls",),
                "gen_ai.usage.input_tokens": 30,
                "gen_ai.usage.output_tokens": 15,
            },
        )

        # Tool definitions in request
        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.tool.definitions"]),
            [
                {
                    "type": "function",
                    "name": "get_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "City name"}
                        },
                        "required": ["location"],
                    },
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "What's the weather in Paris?"}
                    ],
                },
            ],
        )

        # Output messages — assistant with tool call and empty text content
        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {"type": "text", "content": ""},
                        {
                            "type": "tool_call",
                            "name": "get_weather",
                            "id": "call_abc123",
                            "arguments": '{"location": "Paris"}',
                        },
                    ],
                    "finish_reason": "tool_calls",
                },
            ],
        )

    # -- Embeddings ------------------------------------------------------------

    def test_embeddings(self):
        request = EmbeddingRequest(
            model="mistral-embed",
            inputs=["What is the best French cheese?"],
        )
        response = EmbeddingResponse(
            id="emb-a1b2c3",
            object="list",
            model="mistral-embed",
            data=[
                EmbeddingResponseData(
                    object="embedding", embedding=[0.1, 0.2, 0.3], index=0
                )
            ],
            usage=UsageInfo(prompt_tokens=10, completion_tokens=0, total_tokens=10),
        )

        self._run_hook_lifecycle(
            "embeddings_v1_embeddings_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "embeddings mistral-embed")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "embeddings",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.request.model": "mistral-embed",
                "gen_ai.response.id": "emb-a1b2c3",
                "gen_ai.response.model": "mistral-embed",
                "gen_ai.usage.input_tokens": 10,
            },
        )

        # Embeddings have no messages or choices
        self.assertNotIn("gen_ai.input.messages", span.attributes)
        self.assertNotIn("gen_ai.output.messages", span.attributes)
        self.assertNotIn("gen_ai.response.finish_reasons", span.attributes)

    # -- Create agent ----------------------------------------------------------

    def test_create_agent(self):
        request = CreateAgentRequest(
            model="mistral-large-latest",
            name="my-test-agent",
            description="A helpful test agent",
            instructions="You are a helpful test assistant. Be concise.",
            tools=[
                FunctionTool(
                    function=Function(
                        name="get_weather",
                        description="Get weather",
                        parameters={
                            "type": "object",
                            "properties": {"location": {"type": "string"}},
                        },
                    ),
                ),
            ],
        )
        response = Agent(
            id="agent-xyz-789",
            object="agent",
            model="mistral-large-latest",
            name="my-test-agent",
            version=0,
            versions=[],
            description="A helpful test agent",
            instructions="You are a helpful test assistant. Be concise.",
            tools=[],
            created_at=datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            deployment_chat=False,
            source="api",
        )

        self._run_hook_lifecycle(
            "agents_api_v1_agents_create",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "create_agent my-test-agent")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "create_agent",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.agent.id": "agent-xyz-789",
                "gen_ai.agent.name": "my-test-agent",
                "gen_ai.agent.description": "A helpful test agent",
                "gen_ai.system_instructions": "You are a helpful test assistant. Be concise.",
                "gen_ai.agent.version": "0",
                "gen_ai.request.model": "mistral-large-latest",
            },
        )

        # response.id should NOT be set (id means agent id for create_agent)
        self.assertNotIn("gen_ai.response.id", span.attributes)

    # -- Agent completion (via /v1/agents/completions) -------------------------

    def test_agent_completion(self):
        request = AgentsCompletionRequest(
            agent_id="agent-xyz-789",
            messages=[
                UserMessage(content="What's the weather in Paris?"),
            ],
            max_tokens=1024,
        )
        response = ChatCompletionResponse(
            id="cmpl-agent-001",
            object="chat.completion",
            model="mistral-large-latest",
            created=1700000002,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="It's sunny and 22C in Paris today.",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=40, completion_tokens=12, total_tokens=52),
        )

        self._run_hook_lifecycle(
            "agents_completion_v1_agents_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        # Span name — no agent name in request body, falls back to op name
        self.assertEqual(span.name, "invoke_agent")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "invoke_agent",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.response.id": "cmpl-agent-001",
                "gen_ai.response.model": "mistral-large-latest",
                "gen_ai.response.finish_reasons": ("stop",),
                "gen_ai.usage.input_tokens": 40,
                "gen_ai.usage.output_tokens": 12,
            },
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "What's the weather in Paris?"}
                    ],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "It's sunny and 22C in Paris today.",
                        }
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    # -- Conversation start (via /v1/conversations) ----------------------------

    def test_conversation_start(self):
        request = ConversationRequest(
            agent_id="agent-xyz-789",
            inputs="What's the weather in Paris?",
        )
        response = ConversationResponse(
            conversation_id="conv-001",
            object="conversation.response",
            usage=ConversationUsageInfo(
                prompt_tokens=15, completion_tokens=10, total_tokens=25
            ),
            outputs=[
                ToolExecutionEntry(
                    name="get_weather",
                    arguments='{"location": "Paris"}',
                    id="tool-exec-001",
                    info={"temperature": "22C", "condition": "sunny"},
                    created_at=datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
                    completed_at=datetime(2024, 6, 1, 12, 0, 1, tzinfo=timezone.utc),
                ),
                MessageOutputEntry(
                    id="msg-out-001",
                    role="assistant",
                    content="It's sunny and 22C in Paris today.",
                    model="mistral-large-latest",
                    agent_id="agent-xyz-789",
                    created_at=datetime(2024, 6, 1, 12, 0, 1, tzinfo=timezone.utc),
                    completed_at=datetime(2024, 6, 1, 12, 0, 2, tzinfo=timezone.utc),
                ),
            ],
        )

        self._run_hook_lifecycle(
            "agents_api_v1_conversations_start",
            request,
            response,
        )
        spans = self._get_finished_spans()

        # Parent span + 2 child spans (tool execution + message output)
        self.assertEqual(len(spans), 3, f"Expected 3 spans, got {len(spans)}")

        # Identify spans by operation name
        parent = None
        tool_span = None
        message_span = None
        for s in spans:
            op = s.attributes.get("gen_ai.operation.name")
            if op == "invoke_agent":
                parent = s
            elif op == "execute_tool":
                tool_span = s
            elif op == "chat":
                message_span = s

        self.assertIsNotNone(parent, "Missing invoke_agent parent span")
        self.assertIsNotNone(tool_span, "Missing execute_tool child span")
        self.assertIsNotNone(message_span, "Missing chat child span")

        # Parent span
        self.assertSpanAttributes(
            parent,
            {
                "gen_ai.operation.name": "invoke_agent",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.conversation.id": "conv-001",
                "gen_ai.usage.input_tokens": 15,
                "gen_ai.usage.output_tokens": 10,
            },
        )

        self.assertListEqual(
            _parse_json_list(parent.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "What's the weather in Paris?"}
                    ],
                },
            ],
        )

        # Parent span should NOT have output messages (they belong on child spans)
        self.assertNotIn("gen_ai.output.messages", parent.attributes)

        # Tool execution child span
        self.assertEqual(tool_span.name, "execute_tool get_weather")
        self.assertSpanAttributes(
            tool_span,
            {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.tool.name": "get_weather",
                "gen_ai.tool.call.id": "tool-exec-001",
                "gen_ai.tool.call.arguments": '{"location": "Paris"}',
                "gen_ai.tool.type": "extension",
            },
        )
        self.assertEqual(
            json.loads(tool_span.attributes["gen_ai.tool.call.result"]),
            {"temperature": "22C", "condition": "sunny"},
        )
        self.assertEqual(tool_span.parent.span_id, parent.context.span_id)

        # Message output child span
        self.assertEqual(message_span.name, "chat mistral-large-latest")
        self.assertSpanAttributes(
            message_span,
            {
                "gen_ai.operation.name": "chat",
                "gen_ai.response.id": "msg-out-001",
                "gen_ai.agent.id": "agent-xyz-789",
                "gen_ai.response.model": "mistral-large-latest",
            },
        )
        self.assertEqual(message_span.parent.span_id, parent.context.span_id)

        self.assertListEqual(
            _parse_json_list(message_span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "It's sunny and 22C in Paris today.",
                        }
                    ],
                    "finish_reason": "",
                },
            ],
        )

    # -- Conversation append ---------------------------------------------------

    def test_conversation_append_with_function_results(self):
        """Conversation append with FunctionResultEntry inputs must serialize them as tool messages."""
        request = ConversationAppendRequest(
            inputs=[
                FunctionResultEntry(
                    tool_call_id="tc-001",
                    result='{"status": "Completed"}',
                ),
                FunctionResultEntry(
                    tool_call_id="tc-002",
                    result='{"date": "2021-10-05"}',
                ),
            ],
        )
        response = ConversationResponse(
            conversation_id="conv-001",
            object="conversation.response",
            usage=ConversationUsageInfo(
                prompt_tokens=20, completion_tokens=15, total_tokens=35
            ),
            outputs=[
                MessageOutputEntry(
                    id="msg-out-002",
                    role="assistant",
                    content="Transaction T1001 was completed on 2021-10-05.",
                    model="mistral-large-latest",
                    agent_id="agent-xyz-789",
                    created_at=datetime(2024, 6, 1, 12, 1, 0, tzinfo=timezone.utc),
                    completed_at=datetime(2024, 6, 1, 12, 1, 1, tzinfo=timezone.utc),
                ),
            ],
        )

        self._run_hook_lifecycle(
            "agents_api_v1_conversations_append",
            _dump(request),
            _dump(response),
        )
        spans = self._get_finished_spans()

        # Parent span + 1 child span (message output)
        self.assertEqual(len(spans), 2, f"Expected 2 spans, got {len(spans)}")

        parent = None
        message_span = None
        for s in spans:
            op = s.attributes.get("gen_ai.operation.name")
            if op == "invoke_agent" and s.parent is None:
                parent = s
            elif op == "chat":
                message_span = s

        self.assertIsNotNone(parent, "Missing invoke_agent parent span")
        self.assertIsNotNone(message_span, "Missing chat child span")

        # Parent span — input messages must contain the function results
        self.assertListEqual(
            _parse_json_list(parent.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "tool",
                    "parts": [
                        {
                            "type": "tool_call_response",
                            "response": '{"status": "Completed"}',
                            "id": "tc-001",
                        },
                    ],
                },
                {
                    "role": "tool",
                    "parts": [
                        {
                            "type": "tool_call_response",
                            "response": '{"date": "2021-10-05"}',
                            "id": "tc-002",
                        },
                    ],
                },
            ],
        )

    # -- Non-GenAI operation ---------------------------------------------------

    def test_non_genai_operation(self):
        self._run_hook_lifecycle(
            "files_api_routes_upload_file",
            {"file": "data"},
            {"id": "file-123", "object": "file"},
        )
        span = self._get_single_span()
        self.assertNotIn("gen_ai.operation.name", span.attributes)
        self.assertNotIn("gen_ai.provider.name", span.attributes)
        self.assertEqual(span.attributes["http.request.method"], "POST")

    # -- Multi-turn tool use ---------------------------------------------------

    def test_multi_turn_tool_use(self):
        """Full tool-use loop: user → assistant(tool_calls) → tool(result) → assistant(final).

        Tests that all message roles are serialised correctly in
        gen_ai.input.messages, including the tool_call_response part for
        role="tool" and the tool_call parts for role="assistant".
        """
        request = ChatCompletionRequest(
            model="mistral-small-latest",
            max_tokens=64,
            messages=[
                UserMessage(content="What is the weather in Paris?"),
                AssistantMessage(
                    content="",
                    tool_calls=[
                        ToolCall(
                            id="7SXIeh1Ie",
                            function=FunctionCall(
                                name="get_weather",
                                arguments='{"location": "Paris"}',
                            ),
                        ),
                    ],
                ),
                ToolMessage(
                    name="get_weather",
                    content="22C, sunny",
                    tool_call_id="7SXIeh1Ie",
                ),
            ],
            tools=[
                Tool(
                    type="function",
                    function=Function(
                        name="get_weather",
                        description="Get the current weather in a given location",
                        parameters={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name",
                                },
                            },
                            "required": ["location"],
                        },
                    ),
                ),
            ],
        )
        response = ChatCompletionResponse(
            id="cmpl-multiturn-001",
            object="chat.completion",
            model="mistral-small-latest",
            created=1700000003,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="The weather in Paris is currently 22°C and sunny.",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=115, completion_tokens=14, total_tokens=129),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "chat mistral-small-latest")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.usage.input_tokens": 115,
                "gen_ai.usage.output_tokens": 14,
            },
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "What is the weather in Paris?"}
                    ],
                },
                {
                    "role": "assistant",
                    "parts": [
                        {"type": "text", "content": ""},
                        {
                            "type": "tool_call",
                            "name": "get_weather",
                            "id": "7SXIeh1Ie",
                            "arguments": '{"location": "Paris"}',
                        },
                    ],
                },
                {
                    "role": "tool",
                    "parts": [
                        {
                            "type": "tool_call_response",
                            "response": "22C, sunny",
                            "id": "7SXIeh1Ie",
                        },
                    ],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "The weather in Paris is currently 22°C and sunny.",
                        }
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

        # Tool definitions
        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.tool.definitions"]),
            [
                {
                    "type": "function",
                    "name": "get_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "City name"}
                        },
                        "required": ["location"],
                    },
                },
            ],
        )

    # -- Content chunks (multimodal) -------------------------------------------

    def test_content_chunks_text_and_image(self):
        """Request with content as array of chunks (text + image_url)."""
        request = ChatCompletionRequest(
            model="mistral-small-latest",
            max_tokens=64,
            messages=[
                UserMessage(
                    content=[
                        TextChunk(text="Describe this image briefly"),
                        ImageURLChunk(
                            image_url=ImageURL(
                                url="https://example.com/image.jpg",
                            ),
                        ),
                    ],
                ),
            ],
        )
        response = ChatCompletionResponse(
            id="cmpl-vision-001",
            object="chat.completion",
            model="mistral-small-latest",
            created=1700000004,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="The image shows a landscape.",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=96, completion_tokens=8, total_tokens=104),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(span.name, "chat mistral-small-latest")

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [
                        {"type": "text", "content": "Describe this image briefly"},
                        {
                            "type": "uri",
                            "modality": "image",
                            "uri": "https://example.com/image.jpg",
                        },
                    ],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {"type": "text", "content": "The image shows a landscape."}
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    def test_content_chunks_thinking(self):
        """Response with thinking content chunk.

        Tests the "thinking" → "reasoning" mapping in _content_to_parts.
        """
        request = ChatCompletionRequest(
            model="magistral-small-latest",
            messages=[
                UserMessage(content="What is 15 * 37?"),
            ],
        )
        response = ChatCompletionResponse(
            id="cmpl-think-001",
            object="chat.completion",
            model="magistral-small-latest",
            created=1700000006,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content=[
                            ThinkChunk(
                                thinking=[
                                    TextChunk(
                                        text="Let me calculate: 15 * 37 = 15 * 30 + 15 * 7 = 450 + 105 = 555"
                                    ),
                                ],
                            ),
                            TextChunk(text="15 * 37 = 555"),
                        ],
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=10, completion_tokens=30, total_tokens=40),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [{"type": "text", "content": "What is 15 * 37?"}],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "reasoning",
                            "content": "Let me calculate: 15 * 37 = 15 * 30 + 15 * 7 = 450 + 105 = 555",
                        },
                        {"type": "text", "content": "15 * 37 = 555"},
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    # -- Multiple choices (n > 1) ----------------------------------------------

    def test_multiple_choices(self):
        """Response with multiple choices (n=2)."""
        request = ChatCompletionRequest(
            model="mistral-small-latest",
            n=2,
            max_tokens=32,
            messages=[
                UserMessage(content="Tell me a joke"),
            ],
        )
        response = ChatCompletionResponse(
            id="cmpl-multi-001",
            object="chat.completion",
            model="mistral-small-latest",
            created=1700000005,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(
                        content="Why did the chicken cross the road?",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
                ChatCompletionChoice(
                    index=1,
                    message=AssistantMessage(
                        content="A programmer walks into a bar...",
                        tool_calls=None,
                    ),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=10, completion_tokens=20, total_tokens=30),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )
        span = self._get_single_span()

        self.assertEqual(
            span.attributes["gen_ai.response.finish_reasons"], ("stop", "stop")
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.input.messages"]),
            [
                {
                    "role": "user",
                    "parts": [{"type": "text", "content": "Tell me a joke"}],
                },
            ],
        )

        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "Why did the chicken cross the road?",
                        }
                    ],
                    "finish_reason": "stop",
                },
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "A programmer walks into a bar...",
                        }
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    # -- Error response --------------------------------------------------------

    def test_error_response(self):
        """API error response (object="error") via after_error hook."""

        request = ChatCompletionRequest(
            model="mistral-large-latest",
            temperature=0.7,
            top_p=1,
            max_tokens=512,
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="What is the best French cheese?"),
            ],
        )
        error_body = {
            "object": "error",
            "message": "Invalid model: nonexistent-model",
            "type": "invalid_model",
            "param": None,
            "code": "1500",
        }

        self._run_hook_error_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            error_body,
            status_code=400,
            error=Exception("Bad Request"),
        )
        span = self._get_single_span()

        self.assertEqual(span.status.status_code, StatusCode.ERROR)
        self.assertEqual(span.status.description, "Invalid model: nonexistent-model")
        self.assertSpanAttributes(
            span,
            {
                "error.type": "invalid_model",
                "mistral_ai.error.code": "1500",
                "http.response.status_code": 400,
            },
        )

        # Exception event per OTEL exception semantic conventions
        exc_events = [e for e in span.events if e.name == "exception"]
        self.assertEqual(
            len(exc_events), 2
        )  # one from record_exception, one from API error body
        api_error_event = exc_events[1]
        self.assertEqual(api_error_event.attributes["exception.type"], "invalid_model")
        self.assertEqual(
            api_error_event.attributes["exception.message"],
            "Invalid model: nonexistent-model",
        )

    # -- Streaming response ----------------------------------------------------

    def test_streaming_chat_completion_enriches_span(self):
        """Streaming responses must set the same response attributes as non-streaming.

        Simulates a realistic SSE stream with multiple CompletionEvent chunks:
        - chunk 1: role + first content delta
        - chunk 2: more content
        - chunk 3: finish_reason + usage
        - sentinel: [DONE]

        After consuming the stream and closing, the span must contain
        gen_ai.response.id, gen_ai.response.model, gen_ai.usage.*,
        gen_ai.response.finish_reasons, and gen_ai.output.messages.
        """
        request = ChatCompletionRequest(
            model="mistral-large-latest",
            temperature=0.7,
            max_tokens=512,
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="What is the best French cheese?"),
            ],
        )
        response_events = [
            CompletionEvent(
                data=CompletionChunk(
                    id="cmpl-stream-001",
                    model="mistral-large-latest",
                    object="chat.completion.chunk",
                    created=1700000000,
                    choices=[
                        CompletionResponseStreamChoice(
                            index=0,
                            delta=DeltaMessage(role="assistant", content="Camembert"),
                            finish_reason=None,
                        ),
                    ],
                ),
            ),
            CompletionEvent(
                data=CompletionChunk(
                    id="cmpl-stream-001",
                    model="mistral-large-latest",
                    object="chat.completion.chunk",
                    created=1700000000,
                    choices=[
                        CompletionResponseStreamChoice(
                            index=0,
                            delta=DeltaMessage(content=" is a classic choice."),
                            finish_reason=None,
                        ),
                    ],
                ),
            ),
            CompletionEvent(
                data=CompletionChunk(
                    id="cmpl-stream-001",
                    model="mistral-large-latest",
                    object="chat.completion.chunk",
                    created=1700000000,
                    choices=[
                        CompletionResponseStreamChoice(
                            index=0,
                            delta=DeltaMessage(content=""),
                            finish_reason="stop",
                        ),
                    ],
                    usage=UsageInfo(
                        prompt_tokens=20, completion_tokens=8, total_tokens=28
                    ),
                ),
            ),
        ]

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response_events,
            streaming=True,
        )
        span = self._get_single_span()

        # Request-side attributes
        self.assertEqual(span.name, "chat mistral-large-latest")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "chat",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.request.model": "mistral-large-latest",
                "gen_ai.request.temperature": 0.7,
                "gen_ai.request.max_tokens": 512,
                "gen_ai.response.id": "cmpl-stream-001",
                "gen_ai.response.model": "mistral-large-latest",
                "gen_ai.usage.input_tokens": 20,
                "gen_ai.usage.output_tokens": 8,
                "gen_ai.response.finish_reasons": ("stop",),
            },
        )

        # Output messages — accumulated from deltas
        self.assertListEqual(
            _parse_json_list(span.attributes["gen_ai.output.messages"]),
            [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": "text",
                            "content": "Camembert is a classic choice.",
                        }
                    ],
                    "finish_reason": "stop",
                },
            ],
        )

    # -- create_function_result (client-side tool execution) -------------------

    def test_create_function_result_span_attributes(self):
        """create_function_result must emit an execute_tool span with all GenAI attributes."""

        def get_weather(location: str) -> dict:
            return {"temperature": "22C", "condition": "sunny"}

        function_call = FunctionCallEntry(
            tool_call_id="tc-001",
            name="get_weather",
            arguments='{"location": "Paris"}',
            id="fc-001",
        )
        run_tool = RunFunction(
            name="get_weather",
            callable=get_weather,
            tool=FunctionTool(function=Function(name="get_weather", parameters={})),
        )

        result = asyncio.get_event_loop().run_until_complete(
            create_function_result(function_call, run_tool)
        )
        self.assertEqual(result.tool_call_id, "tc-001")

        span = self._get_single_span()

        self.assertEqual(span.name, "execute_tool get_weather")
        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.provider.name": "mistral_ai",
                "gen_ai.tool.name": "get_weather",
                "gen_ai.tool.call.id": "fc-001",
                "gen_ai.tool.call.arguments": '{"location": "Paris"}',
                "gen_ai.tool.type": "function",
            },
        )
        self.assertEqual(
            json.loads(span.attributes["gen_ai.tool.call.result"]),
            {"temperature": "22C", "condition": "sunny"},
        )

    def test_create_function_result_error_span(self):
        """When the tool raises, the span must record the error and retain identity attributes."""

        def failing_tool(x: int) -> str:
            raise ValueError("boom")

        function_call = FunctionCallEntry(
            tool_call_id="tc-err",
            name="failing_tool",
            arguments='{"x": 1}',
            id="fc-err",
        )
        run_tool = RunFunction(
            name="failing_tool",
            callable=failing_tool,
            tool=FunctionTool(function=Function(name="failing_tool", parameters={})),
        )

        asyncio.get_event_loop().run_until_complete(
            create_function_result(function_call, run_tool, continue_on_fn_error=True)
        )

        span = self._get_single_span()

        self.assertSpanAttributes(
            span,
            {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.tool.name": "failing_tool",
                "gen_ai.tool.call.id": "fc-err",
            },
        )
        # Result should NOT be present (tool didn't succeed)
        self.assertNotIn("gen_ai.tool.call.result", span.attributes)
        # Error status must be recorded
        self.assertEqual(span.status.status_code, StatusCode.ERROR)
        # Exception event must be recorded
        self.assertTrue(
            any(e.name == "exception" for e in span.events),
            "Expected an exception event on the span",
        )


    # -- Baggage propagation: gen_ai.conversation.id ---------------------------

    def test_conversation_id_from_baggage(self):
        """When gen_ai.conversation.id is set in OTEL baggage, it must appear as a span attribute."""
        request = ChatCompletionRequest(
            model="mistral-small-latest",
            messages=[UserMessage(content="Hello")],
        )
        response = ChatCompletionResponse(
            id="cmpl-baggage-001",
            object="chat.completion",
            model="mistral-small-latest",
            created=1700000010,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(content="Hi!", tool_calls=None),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=5, completion_tokens=2, total_tokens=7),
        )

        # Attach baggage to the current context
        ctx = set_baggage("gen_ai.conversation.id", "conv-from-baggage-123")
        token = context_api.attach(ctx)
        try:
            self._run_hook_lifecycle(
                "chat_completion_v1_chat_completions_post",
                request,
                response,
            )
        finally:
            context_api.detach(token)

        span = self._get_single_span()
        self.assertEqual(
            span.attributes["gen_ai.conversation.id"], "conv-from-baggage-123"
        )

    def test_no_conversation_id_without_baggage(self):
        """When no baggage is set, gen_ai.conversation.id must NOT appear on a chat span."""
        request = ChatCompletionRequest(
            model="mistral-small-latest",
            messages=[UserMessage(content="Hello")],
        )
        response = ChatCompletionResponse(
            id="cmpl-nobag-001",
            object="chat.completion",
            model="mistral-small-latest",
            created=1700000011,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=AssistantMessage(content="Hi!", tool_calls=None),
                    finish_reason="stop",
                ),
            ],
            usage=UsageInfo(prompt_tokens=5, completion_tokens=2, total_tokens=7),
        )

        self._run_hook_lifecycle(
            "chat_completion_v1_chat_completions_post",
            request,
            response,
        )

        span = self._get_single_span()
        self.assertNotIn("gen_ai.conversation.id", span.attributes)


if __name__ == "__main__":
    unittest.main()
