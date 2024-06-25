import io
import logging
import unittest.mock as mock

import pytest
from mistralai.constants import (
    HEADER_MODEL_DEPRECATION_TIMESTAMP,
)
from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
)

from .utils import (
    mock_async_stream_response,
    mock_chat_response_payload,
    mock_chat_response_streaming_payload,
    mock_response,
)


class TestAsyncChat:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("target_deprecated_model", [True, False], ids=["deprecated", "not_deprecated"])
    async def test_chat(self, async_client, target_deprecated_model):
        headers = (
            {
                HEADER_MODEL_DEPRECATION_TIMESTAMP: "2023-12-01T00:00:00",
            }
            if target_deprecated_model
            else {}
        )

        async_client._client.request.return_value = mock_response(200, mock_chat_response_payload(), headers)

        # Create a stream to capture the log output
        log_stream = io.StringIO()

        # Create a logger and add a handler that writes to the stream
        logger = async_client._logger
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        result = await async_client.chat(
            model="mistral-small-latest",
            messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        )

        async_client._client.request.assert_awaited_once_with(
            "post",
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": "What is the best French cheese?"}],
                "stream": False,
            },
            data=None,
        )

        assert isinstance(result, ChatCompletionResponse), "Should return an ChatCompletionResponse"
        assert len(result.choices) == 1
        assert result.choices[0].index == 0
        assert result.object == "chat.completion"

        # Check if the log message was produced when the model is deprecated
        log_output = log_stream.getvalue()
        excepted_log = (
            (
                "WARNING: The model mistral-small-latest is deprecated "
                "and will be removed on 2023-12-01T00:00:00. "
                "Please refer to https://docs.mistral.ai/getting-started/models/#api-versioning for more information.\n"
            )
            if target_deprecated_model
            else ""
        )
        assert excepted_log == log_output

    @pytest.mark.asyncio
    @pytest.mark.parametrize("target_deprecated_model", [True, False], ids=["deprecated", "not_deprecated"])
    async def test_chat_streaming(self, async_client, target_deprecated_model):
        headers = (
            {
                HEADER_MODEL_DEPRECATION_TIMESTAMP: "2023-12-01T00:00:00",
            }
            if target_deprecated_model
            else {}
        )

        async_client._client.stream = mock.Mock()
        async_client._client.stream.return_value = mock_async_stream_response(
            200, mock_chat_response_streaming_payload(), headers
        )

        # Create a stream to capture the log output
        log_stream = io.StringIO()

        # Create a logger and add a handler that writes to the stream
        logger = async_client._logger
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        result = async_client.chat_stream(
            model="mistral-small-latest",
            messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        )

        results = [r async for r in result]

        async_client._client.stream.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Accept": "text/event-stream",
                "User-Agent": f"mistral-client-python/{async_client._version}",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": "What is the best French cheese?"}],
                "stream": True,
            },
            data=None,
        )

        for i, result in enumerate(results):
            if i == 0:
                assert isinstance(result, ChatCompletionStreamResponse), "Should return an ChatCompletionStreamResponse"
                assert len(result.choices) == 1
                assert result.choices[0].index == 0
                assert result.choices[0].delta.role == "assistant"
            else:
                assert isinstance(result, ChatCompletionStreamResponse), "Should return an ChatCompletionStreamResponse"
                assert len(result.choices) == 1
                assert result.choices[0].index == i - 1
                assert result.choices[0].delta.content == f"stream response {i-1}"
                assert result.object == "chat.completion.chunk"

        # Check if the log message was produced when the model is deprecated
        log_output = log_stream.getvalue()
        excepted_log = (
            (
                "WARNING: The model mistral-small-latest is deprecated "
                "and will be removed on 2023-12-01T00:00:00. "
                "Please refer to https://docs.mistral.ai/getting-started/models/#api-versioning for more information.\n"
            )
            if target_deprecated_model
            else ""
        )
        assert excepted_log == log_output
