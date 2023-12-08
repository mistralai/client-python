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
        api_key: Optional[str] = None,
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
        safe_mode: bool = True,
    ) -> ChatCompletionResponse:
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
        safe_mode: bool = True,
    ) -> Iterable[ChatCompletionStreamResponse]:
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
        request = {"model": model, "input": input}
        response = self._request("post", request, "v1/embeddings")
        assert isinstance(response, dict), "Bad response from _request"
        return EmbeddingResponse(**response)

    def list_models(self) -> ModelList:
        response = self._request("get", {}, "v1/models")
        assert isinstance(response, dict), "Bad response from _request"
        return ModelList(**response)
