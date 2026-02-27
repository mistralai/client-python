"""
Integration tests for Azure SDK.

These tests require credentials and make real API calls.
Skip if AZURE_API_KEY env var is not set.

Prerequisites:
    1. Azure API key (stored in Bitwarden at "[MaaS] - Azure Foundry API key")
    2. Tailscale connected via gw-0 exit node

Usage:
    AZURE_API_KEY=xxx pytest packages/azure/tests/test_azure_integration.py -v

Environment variables:
    AZURE_API_KEY: API key (required)
    AZURE_ENDPOINT: Base URL (default: https://maas-qa-aifoundry.services.ai.azure.com/models)
    AZURE_MODEL: Model name (default: maas-qa-ministral-3b)
    AZURE_API_VERSION: API version (default: 2024-05-01-preview)

Note: AZURE_ENDPOINT should be the base URL without path suffixes.
The SDK appends /chat/completions to this URL. The api_version parameter
is automatically injected as a query parameter by the SDK.

Available models:
    Chat: maas-qa-ministral-3b, maas-qa-mistral-large-3, maas-qa-mistral-medium-2505
    OCR: maas-qa-mistral-document-ai-2505, maas-qa-mistral-document-ai-2512
         (OCR uses a separate endpoint, not tested here)
"""
import json
import os

import pytest

# Configuration from env vars
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_ENDPOINT = os.environ.get(
    "AZURE_ENDPOINT",
    "https://maas-qa-aifoundry.services.ai.azure.com/models",
)
AZURE_MODEL = os.environ.get("AZURE_MODEL", "maas-qa-ministral-3b")
AZURE_API_VERSION = os.environ.get("AZURE_API_VERSION", "2024-05-01-preview")

SKIP_REASON = "AZURE_API_KEY env var required"

pytestmark = [
    pytest.mark.skipif(not AZURE_API_KEY, reason=SKIP_REASON),
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
def azure_client():
    """Create an Azure client for integration tests."""
    from mistralai.azure.client import MistralAzure
    assert AZURE_API_KEY is not None, "AZURE_API_KEY must be set"
    return MistralAzure(
        api_key=AZURE_API_KEY,
        server_url=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
    )


class TestAzureChatComplete:
    """Test synchronous chat completion."""

    def test_basic_completion(self, azure_client):
        """Test basic chat completion returns a response."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
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

    def test_completion_with_system_message(self, azure_client):
        """Test chat completion with system + user message."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "system", "content": "You are a pirate. Respond in pirate speak."},
                {"role": "user", "content": "Say hello."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None
        assert len(res.choices[0].message.content) > 0

    def test_completion_with_max_tokens(self, azure_client):
        """Test chat completion respects max_tokens."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Count from 1 to 100."}
            ],
            max_tokens=10,
        )
        assert res is not None
        assert res.choices[0].finish_reason in ("length", "stop")

    def test_completion_with_temperature(self, azure_client):
        """Test chat completion accepts temperature parameter."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say 'test'."}
            ],
            temperature=0.0,
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    def test_completion_with_stop_sequence(self, azure_client):
        """Test chat completion stops at stop sequence."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
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

    def test_completion_with_random_seed(self, azure_client):
        """Test chat completion with random_seed returns valid responses."""
        res1 = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say 'deterministic'."}
            ],
            random_seed=42,
        )
        res2 = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say 'deterministic'."}
            ],
            random_seed=42,
        )
        # Both should return valid responses (not asserting equality due to model non-determinism)
        assert res1.choices[0].message.content is not None
        assert res2.choices[0].message.content is not None

    def test_multi_turn_conversation(self, azure_client):
        """Test multi-turn conversation with user/assistant round-trip."""
        res1 = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "My name is Alice."}
            ],
        )
        assert res1.choices[0].message.content is not None

        res2 = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "My name is Alice."},
                {"role": "assistant", "content": res1.choices[0].message.content},
                {"role": "user", "content": "What is my name?"},
            ],
        )
        assert res2.choices[0].message.content is not None
        assert "Alice" in res2.choices[0].message.content

    def test_tool_call(self, azure_client):
        """Test that the model returns a tool call when given tools."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
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

    def test_json_response_format(self, azure_client):
        """Test JSON response format returns valid JSON."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
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

    def test_completion_with_n(self, azure_client):
        """Test completion with n=2 returns multiple choices."""
        res = azure_client.chat.complete(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say a random word."}
            ],
            n=2,
        )
        assert res is not None
        assert len(res.choices) == 2
        for choice in res.choices:
            assert choice.message.content is not None


class TestAzureChatStream:
    """Test streaming chat completion."""

    def test_basic_stream(self, azure_client):
        """Test streaming returns chunks with content."""
        stream = azure_client.chat.stream(
            model=AZURE_MODEL,
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

    def test_stream_with_max_tokens(self, azure_client):
        """Test streaming respects max_tokens truncation."""
        stream = azure_client.chat.stream(
            model=AZURE_MODEL,
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

    def test_stream_finish_reason(self, azure_client):
        """Test that the last chunk has a finish_reason."""
        stream = azure_client.chat.stream(
            model=AZURE_MODEL,
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

    def test_stream_tool_call(self, azure_client):
        """Test tool call via streaming, collecting tool_call delta chunks."""
        stream = azure_client.chat.stream(
            model=AZURE_MODEL,
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


class TestAzureChatCompleteAsync:
    """Test async chat completion."""

    @pytest.mark.asyncio
    async def test_basic_completion_async(self, azure_client):
        """Test async chat completion returns a response."""
        res = await azure_client.chat.complete_async(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_completion_with_system_message_async(self, azure_client):
        """Test async chat completion with system + user message."""
        res = await azure_client.chat.complete_async(
            model=AZURE_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'hello'."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_tool_call_async(self, azure_client):
        """Test async tool call returns tool_calls."""
        res = await azure_client.chat.complete_async(
            model=AZURE_MODEL,
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


class TestAzureChatStreamAsync:
    """Test async streaming chat completion."""

    @pytest.mark.asyncio
    async def test_basic_stream_async(self, azure_client):
        """Test async streaming returns chunks with content."""
        stream = await azure_client.chat.stream_async(
            model=AZURE_MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )

        content = ""
        async for chunk in stream:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                content += chunk.data.choices[0].delta.content

        assert len(content) > 0


class TestAzureContextManager:
    """Test context manager support."""

    def test_sync_context_manager(self):
        """Test that MistralAzure works as a sync context manager."""
        from mistralai.azure.client import MistralAzure
        assert AZURE_API_KEY is not None, "AZURE_API_KEY must be set"
        with MistralAzure(
            api_key=AZURE_API_KEY,
            server_url=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION,
        ) as client:
            res = client.chat.complete(
                model=AZURE_MODEL,
                messages=[
                    {"role": "user", "content": "Say 'context'."}
                ],
            )
            assert res is not None
            assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test that MistralAzure works as an async context manager."""
        from mistralai.azure.client import MistralAzure
        assert AZURE_API_KEY is not None, "AZURE_API_KEY must be set"
        async with MistralAzure(
            api_key=AZURE_API_KEY,
            server_url=AZURE_ENDPOINT,
            api_version=AZURE_API_VERSION,
        ) as client:
            res = await client.chat.complete_async(
                model=AZURE_MODEL,
                messages=[
                    {"role": "user", "content": "Say 'async context'."}
                ],
            )
            assert res is not None
            assert res.choices[0].message.content is not None
