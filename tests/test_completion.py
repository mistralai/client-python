from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
)

from .utils import (
    mock_completion_response_payload,
    mock_response,
    mock_stream_response,
)


class TestCompletion:
    def test_completion(self, client):
        client._client.request.return_value = mock_response(
            200,
            mock_completion_response_payload(),
        )

        result = client.completion(
            model="mistral-small-latest",
            prompt="def add(a, b):",
            suffix="return a + b",
            temperature=0.5,
            max_tokens=50,
            top_p=0.9,
            random_seed=42,
        )

        client._client.request.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/fim/completions",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "application/json",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-small-latest",
                "prompt": "def add(a, b):",
                "suffix": "return a + b",
                "stream": False,
                "temperature": 0.5,
                "max_tokens": 50,
                "top_p": 0.9,
                "random_seed": 42,
            },
        )

        assert isinstance(result, ChatCompletionResponse), "Should return an ChatCompletionResponse"
        assert len(result.choices) == 1
        assert result.choices[0].index == 0
        assert result.object == "chat.completion"

    def test_completion_streaming(self, client):
        client._client.stream.return_value = mock_stream_response(
            200,
            mock_completion_response_payload(),
        )

        result = client.completion_stream(
            model="mistral-small-latest", prompt="def add(a, b):", suffix="return a + b", stop=["#"]
        )

        results = list(result)

        client._client.stream.assert_called_once_with(
            "post",
            "https://api.mistral.ai/v1/fim/completions",
            headers={
                "User-Agent": f"mistral-client-python/{client._version}",
                "Accept": "text/event-stream",
                "Authorization": "Bearer test_api_key",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistral-small-latest",
                "prompt": "def add(a, b):",
                "suffix": "return a + b",
                "stream": True,
                "stop": ["#"],
            },
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
                assert result.choices[0].delta.content == f"stream response {i - 1}"
                assert result.object == "chat.completion.chunk"
