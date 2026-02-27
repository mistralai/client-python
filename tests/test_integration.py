"""
Integration tests for the main Mistral SDK.

These tests require a real Mistral API key and make actual API calls.
Skip if MISTRAL_API_KEY env var is not set.

Usage:
    MISTRAL_API_KEY=xxx pytest tests/test_integration.py -v

Environment variables:
    MISTRAL_API_KEY: API key (required)
    MISTRAL_MODEL: Chat model (default: mistral-small-latest)
    MISTRAL_FIM_MODEL: FIM model (default: codestral-latest)
    MISTRAL_EMBED_MODEL: Embedding model (default: mistral-embed)
    MISTRAL_MODERATION_MODEL: Moderation model (default: mistral-moderation-latest)
"""

import json
import os

import pytest

from mistralai.client.sdk import Mistral

# Configuration from env vars
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MODEL = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
CODESTRAL_MODEL = os.environ.get("MISTRAL_FIM_MODEL", "codestral-latest")
EMBED_MODEL = os.environ.get("MISTRAL_EMBED_MODEL", "mistral-embed")
MODERATION_MODEL = os.environ.get("MISTRAL_MODERATION_MODEL", "mistral-moderation-latest")
SKIP_REASON = "MISTRAL_API_KEY env var required"

pytestmark = [
    pytest.mark.skipif(not MISTRAL_API_KEY, reason=SKIP_REASON),
    pytest.mark.integration,
]

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
def client():
    """Create a Mistral client for integration tests."""
    assert MISTRAL_API_KEY is not None, "MISTRAL_API_KEY must be set"
    return Mistral(api_key=MISTRAL_API_KEY)


class TestChatComplete:
    """Test synchronous chat completion."""

    def test_basic_completion(self, client):
        """Test basic chat completion returns a response."""
        res = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": "Say hello in one word."}],
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message is not None
        assert res.choices[0].message.content is not None
        assert len(res.choices[0].message.content) > 0

    def test_completion_with_system_message(self, client):
        """Test chat completion with system + user message."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a pirate. Respond in pirate speak."},
                {"role": "user", "content": "Say hello."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None
        assert len(res.choices[0].message.content) > 0

    def test_completion_with_max_tokens(self, client):
        """Test chat completion respects max_tokens."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Write a long story about a cat."}
            ],
            max_tokens=10,
        )
        assert res is not None
        assert res.choices[0].finish_reason in ("length", "stop")

    def test_completion_with_temperature(self, client):
        """Test chat completion accepts temperature parameter."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'test'."}
            ],
            temperature=0.0,
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    def test_completion_with_stop_sequence(self, client):
        """Test chat completion stops at stop sequence."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Count from 1 to 10, separated by commas."}
            ],
            stop=["5"],
        )
        assert res is not None
        content = res.choices[0].message.content
        assert content is not None
        assert "6" not in content

    def test_multi_turn_conversation(self, client):
        """Test multi-turn conversation preserves context."""
        messages = [
            {"role": "user", "content": "My name is Alice."},
            {"role": "assistant", "content": "Hello Alice!"},
            {"role": "user", "content": "What is my name?"},
        ]
        res = client.chat.complete(model=MODEL, messages=messages)
        assert res.choices is not None
        content = res.choices[0].message.content
        assert content is not None
        assert "Alice" in content

    def test_tool_call(self, client):
        """Test that the model returns a tool call when given tools."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": "What's the weather in Paris?"}
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

    def test_json_response_format(self, client):
        """Test JSON response format returns valid JSON."""
        res = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Return a JSON object with key 'greeting' and value 'hello'."}
            ],
            response_format={"type": "json_object"},
        )
        assert res is not None
        content = res.choices[0].message.content
        assert content is not None
        parsed = json.loads(content)
        assert isinstance(parsed, dict)

    def test_structured_output_parse(self, client):
        """Test structured output parsing with Pydantic model."""
        from pydantic import BaseModel

        class Greeting(BaseModel):
            message: str
            language: str

        res = client.chat.parse(
            response_format=Greeting,
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in French. Return JSON with 'message' and 'language' fields.",
                }
            ],
        )
        assert res.choices is not None
        assert res.choices[0].message.parsed is not None
        assert isinstance(res.choices[0].message.parsed, Greeting)

    def test_completion_with_n(self, client):
        """Test completion with n=2 returns multiple choices."""
        res = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": "Say a random word."}],
            n=2,
        )
        assert res is not None
        assert len(res.choices) == 2
        for choice in res.choices:
            assert choice.message.content is not None


class TestChatStream:
    """Test streaming chat completion."""

    def test_basic_stream(self, client):
        """Test streaming returns chunks with content."""
        stream = client.chat.stream(
            model=MODEL,
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

    def test_stream_with_max_tokens(self, client):
        """Test streaming respects max_tokens truncation."""
        stream = client.chat.stream(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Count from 1 to 100."}
            ],
            max_tokens=10,
        )

        chunks = list(stream)
        assert len(chunks) > 0

        finish_reasons = [
            chunk.data.choices[0].finish_reason
            for chunk in chunks
            if chunk.data.choices and chunk.data.choices[0].finish_reason is not None
        ]
        assert len(finish_reasons) > 0
        assert finish_reasons[-1] in ("length", "stop")

    def test_stream_finish_reason(self, client):
        """Test that the last chunk has a finish_reason."""
        stream = client.chat.stream(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'hi'."}
            ],
        )

        chunks = list(stream)
        assert len(chunks) > 0

        finish_reasons = [
            chunk.data.choices[0].finish_reason
            for chunk in chunks
            if chunk.data.choices and chunk.data.choices[0].finish_reason is not None
        ]
        assert len(finish_reasons) > 0
        assert finish_reasons[-1] == "stop"

    def test_stream_tool_call(self, client):
        """Test tool call via streaming, collecting tool_call delta chunks."""
        stream = client.chat.stream(
            model=MODEL,
            messages=[
                {"role": "user", "content": "What is the weather in Paris?"}
            ],
            tools=[WEATHER_TOOL],
            tool_choice="any",
        )

        chunks = list(stream)
        assert len(chunks) > 0

        tool_call_found = False
        for chunk in chunks:
            if chunk.data.choices and chunk.data.choices[0].delta.tool_calls:
                tool_call_found = True
                break

        assert tool_call_found, "Expected tool_call delta chunks in stream"


class TestChatCompleteAsync:
    """Test async chat completion."""

    @pytest.mark.asyncio
    async def test_basic_completion_async(self, client):
        """Test async chat completion returns a response."""
        res = await client.chat.complete_async(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_completion_with_system_message_async(self, client):
        """Test async chat completion with system + user message."""
        res = await client.chat.complete_async(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'hello'."},
            ],
        )
        assert res is not None
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_tool_call_async(self, client):
        """Test async tool call returns tool_calls."""
        res = await client.chat.complete_async(
            model=MODEL,
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


class TestChatStreamAsync:
    """Test async streaming chat completion."""

    @pytest.mark.asyncio
    async def test_basic_stream_async(self, client):
        """Test async streaming returns chunks with content."""
        stream = await client.chat.stream_async(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
        )

        content = ""
        async for chunk in stream:
            if chunk.data.choices and chunk.data.choices[0].delta.content:
                content += chunk.data.choices[0].delta.content

        assert len(content) > 0


class TestFIM:
    """Test FIM (Fill-in-the-middle) completion."""

    def test_fim_complete(self, client):
        """Test FIM completion returns a response."""
        res = client.fim.complete(
            model=CODESTRAL_MODEL,
            prompt="def fibonacci(n):\n    ",
            suffix="\n    return result",
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    def test_fim_stream(self, client):
        """Test FIM streaming returns chunks."""
        stream = client.fim.stream(
            model=CODESTRAL_MODEL,
            prompt="def hello():\n    ",
            suffix="    return greeting",
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

    def test_fim_with_max_tokens(self, client):
        """Test FIM completion with max_tokens."""
        res = client.fim.complete(
            model=CODESTRAL_MODEL,
            prompt="def add(a, b):\n    ",
            suffix="    return result",
            max_tokens=10,
        )
        assert res is not None
        assert res.choices[0].finish_reason in ("length", "stop")

    @pytest.mark.asyncio
    async def test_fim_complete_async(self, client):
        """Test async FIM completion returns a response."""
        res = await client.fim.complete_async(
            model=CODESTRAL_MODEL,
            prompt="def fibonacci(n):\n    ",
            suffix="\n    return result",
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0
        assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_fim_stream_async(self, client):
        """Test async FIM streaming returns chunks."""
        stream = await client.fim.stream_async(
            model=CODESTRAL_MODEL,
            prompt="def hello():\n    ",
            suffix="    return greeting",
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


class TestEmbeddings:
    """Test embeddings API."""

    def test_embeddings_create(self, client):
        """Test embeddings create returns vectors."""
        res = client.embeddings.create(
            model=EMBED_MODEL,
            inputs="Hello world",
        )
        assert res is not None
        assert res.data is not None
        assert len(res.data) > 0
        assert len(res.data[0].embedding) > 0

    def test_embeddings_multiple_inputs(self, client):
        """Test embeddings with multiple inputs returns multiple vectors."""
        res = client.embeddings.create(
            model=EMBED_MODEL,
            inputs=["Hello", "World"],
        )
        assert res.data is not None
        assert len(res.data) == 2

    def test_embeddings_output_dtype(self, client):
        """Test embeddings with output_dtype parameter."""
        res = client.embeddings.create(
            model=EMBED_MODEL,
            inputs="Hello",
            output_dtype="float",
        )
        assert res.data is not None
        assert len(res.data[0].embedding) > 0

    @pytest.mark.asyncio
    async def test_embeddings_create_async(self, client):
        """Test async embeddings returns vectors."""
        res = await client.embeddings.create_async(
            model=EMBED_MODEL,
            inputs="Hello world",
        )
        assert res is not None
        assert res.data is not None


class TestClassifiers:
    """Test moderation and classification APIs."""

    def test_moderate_text(self, client):
        """Test text moderation returns results."""
        res = client.classifiers.moderate(
            model=MODERATION_MODEL,
            inputs=["This is a normal message."],
        )
        assert res is not None
        assert res.results is not None
        assert len(res.results) > 0

    def test_moderate_chat(self, client):
        """Test chat moderation returns results."""
        res = client.classifiers.moderate_chat(
            model=MODERATION_MODEL,
            inputs=[[{"role": "user", "content": "Hello there."}]],
        )
        assert res is not None
        assert res.results is not None

    def test_classify_text(self, client):
        """Test text classification returns results."""
        try:
            res = client.classifiers.classify(
                model=MODERATION_MODEL,
                inputs=["This is a normal message."],
            )
            assert res is not None
            assert res.results is not None
        except Exception as e:
            if "Invalid model" in str(e):
                pytest.skip("Classification not supported with this model")
            raise

    def test_classify_chat(self, client):
        """Test chat classification with InstructRequest."""
        from mistralai.client.models import InstructRequest

        try:
            res = client.classifiers.classify_chat(
                model=MODERATION_MODEL,
                input=[
                    InstructRequest(
                        messages=[{"role": "user", "content": "Hello there."}]
                    )
                ],
            )
            assert res is not None
            assert res.results is not None
        except Exception as e:
            if "Invalid model" in str(e):
                pytest.skip("Classification not supported with this model")
            raise


class TestModels:
    """Test models list and retrieve APIs."""

    def test_models_list(self, client):
        """Test models list returns available models."""
        res = client.models.list()
        assert res is not None
        assert res.data is not None
        assert len(res.data) > 0

    def test_models_retrieve(self, client):
        """Test model retrieve returns model details."""
        res = client.models.retrieve(model_id=MODEL)
        assert res is not None
        assert res.id == MODEL

    @pytest.mark.asyncio
    async def test_models_list_async(self, client):
        """Test async models list returns available models."""
        res = await client.models.list_async()
        assert res is not None
        assert res.data is not None


class TestFiles:
    """Test file upload, list, and retrieve APIs."""

    SAMPLE_JSONL = b'{"messages": [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]}\n'

    def test_file_upload_and_retrieve(self, client):
        """Test file upload and retrieve returns file info."""
        from mistralai.client.models import File

        file_obj = File(file_name="test.jsonl", content=self.SAMPLE_JSONL)
        res = client.files.upload(file=file_obj)
        assert res is not None
        assert res.id is not None

        retrieved = client.files.retrieve(file_id=res.id)
        assert retrieved is not None
        assert retrieved.id == res.id

        # Cleanup
        client.files.delete(file_id=res.id)

    def test_file_list(self, client):
        """Test file list returns files."""
        res = client.files.list()
        assert res is not None

    @pytest.mark.asyncio
    async def test_file_upload_async(self, client):
        """Test async file upload returns file info."""
        from mistralai.client.models import File

        file_obj = File(file_name="async_test.jsonl", content=self.SAMPLE_JSONL)
        res = await client.files.upload_async(file=file_obj)
        assert res is not None
        assert res.id is not None

        # Cleanup
        await client.files.delete_async(file_id=res.id)


class TestFilesExtended:
    """Test file download, signed URL, and delete APIs."""

    SAMPLE_JSONL = b'{"messages": [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]}\n'

    def test_file_download(self, client):
        """Test file download returns content."""
        from mistralai.client.models import File

        file_obj = File(file_name="download_test.jsonl", content=self.SAMPLE_JSONL)
        res = client.files.upload(file=file_obj)
        assert res is not None
        assert res.id is not None

        # download() returns an httpx.Response (streaming) - must call read()
        downloaded = client.files.download(file_id=res.id)
        assert downloaded is not None
        content = downloaded.read()
        assert content is not None
        assert len(content) > 0

        # Cleanup
        client.files.delete(file_id=res.id)

    def test_file_get_signed_url(self, client):
        """Test file get_signed_url returns valid URL."""
        from mistralai.client.models import File

        file_obj = File(file_name="signed_url_test.jsonl", content=self.SAMPLE_JSONL)
        res = client.files.upload(file=file_obj)
        assert res is not None
        assert res.id is not None

        signed = client.files.get_signed_url(file_id=res.id)
        assert signed is not None
        assert signed.url is not None
        assert signed.url.startswith("http")

        # Cleanup
        client.files.delete(file_id=res.id)

    def test_file_delete(self, client):
        """Test file delete marks file as deleted."""
        from mistralai.client.models import File

        file_obj = File(file_name="delete_test.jsonl", content=self.SAMPLE_JSONL)
        res = client.files.upload(file=file_obj)
        assert res is not None
        assert res.id is not None

        deleted = client.files.delete(file_id=res.id)
        assert deleted is not None
        assert deleted.id == res.id
        assert deleted.deleted is True


class TestOCR:
    """Test OCR document processing API."""

    def test_ocr_process(self, client):
        """Test OCR process returns extracted pages."""
        res = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://arxiv.org/pdf/2310.06825",
            },
        )
        assert res is not None
        assert res.pages is not None
        assert len(res.pages) > 0
        assert res.model == "mistral-ocr-latest"

    @pytest.mark.asyncio
    async def test_ocr_process_async(self, client):
        """Test async OCR process returns extracted pages."""
        res = await client.ocr.process_async(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": "https://arxiv.org/pdf/2310.06825",
            },
        )
        assert res is not None
        assert res.pages is not None
        assert len(res.pages) > 0
        assert res.model == "mistral-ocr-latest"


class TestContextManager:
    """Test context manager support."""

    def test_sync_context_manager(self):
        """Test that Mistral works as a sync context manager."""
        assert MISTRAL_API_KEY is not None
        with Mistral(api_key=MISTRAL_API_KEY) as m:
            res = m.chat.complete(
                model=MODEL,
                messages=[{"role": "user", "content": "Say 'context'."}],
            )
            assert res is not None
            assert res.choices[0].message.content is not None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test that Mistral works as an async context manager."""
        assert MISTRAL_API_KEY is not None
        async with Mistral(api_key=MISTRAL_API_KEY) as m:
            res = await m.chat.complete_async(
                model=MODEL,
                messages=[{"role": "user", "content": "Say 'async context'."}],
            )
            assert res is not None
            assert res.choices[0].message.content is not None


class TestErrors:
    """Test error handling scenarios."""

    def test_invalid_model_returns_error(self, client):
        """Test that invalid model raises SDKError."""
        from mistralai.client.errors import SDKError

        with pytest.raises(SDKError):
            client.chat.complete(
                model="nonexistent-model-12345",
                messages=[{"role": "user", "content": "Hi"}],
            )

    def test_invalid_api_key_returns_401(self):
        """Test that invalid API key returns 401."""
        bad_client = Mistral(api_key="invalid-key-12345")
        from mistralai.client.errors import SDKError

        with pytest.raises(SDKError) as exc_info:
            bad_client.chat.complete(
                model=MODEL,
                messages=[{"role": "user", "content": "Hi"}],
            )
        assert exc_info.value.status_code == 401

    def test_empty_messages_returns_error(self, client):
        """Test that empty messages raises SDKError."""
        from mistralai.client.errors import SDKError

        with pytest.raises(SDKError):
            client.chat.complete(
                model=MODEL,
                messages=[],
            )

    def test_rate_limit_retry(self, client):
        """Test retry configuration works with API calls."""
        from mistralai.client.utils.retries import BackoffStrategy, RetryConfig

        retry = RetryConfig(
            strategy="backoff",
            backoff=BackoffStrategy(
                initial_interval=500,
                max_interval=10000,
                exponent=1.5,
                max_elapsed_time=30000,
            ),
            retry_connection_errors=True,
        )
        res = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": "Say hello in one word."}],
            retries=retry,
        )
        assert res is not None
        assert res.choices is not None
        assert len(res.choices) > 0


class TestAgentsComplete:
    """Test agents completion API."""

    def _create_agent(self, client):
        """Create a test agent for completion tests."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-completion",
            instructions="You are a helpful assistant. Reply concisely.",
        )
        return agent

    def test_agents_complete(self, client):
        """Test agents complete returns a response."""
        agent = self._create_agent(client)
        try:
            res = client.agents.complete(
                agent_id=agent.id,
                messages=[{"role": "user", "content": "Say hello in one word."}],
            )
            assert res is not None
            assert res.choices is not None
            assert len(res.choices) > 0
            assert res.choices[0].message is not None
            assert res.choices[0].message.content is not None
        finally:
            client.beta.agents.delete(agent_id=agent.id)

    def test_agents_stream(self, client):
        """Test agents stream returns chunks."""
        agent = self._create_agent(client)
        try:
            stream = client.agents.stream(
                agent_id=agent.id,
                messages=[{"role": "user", "content": "Say hello in one word."}],
            )
            chunks = list(stream)
            assert len(chunks) > 0
            last = chunks[-1]
            assert last.data is not None
            assert last.data.choices is not None
        finally:
            client.beta.agents.delete(agent_id=agent.id)

    @pytest.mark.asyncio
    async def test_agents_complete_async(self, client):
        """Test async agents complete returns a response."""
        agent = self._create_agent(client)
        try:
            res = await client.agents.complete_async(
                agent_id=agent.id,
                messages=[{"role": "user", "content": "Say hello in one word."}],
            )
            assert res is not None
            assert res.choices is not None
            assert len(res.choices) > 0
        finally:
            client.beta.agents.delete(agent_id=agent.id)


class TestBetaAgents:
    """Test beta agents CRUD APIs."""

    def test_agent_create_and_get(self, client):
        """Test agent create and get returns agent info."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-create",
            instructions="You are a helpful assistant.",
        )
        try:
            assert agent is not None
            assert agent.id is not None
            assert agent.name == "test-agent-create"

            retrieved = client.beta.agents.get(agent_id=agent.id)
            assert retrieved is not None
            assert retrieved.id == agent.id
            assert retrieved.name == "test-agent-create"
        finally:
            client.beta.agents.delete(agent_id=agent.id)

    def test_agent_list(self, client):
        """Test agent list returns created agent."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-list",
            instructions="You are a helpful assistant.",
        )
        try:
            # Pass metadata={} explicitly to work around SDK UNSET serialization bug
            agents = client.beta.agents.list(metadata={})
            assert agents is not None
            assert isinstance(agents, list)
            agent_ids = [a.id for a in agents]
            assert agent.id in agent_ids
        finally:
            client.beta.agents.delete(agent_id=agent.id)

    def test_agent_update(self, client):
        """Test agent update modifies agent properties."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-update-original",
            instructions="You are a helpful assistant.",
        )
        try:
            updated = client.beta.agents.update(
                agent_id=agent.id,
                name="test-agent-update-modified",
            )
            assert updated is not None
            assert updated.name == "test-agent-update-modified"
        finally:
            client.beta.agents.delete(agent_id=agent.id)

    def test_agent_delete(self, client):
        """Test agent delete removes agent."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-delete",
            instructions="You are a helpful assistant.",
        )
        client.beta.agents.delete(agent_id=agent.id)

        from mistralai.client.errors import SDKError

        try:
            client.beta.agents.get(agent_id=agent.id)
            pytest.fail("Agent should have been deleted")
        except SDKError:
            pass  # Expected: agent not found

    def test_agent_list_versions(self, client):
        """Test agent list_versions returns version history."""
        agent = client.beta.agents.create(
            model=MODEL,
            name="test-agent-versions",
            instructions="You are a helpful assistant.",
        )
        try:
            client.beta.agents.update(
                agent_id=agent.id,
                name="test-agent-versions-v2",
            )

            versions = client.beta.agents.list_versions(agent_id=agent.id)
            assert versions is not None
            assert isinstance(versions, list)
            assert len(versions) > 0
        finally:
            client.beta.agents.delete(agent_id=agent.id)


class TestConversations:
    """Test conversations API."""

    def test_conversation_start(self, client):
        """Test conversation start returns conversation ID."""
        res = client.beta.conversations.start(
            inputs=[
                {"role": "user", "content": "Say hello in one word."},
            ],
            model=MODEL,
        )
        assert res is not None
        assert res.conversation_id is not None
        assert res.outputs is not None

        # Cleanup
        client.beta.conversations.delete(conversation_id=res.conversation_id)

    def test_conversation_append(self, client):
        """Test conversation append adds to existing conversation."""
        res = client.beta.conversations.start(
            inputs=[
                {"role": "user", "content": "My name is Alice."},
            ],
            model=MODEL,
        )
        assert res.conversation_id is not None

        append_res = client.beta.conversations.append(
            conversation_id=res.conversation_id,
            inputs=[
                {"role": "user", "content": "What is my name?"},
            ],
        )
        assert append_res is not None
        assert append_res.conversation_id == res.conversation_id
        assert append_res.outputs is not None

        # Cleanup
        client.beta.conversations.delete(conversation_id=res.conversation_id)

    def test_conversation_get_history(self, client):
        """Test conversation get_history returns entries."""
        res = client.beta.conversations.start(
            inputs=[
                {"role": "user", "content": "Say hello."},
            ],
            model=MODEL,
        )
        assert res.conversation_id is not None

        history = client.beta.conversations.get_history(
            conversation_id=res.conversation_id,
        )
        assert history is not None
        assert history.conversation_id == res.conversation_id
        assert history.entries is not None
        assert len(history.entries) > 0

        # Cleanup
        client.beta.conversations.delete(conversation_id=res.conversation_id)

    def test_conversation_get_messages(self, client):
        """Test conversation get_messages returns messages."""
        res = client.beta.conversations.start(
            inputs=[
                {"role": "user", "content": "Say hello."},
            ],
            model=MODEL,
        )
        assert res.conversation_id is not None

        messages = client.beta.conversations.get_messages(
            conversation_id=res.conversation_id,
        )
        assert messages is not None
        assert messages.conversation_id == res.conversation_id
        assert messages.messages is not None
        assert len(messages.messages) > 0

        # Cleanup
        client.beta.conversations.delete(conversation_id=res.conversation_id)

    def test_conversation_start_stream(self, client):
        """Test conversation start_stream returns events."""
        stream = client.beta.conversations.start_stream(
            inputs=[
                {"role": "user", "content": "Say hello in one word."},
            ],
            model=MODEL,
        )
        events = list(stream)
        assert len(events) > 0

        conversation_id = None
        for event in events:
            if hasattr(event, "data") and hasattr(event.data, "conversation_id"):
                conversation_id = event.data.conversation_id
                break

        if conversation_id is not None:
            client.beta.conversations.delete(conversation_id=conversation_id)

    def test_conversation_delete(self, client):
        """Test conversation delete removes conversation."""
        res = client.beta.conversations.start(
            inputs=[
                {"role": "user", "content": "Say hello."},
            ],
            model=MODEL,
        )
        assert res.conversation_id is not None

        client.beta.conversations.delete(conversation_id=res.conversation_id)

        from mistralai.client.errors import SDKError

        try:
            client.beta.conversations.get_history(
                conversation_id=res.conversation_id,
            )
            pytest.fail("Conversation should have been deleted")
        except SDKError:
            pass  # Expected: conversation not found
