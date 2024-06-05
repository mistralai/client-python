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
)


class TestChat:
    def test_chat(self, client):
        client._client.request.return_value = mock_response(
            200,
            mock_chat_response_payload(),
        )

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

    def test_chat_streaming(self, client):
        client._client.stream.return_value = mock_stream_response(
            200,
            mock_chat_response_streaming_payload(),
        )

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
