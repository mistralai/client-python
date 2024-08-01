import io
import logging

import pytest
from mistralai.constants import HEADER_MODEL_DEPRECATION_TIMESTAMP
from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
)

from .utils import (
    mock_chat_response_payload,
    mock_chat_response_streaming_payload,
    mock_response,
    mock_stream_response,
    mock_chat_response_payload_with_stop_token,
)


class TestChat:
    @pytest.mark.parametrize("target_deprecated_model", [True, False], ids=["deprecated", "not_deprecated"])
    def test_chat(self, client, target_deprecated_model):
        headers = (
            {
                HEADER_MODEL_DEPRECATION_TIMESTAMP: "2023-12-01T00:00:00",
            }
            if target_deprecated_model
            else {}
        )

        client._client.request.return_value = mock_response(200, mock_chat_response_payload(), headers)

        # Create a stream to capture the log output
        log_stream = io.StringIO()

        # Create a logger and add a handler that writes to the stream
        logger = client._logger
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        result = client.chat(
            model="mistral-small-latest",
            messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        )

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
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

    @pytest.mark.parametrize("target_deprecated_model", [True, False], ids=["deprecated", "not_deprecated"])
    def test_chat_streaming(self, client, target_deprecated_model):
        headers = (
            {
                HEADER_MODEL_DEPRECATION_TIMESTAMP: "2023-12-01T00:00:00",
            }
            if target_deprecated_model
            else {}
        )

        client._client.stream.return_value = mock_stream_response(200, mock_chat_response_streaming_payload(), headers)

        # Create a stream to capture the log output
        log_stream = io.StringIO()

        # Create a logger and add a handler that writes to the stream
        logger = client._logger
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        result = client.chat_stream(
            model="mistral-small-latest",
            messages=[ChatMessage(role="user", content="What is the best French cheese?")],
        )

        results = list(result)

        client._client.stream.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "text/event-stream",
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

        # Check if the log message was produced
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


    @pytest.mark.parametrize("target_deprecated_model", [True, False], ids=["deprecated", "not_deprecated"])
    def test_chat_stop(self, client, target_deprecated_model):
        headers = (
            {
                HEADER_MODEL_DEPRECATION_TIMESTAMP: "2023-12-01T00:00:00",
            }
            if target_deprecated_model
            else {}
        )

        client._client.request.return_value = mock_response(200, mock_chat_response_payload_with_stop_token(), headers)

        # Create a stream to capture the log output
        log_stream = io.StringIO()

        # Create a logger and add a handler that writes to the stream
        logger = client._logger
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        chat_messages = dict(model="mistral-small-latest",
                    messages=[ChatMessage(role="user", content="What is the the capital of France?"),
                              ChatMessage(role="assistant", content="The", prefix=True)],
            stop=["France"])
        result = client.chat(
            **chat_messages
        )

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": "What is the the capital of France?"},
                             {"role": "assistant", "content":"The", "prefix":True}],
                "stream": False,
                'stop': ['France'],
            },
            data=None,
        )

        print("***")
        print(chat_messages)
        print(result)
        
        assert isinstance(result, ChatCompletionResponse), "Should return an ChatCompletionResponse"
        assert len(result.choices) == 1
        assert result.choices[0].index == 0
        assert result.object == "chat.completion"
        assert result.choices[0].message.content == "The capital of "

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
