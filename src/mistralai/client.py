import os
import posixpath
import time
from json import JSONDecodeError
from typing import Any, Dict, Iterable, Iterator, List, Optional, Union

import orjson
from httpx import Response, Client, HTTPTransport, RequestError, ConnectError

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
    ChatMessage,
)
from mistralai.models.embeddings import EmbeddingResponse
from mistralai.models.models import ModelList


class MistralClient(ClientBase):
    """
    Synchronous wrapper around the async client
    """

    def __init__(
        self,
        api_key: Optional[str] = os.environ.get("MISTRAL_API_KEY", None),
        endpoint: str = ENDPOINT,
        max_retries: int = 5,
        timeout: int = 120,
    ):
        super().__init__(endpoint, api_key, max_retries, timeout)

        self._client = Client(
            follow_redirects=True,
            timeout=self._timeout,
            transport=HTTPTransport(retries=self._max_retries))

    def __del__(self) -> None:
        self._client.close()

    def _request(
        self,
        method: str,
        json: Dict[str, Any],
        path: str,
        stream: bool = False,
        attempt: int = 1,
    ) -> Iterator[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        url = posixpath.join(self._endpoint, path)

        self._logger.debug(f"Sending request: {method} {url} {json}")

        response: Response

        try:
            if stream:
                self._logger.debug("Streaming Response")
                with self._client.stream(
                    method,
                    url,
                    headers=headers,
                    json=json,
                ) as response:
                    if response.status_code in RETRY_STATUS_CODES:
                        raise MistralAPIStatusException.from_response(
                            response,
                            message=f"Cannot stream response. Status: {response.status_code}",
                        )

                    self._check_response(
                        dict(response.headers),
                        response.status_code,
                    )

                    for line in response.iter_lines():
                        self._logger.debug(f"Received line: {line}")

                        if line.startswith("data: "):
                            line = line[6:].strip()
                            if line != "[DONE]":
                                try:
                                    json_streamed_response = orjson.loads(line)
                                except JSONDecodeError:
                                    raise MistralAPIException.from_response(
                                        response,
                                        message=f"Failed to decode json body: {json_streamed_response}",
                                    )

                                yield json_streamed_response

            else:
                self._logger.debug("Non-Streaming Response")
                response = self._client.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                )

                self._logger.debug(f"Received response: {response}")

                if response.status_code in RETRY_STATUS_CODES:
                    raise MistralAPIStatusException.from_response(response)

                try:
                    json_response: Dict[str, Any] = response.json()
                except JSONDecodeError:
                    raise MistralAPIException.from_response(
                        response,
                        message=f"Failed to decode json body: {response.text}",
                    )

                self._check_response(
                    dict(response.headers), response.status_code, json_response
                )
                yield json_response

        except ConnectError as e:
            raise MistralConnectionException(str(e)) from e
        except RequestError as e:
            raise MistralException(
                f"Unexpected exception ({e.__class__.__name__}): {e}"
            ) from e
        except MistralAPIStatusException as e:
            attempt += 1
            if attempt > self._max_retries:
                raise MistralAPIStatusException.from_response(
                    response, message=str(e)
                ) from e
            backoff = 2.0**attempt  # exponential backoff
            time.sleep(backoff)

            # Retry as a generator
            for r in self._request(method, json, path, stream=stream, attempt=attempt):
                yield r

    def chat(
        self,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        safe_mode: bool = False,
    ) -> ChatCompletionResponse:
        """A chat endpoint that returns a single response.

        Args:
            model (str): model the name of the model to chat with, e.g. mistral-tiny
            messages (List[ChatMessage]): messages an array of messages to chat with, e.g.
                [{role: 'user', content: 'What is the best French cheese?'}]
            temperature (Optional[float], optional): temperature the temperature to use for sampling, e.g. 0.5.
            max_tokens (Optional[int], optional): the maximum number of tokens to generate, e.g. 100. Defaults to None.
            top_p (Optional[float], optional): the cumulative probability of tokens to generate, e.g. 0.9.
            Defaults to None.
            random_seed (Optional[int], optional): the random seed to use for sampling, e.g. 42. Defaults to None.
            safe_mode (bool, optional): whether to use safe mode, e.g. true. Defaults to False.

        Returns:
            ChatCompletionResponse: a response object containing the generated text.
        """
        request = self._make_chat_request(
            model,
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            random_seed=random_seed,
            stream=False,
            safe_mode=safe_mode,
        )

        single_response = self._request("post", request, "v1/chat/completions")

        for response in single_response:
            return ChatCompletionResponse(**response)

        raise MistralException("No response received")

    def chat_stream(
        self,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        safe_mode: bool = False,
    ) -> Iterable[ChatCompletionStreamResponse]:
        """A chat endpoint that streams responses.

        Args:
            model (str): model the name of the model to chat with, e.g. mistral-tiny
            messages (List[ChatMessage]): messages an array of messages to chat with, e.g.
                [{role: 'user', content: 'What is the best French cheese?'}]
            temperature (Optional[float], optional): temperature the temperature to use for sampling, e.g. 0.5.
            max_tokens (Optional[int], optional): the maximum number of tokens to generate, e.g. 100. Defaults to None.
            top_p (Optional[float], optional): the cumulative probability of tokens to generate, e.g. 0.9.
            Defaults to None.
            random_seed (Optional[int], optional): the random seed to use for sampling, e.g. 42. Defaults to None.
            safe_mode (bool, optional): whether to use safe mode, e.g. true. Defaults to False.

        Returns:
             Iterable[ChatCompletionStreamResponse]:
                A generator that yields ChatCompletionStreamResponse objects.
        """
        request = self._make_chat_request(
            model,
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            random_seed=random_seed,
            stream=True,
            safe_mode=safe_mode,
        )

        response = self._request("post", request, "v1/chat/completions", stream=True)

        for json_streamed_response in response:
            yield ChatCompletionStreamResponse(**json_streamed_response)

    def embeddings(self, model: str, input: Union[str, List[str]]) -> EmbeddingResponse:
        """An embeddings endpoint that returns embeddings for a single, or batch of inputs

        Args:
            model (str): The embedding model to use, e.g. mistral-embed
            input (Union[str, List[str]]): The input to embed,
                 e.g. ['What is the best French cheese?']

        Returns:
            EmbeddingResponse: A response object containing the embeddings.
        """
        request = {"model": model, "input": input}
        singleton_response = self._request("post", request, "v1/embeddings")

        for response in singleton_response:
            return EmbeddingResponse(**response)
        
        raise MistralException("No response received")

    def list_models(self) -> ModelList:
        """Returns a list of the available models

        Returns:
            ModelList: A response object containing the list of models.
        """
        singleton_response = self._request("get", {}, "v1/models")

        for response in singleton_response:
            return ModelList(**response)
        
        raise MistralException("No response received")
