"""
Integration tests for GCP SDK.

These tests require GCP credentials and make real API calls.
Skip if GCP_PROJECT_ID env var is not set.

Prerequisites:
    1. Authenticate with GCP: gcloud auth application-default login
    2. Have "Vertex AI User" role on the project (e.g. model-garden-420509)

The SDK automatically:
    - Detects credentials via google.auth.default()
    - Auto-refreshes tokens when they expire
    - Builds the Vertex AI URL from project_id and region

Available models:
    - Chat: mistral-small-2503, mistral-large-2501, ...
    - FIM: codestral-2
    See: https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral

Usage:
    GCP_PROJECT_ID=model-garden-420509 pytest packages/gcp/tests/test_gcp_integration.py -v

Environment variables:
    GCP_PROJECT_ID: GCP project ID (required, or auto-detected from credentials)
    GCP_REGION: Vertex AI region (default: us-central1)
    GCP_MODEL: Model name for chat (default: mistral-small-2503)
    GCP_FIM_MODEL: Model name for FIM (default: codestral-2)

"""
import json
import os

import pytest

# Configuration from env vars
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_REGION = os.environ.get("GCP_REGION", "us-central1")
GCP_MODEL = os.environ.get("GCP_MODEL", "mistral-small-2503")
GCP_FIM_MODEL = os.environ.get("GCP_FIM_MODEL", "codestral-2")

SKIP_REASON = "GCP_PROJECT_ID env var required"

pytestmark = [
    pytest.mark.skipif(not GCP_PROJECT_ID, reason=SKIP_REASON),
    pytest.mark.integration,
]

# Shared tool definition for tool-call tests
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather in a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}


@pytest.fixture
def gcp_client():
    """Create a GCP client for integration tests."""
    from mistralai.gcp.client import MistralGCP
    return MistralGCP(
        project_id=GCP_PROJECT_ID,
        region=GCP_REGION,
    )


class TestGCPChatComplete:
    """Test synchronous chat completion."""

    def test_basic_completion(self, gcp_client):
        """Test basic chat completion returns a response."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message is not None
        assert res.choices[0].message.content is not None
        assert len(res.choices[0].message.content) > 0

    def test_completion_with_system_message(self, gcp_client):
        """Test chat completion with system + user message."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "system", "content": "You are a pirate. Respond in pirate speak."},
                {"role": "user", "content": "Say hello."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None
        assert len(res.choices[0].message.content) > 0

    def test_completion_with_max_tokens(self, gcp_client):
        """Test chat completion respects max_tokens."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Count from 1 to 100."}
            ],
            max_tokens=10,
        )
        assert res is not None
        assert res.choices[0].finish_reason in ("length", "stop")

    def test_completion_with_temperature(self, gcp_client):
        """Test chat completion accepts temperature parameter."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'test'."}
            ],
            temperature=0.0,
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    def test_completion_with_stop_sequence(self, gcp_client):
        """Test chat completion stops at stop sequence."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Write three sentences about the sky."}
            ],
            stop=["."],
        )
        assert res is not None
        content = res.choices[0].message.content
        assert content is not None
        # The model should stop at or before the first period
        assert content.count(".") <= 1

    def test_completion_with_random_seed(self, gcp_client):
        """Test chat completion with random_seed returns valid responses."""
        res1 = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'deterministic'."}
            ],
            random_seed=42,
        )
        res2 = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'deterministic'."}
            ],
            random_seed=42,
        )
        # Both should return valid responses (not asserting equality due to model non-determinism)
        assert res1.choices[0].message.content is not None
        assert res2.choices[0].message.content is not None

    def test_multi_turn_conversation(self, gcp_client):
        """Test multi-turn conversation with user/assistant round-trip."""
        res1 = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "My name is Alice."}
            ],
        )
        assert res1.choices[0].message.content is not None

        res2 = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "My name is Alice."},
                {"role": "assistant", "content": res1.choices[0].message.content},
                {"role": "user", "content": "What is my name?"},
            ],
        )
        assert res2.choices[0].message.content is not None
        assert "Alice" in res2.choices[0].message.content

    def test_tool_call(self, gcp_client):
        """Test that the model returns a tool call when given tools."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "What is the weather in Paris?"}
            ],
            tools=[WEATHER_TOOL],
            tool_choice="any",
        )
        assert res is not None
        choice = res.choices[0]
        assert choice.message.tool_calls is not None
        assert len(choice.message.tool_calls) > 0
        tool_call = choice.message.tool_calls[0]
        assert tool_call.function.name == "get_weather"
        args = json.loads(tool_call.function.arguments)
        assert "city" in args

    def test_json_response_format(self, gcp_client):
        """Test JSON response format returns valid JSON."""
        res = gcp_client.chat.complete(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Return a JSON object with a key 'greeting' and value 'hello'."}
            ],
            response_format={"type": "json_object"},
        )
        assert res is not None
        content = res.choices[0].message.content
        assert content is not None
        parsed = json.loads(content)
        assert isinstance(parsed, dict)


class TestGCPChatStream:
    """Test streaming chat completion."""

    def test_basic_stream(self, gcp_client):
        """Test streaming returns chunks with content."""
        stream = gcp_client.chat.stream(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )

        chunks = list(stream)
        assert len(chunks) > 0

        content = ""
        for chunk in chunks:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                content += chunk.data.choices[0].delta.content

        assert len(content) > 0

    def test_stream_with_max_tokens(self, gcp_client):
        """Test streaming respects max_tokens truncation."""
        stream = gcp_client.chat.stream(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Count from 1 to 100."}
            ],
            max_tokens=10,
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # Find finish_reason in any chunk
        finish_reasons = [
            chunk.data.choices[0].finish_reason
            for chunk in chunks
            if chunk.data.choices and chunk.data.choices[0].finish_reason is not None
        ]
        assert len(finish_reasons) > 0
        assert finish_reasons[-1] in ("length", "stop")

    def test_stream_finish_reason(self, gcp_client):
        """Test that the last chunk has a finish_reason."""
        stream = gcp_client.chat.stream(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hi'."}
            ],
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # The final chunk(s) should contain a finish_reason
        finish_reasons = [
            chunk.data.choices[0].finish_reason
            for chunk in chunks
            if chunk.data.choices and chunk.data.choices[0].finish_reason is not None
        ]
        assert len(finish_reasons) > 0
        assert finish_reasons[-1] == "stop"

    def test_stream_tool_call(self, gcp_client):
        """Test tool call via streaming, collecting tool_call delta chunks."""
        stream = gcp_client.chat.stream(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "What is the weather in Paris?"}
            ],
            tools=[WEATHER_TOOL],
            tool_choice="any",
        )

        chunks = list(stream)
        assert len(chunks) > 0

        # Collect tool call information from delta chunks
        tool_call_found = False
        for chunk in chunks:
            if chunk.data.choices and chunk.data.choices[0].delta.tool_calls:
                tool_call_found = True
                break

        assert tool_call_found, "Expected tool_call delta chunks in stream"


class TestGCPChatCompleteAsync:
    """Test async chat completion."""

    @pytest.mark.asyncio
    async def test_basic_completion_async(self, gcp_client):
        """Test async chat completion returns a response."""
        res = await gcp_client.chat.complete_async(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_completion_with_system_message_async(self, gcp_client):
        """Test async chat completion with system + user message."""
        res = await gcp_client.chat.complete_async(
            model=GCP_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'hello'."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_tool_call_async(self, gcp_client):
        """Test async tool call returns tool_calls."""
        res = await gcp_client.chat.complete_async(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "What is the weather in Paris?"}
            ],
            tools=[WEATHER_TOOL],
            tool_choice="any",
        )
        assert res is not None
        choice = res.choices[0]
        assert choice.message.tool_calls is not None
        assert len(choice.message.tool_calls) > 0
        assert choice.message.tool_calls[0].function.name == "get_weather"


class TestGCPChatStreamAsync:
    """Test async streaming chat completion."""

    @pytest.mark.asyncio
    async def test_basic_stream_async(self, gcp_client):
        """Test async streaming returns chunks with content."""
        stream = await gcp_client.chat.stream_async(
            model=GCP_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )

        content = ""
        async for chunk in stream:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                content += chunk.data.choices[0].delta.content

        assert len(content) > 0


class TestGCPContextManager:
    """Test context manager support."""

    def test_sync_context_manager(self):
        """Test that MistralGCP works as a sync context manager."""
        from mistralai.gcp.client import MistralGCP
        with MistralGCP(
            project_id=GCP_PROJECT_ID,
            region=GCP_REGION,
        ) as client:
            res = client.chat.complete(
                model=GCP_MODEL,
                messages=[
                    {"role": "user", "content": "Say 'context'."}
                ],
            )
            assert res is not None
            assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test that MistralGCP works as an async context manager."""
        from mistralai.gcp.client import MistralGCP
        async with MistralGCP(
            project_id=GCP_PROJECT_ID,
            region=GCP_REGION,
        ) as client:
            res = await client.chat.complete_async(
                model=GCP_MODEL,
                messages=[
                    {"role": "user", "content": "Say 'async context'."}
                ],
            )
            assert res is not None
            assert res.choices[0].message.content is not None


class TestGCPFIM:
    """Test FIM (Fill-in-the-middle) completion."""

    def _make_fim_client(self):
        """Create a GCP client configured for FIM model."""
        from mistralai.gcp.client import MistralGCP
        return MistralGCP(project_id=GCP_PROJECT_ID, region=GCP_REGION)

    def test_fim_complete(self):
        """Test FIM completion returns a response."""
        client = self._make_fim_client()
        res = client.fim.complete(
            model=GCP_FIM_MODEL,
            prompt="def fib():",
            suffix="    return result",
            timeout_ms=10000,
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    def test_fim_stream(self):
        """Test FIM streaming returns chunks."""
        client = self._make_fim_client()
        stream = client.fim.stream(
            model=GCP_FIM_MODEL,
            prompt="def hello():",
            suffix="    return greeting",
            timeout_ms=10000,
        )
        chunks = list(stream)
        assert len(chunks) > 0

        content = ""
        for chunk in chunks:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                delta_content = chunk.data.choices[0].delta.content
                if isinstance(delta_content, str):
                    content += delta_content
        assert len(content) > 0

    def test_fim_with_max_tokens(self):
        """Test FIM completion with max_tokens."""
        client = self._make_fim_client()
        res = client.fim.complete(
            model=GCP_FIM_MODEL,
            prompt="def add(a, b):",
            suffix="    return result",
            max_tokens=10,
            timeout_ms=10000,
        )
        assert res is not None
        assert res.choices[0].finish_reason in ("length", "stop")

    @pytest.mark.asyncio
    async def test_fim_complete_async(self):
        """Test async FIM completion returns a response."""
        client = self._make_fim_client()
        res = await client.fim.complete_async(
            model=GCP_FIM_MODEL,
            prompt="def fib():",
            suffix="    return result",
            timeout_ms=10000,
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_fim_stream_async(self):
        """Test async FIM streaming returns chunks."""
        client = self._make_fim_client()
        stream = await client.fim.stream_async(
            model=GCP_FIM_MODEL,
            prompt="def hello():",
            suffix="    return greeting",
            timeout_ms=10000,
        )
        chunks = []
        async for chunk in stream:
            chunks.append(chunk)
        assert len(chunks) > 0

        content = ""
        for chunk in chunks:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                delta_content = chunk.data.choices[0].delta.content
                if isinstance(delta_content, str):
                    content += delta_content
        assert len(content) > 0
