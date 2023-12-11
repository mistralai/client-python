import os
import posixpath
from json import JSONDecodeError
from typing import Any, Dict, Iterable, List, Optional, Union

import orjson
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from mistralai.client_base import ClientBase
from mistralai.constants import ENDPOINT, RETRY_STATUS_CODES
from mistralai.exceptions import (
    MistralAPIException,
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

    def _request(
        self,
        method: str,
        json: Dict[str, Any],
        path: str,
        stream: bool = False,
        params: Optional[Dict[str, Any]] = None,
    ) -> Union[Response, Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        url = posixpath.join(self._endpoint, path)

        with requests.Session() as session:
            retries = Retry(
                total=self._max_retries,
                backoff_factor=0.5,
                allowed_methods=["POST", "GET"],
                status_forcelist=RETRY_STATUS_CODES,
                raise_on_status=False,
            )
            session.mount("https://", HTTPAdapter(max_retries=retries))
            session.mount("http://", HTTPAdapter(max_retries=retries))

            if stream:
                return session.request(
                    method, url, headers=headers, json=json, stream=True
                )

            try:
                response = session.request(
                    method,
                    url,
                    headers=headers,
                    json=json,
                    timeout=self._timeout,
                    params=params,
                )
            except requests.exceptions.ConnectionError as e:
                raise MistralConnectionException(str(e)) from e
            except requests.exceptions.RequestException as e:
                raise MistralException(
                    f"Unexpected exception ({e.__class__.__name__}): {e}"
                ) from e

            try:
                json_response: Dict[str, Any] = response.json()
            except JSONDecodeError:
                raise MistralAPIException.from_response(
                    response, message=f"Failed to decode json body: {response.text}"
                )

            self._check_response(
                json_response, dict(response.headers), response.status_code
            )
        return json_response

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
        """ A chat endpoint that returns a single response.

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

        response = self._request("post", request, "v1/chat/completions")

        assert isinstance(response, dict), "Bad response from _request"

        return ChatCompletionResponse(**response)

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
        """ A chat endpoint that streams responses.

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

        assert isinstance(response, Response), "Bad response from _request"

        for line in response.iter_lines():
            self._logger.debug(f"Received line: {line}")
            if line == b"\n":
                continue

            if line.startswith(b"data: "):
                line = line[6:].strip()
                if line != b"[DONE]":
                    json_response = orjson.loads(line)
                    yield ChatCompletionStreamResponse(**json_response)

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
        response = self._request("post", request, "v1/embeddings")
        assert isinstance(response, dict), "Bad response from _request"
        return EmbeddingResponse(**response)

    def list_models(self) -> ModelList:
        """Returns a list of the available models

        Returns:
            ModelList: A response object containing the list of models.
        """
        response = self._request("get", {}, "v1/models")
        assert isinstance(response, dict), "Bad response from _request"
        return ModelList(**response)
