import os
import posixpath
import time
from json import JSONDecodeError
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

from httpx import (
    AsyncClient,
    AsyncHTTPTransport,
    ConnectError,
    Limits,
    RequestError,
    Response,
)

from mistralai.client_base import ClientBase
from mistralai.constants import ENDPOINT, RETRY_STATUS_CODES
from mistralai.exceptions import (
    MistralAPIException,
    MistralAPIStatusException,
    MistralConnectionException,
    MistralException,
)
from mistralai.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ResponseFormat,
    ToolChoice,
)
from mistralai.models.embeddings import EmbeddingResponse
from mistralai.models.models import ModelList


class MistralAsyncClient(ClientBase):
    def __init__(
        self,
        api_key: Optional[str] = os.environ.get("MISTRAL_API_KEY", None),
        endpoint: str = ENDPOINT,
        max_retries: int = 5,
        timeout: int = 120,
        max_concurrent_requests: int = 64,
    ):
        super().__init__(endpoint, api_key, max_retries, timeout)

        self._client = AsyncClient(
            follow_redirects=True,
            timeout=timeout,
            limits=Limits(max_connections=max_concurrent_requests),
            transport=AsyncHTTPTransport(retries=max_retries),
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _check_response_status_codes(self, response: Response) -> None:
        if response.status_code in RETRY_STATUS_CODES:
            raise MistralAPIStatusException.from_response(
                response,
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif 400 <= response.status_code < 500:
            if response.stream:
                await response.aread()
            raise MistralAPIException.from_response(
                response,
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif response.status_code >= 500:
            if response.stream:
                await response.aread()
            raise MistralException(
                message=f"Status: {response.status_code}. Message: {response.text}",
            )

    async def _check_streaming_response(self, response: Response) -> None:
        await self._check_response_status_codes(response)

    async def _check_response(self, response: Response) -> Dict[str, Any]:
        await self._check_response_status_codes(response)

        json_response: Dict[str, Any] = response.json()

        if "object" not in json_response:
            raise MistralException(message=f"Unexpected response: {json_response}")
        if "error" == json_response["object"]:  # has errors
            raise MistralAPIException.from_response(
                response,
                message=json_response["message"],
            )

        return json_response

    async def _request(
        self,
        method: str,
        json: Dict[str, Any],
        path: str,
        stream: bool = False,
        attempt: int = 1,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        accept_header = "text/event-stream" if stream else "application/json"
        headers = {
            "Accept": accept_header,
            "User-Agent": f"mistral-client-python/{self._version}",
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        url = posixpath.join(self._endpoint, path)

        self._logger.debug(f"Sending request: {method} {url} {json}")

        response: Response

        try:
            if stream:
                async with self._client.stream(
                    method,
                    url,
                    headers=headers,
                    json=json,
                ) as response:
                    await self._check_streaming_response(response)

                    async for line in response.aiter_lines():
                        json_streamed_response = self._process_line(line)
                        if json_streamed_response:
                            yield json_streamed_response

            else:
                response = await self._client.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                )

                yield await self._check_response(response)

        except ConnectError as e:
            raise MistralConnectionException(str(e)) from e
        except RequestError as e:
            raise MistralException(f"Unexpected exception ({e.__class__.__name__}): {e}") from e
        except JSONDecodeError as e:
            raise MistralAPIException.from_response(
                response,
                message=f"Failed to decode json body: {response.text}",
            ) from e
        except MistralAPIStatusException as e:
            attempt += 1
            if attempt > self._max_retries:
                raise MistralAPIStatusException.from_response(response, message=str(e)) from e
            backoff = 2.0**attempt  # exponential backoff
            time.sleep(backoff)

            # Retry as a generator
            async for r in self._request(method, json, path, stream=stream, attempt=attempt):
                yield r

    async def chat(
        self,
        messages: List[Any],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        safe_mode: bool = False,
        safe_prompt: bool = False,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        response_format: Optional[Union[Dict[str, str], ResponseFormat]] = None,
    ) -> ChatCompletionResponse:
        """A asynchronous chat endpoint that returns a single response.

        Args:
            model (str): model the name of the model to chat with, e.g. mistral-tiny
            messages (List[Any]): messages an array of messages to chat with, e.g.
                [{role: 'user', content: 'What is the best French cheese?'}]
            temperature (Optional[float], optional): temperature the temperature to use for sampling, e.g. 0.5.
            max_tokens (Optional[int], optional): the maximum number of tokens to generate, e.g. 100. Defaults to None.
            top_p (Optional[float], optional): the cumulative probability of tokens to generate, e.g. 0.9.
            Defaults to None.
            random_seed (Optional[int], optional): the random seed to use for sampling, e.g. 42. Defaults to None.
            safe_mode (bool, optional): deprecated, use safe_prompt instead. Defaults to False.
            safe_prompt (bool, optional): whether to use safe prompt, e.g. true. Defaults to False.

        Returns:
            ChatCompletionResponse: a response object containing the generated text.
        """
        request = self._make_chat_request(
            messages,
            model,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            random_seed=random_seed,
            stream=False,
            safe_prompt=safe_mode or safe_prompt,
            tool_choice=tool_choice,
            response_format=response_format,
        )

        single_response = self._request("post", request, "v1/chat/completions")

        async for response in single_response:
            return ChatCompletionResponse(**response)

        raise MistralException("No response received")

    async def chat_stream(
        self,
        messages: List[Any],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        safe_mode: bool = False,
        safe_prompt: bool = False,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        response_format: Optional[Union[Dict[str, str], ResponseFormat]] = None,
    ) -> AsyncGenerator[ChatCompletionStreamResponse, None]:
        """An Asynchronous chat endpoint that streams responses.

        Args:
            model (str): model the name of the model to chat with, e.g. mistral-tiny
            messages (List[Any]): messages an array of messages to chat with, e.g.
                [{role: 'user', content: 'What is the best French cheese?'}]
            tools (Optional[List[Function]], optional): a list of tools to use.
            temperature (Optional[float], optional): temperature the temperature to use for sampling, e.g. 0.5.
            max_tokens (Optional[int], optional): the maximum number of tokens to generate, e.g. 100. Defaults to None.
            top_p (Optional[float], optional): the cumulative probability of tokens to generate, e.g. 0.9.
            Defaults to None.
            random_seed (Optional[int], optional): the random seed to use for sampling, e.g. 42. Defaults to None.
            safe_mode (bool, optional): deprecated, use safe_prompt instead. Defaults to False.
            safe_prompt (bool, optional): whether to use safe prompt, e.g. true. Defaults to False.

        Returns:
            AsyncGenerator[ChatCompletionStreamResponse, None]:
                An async generator that yields ChatCompletionStreamResponse objects.
        """

        request = self._make_chat_request(
            messages,
            model,
            tools=tools,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            random_seed=random_seed,
            stream=True,
            safe_prompt=safe_mode or safe_prompt,
            tool_choice=tool_choice,
            response_format=response_format,
        )
        async_response = self._request("post", request, "v1/chat/completions", stream=True)

        async for json_response in async_response:
            yield ChatCompletionStreamResponse(**json_response)

    async def embeddings(self, model: str, input: Union[str, List[str]]) -> EmbeddingResponse:
        """An asynchronous embeddings endpoint that returns embeddings for a single, or batch of inputs

        Args:
            model (str): The embedding model to use, e.g. mistral-embed
            input (Union[str, List[str]]): The input to embed,
                 e.g. ['What is the best French cheese?']

        Returns:
            EmbeddingResponse: A response object containing the embeddings.
        """
        request = {"model": model, "input": input}
        single_response = self._request("post", request, "v1/embeddings")

        async for response in single_response:
            return EmbeddingResponse(**response)

        raise MistralException("No response received")

    async def list_models(self) -> ModelList:
        """Returns a list of the available models

        Returns:
            ModelList: A response object containing the list of models.
        """
        single_response = self._request("get", {}, "v1/models")

        async for response in single_response:
            return ModelList(**response)

        raise MistralException("No response received")
