import asyncio
import logging
import posixpath
import time
from collections import defaultdict
from json import JSONDecodeError
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, List, Optional, Union

import aiohttp
import backoff
import orjson

from mistral_client.client_base import ClientBase
from mistral_client.constants import ENDPOINT, RETRY_STATUS_CODES
from mistral_client.exceptions import (
    MistralAPIException,
    MistralConnectionException,
    MistralException,
)
from mistral_client.models.chat_completion import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
)
from mistral_client.models.embeddings import EmbeddingResponse
from mistral_client.models.models import ModelList


class AIOHTTPBackend:
    """HTTP backend which handles retries, concurrency limiting and logging"""

    SLEEP_AFTER_FAILURE = defaultdict(lambda: 0.25, {429: 5.0})

    _requester: Callable[..., Awaitable[aiohttp.ClientResponse]]
    _semaphore: asyncio.Semaphore
    _session: Optional[aiohttp.ClientSession]

    def __init__(
        self,
        max_concurrent_requests: int = 64,
        max_retries: int = 5,
        timeout: int = 120,
    ):
        self._logger = logging.getLogger(__name__)
        self._timeout = timeout
        self._max_retries = max_retries
        self._session = None
        self._max_concurrent_requests = max_concurrent_requests

    def build_aio_requester(
        self,
    ) -> Callable:  # returns a function for retryable requests
        @backoff.on_exception(
            backoff.expo,
            (aiohttp.ClientError, aiohttp.ClientResponseError),
            max_tries=self._max_retries + 1,
            max_time=self._timeout,
        )
        async def make_request_fn(
            session: aiohttp.ClientSession, *args: Any, **kwargs: Any
        ) -> aiohttp.ClientResponse:
            async with self._semaphore:  # this limits total concurrency by the client
                response = await session.request(*args, **kwargs)
            if (
                response.status in RETRY_STATUS_CODES
            ):  # likely temporary, raise to retry
                self._logger.info(f"Received status {response.status}, retrying...")
                await asyncio.sleep(self.SLEEP_AFTER_FAILURE[response.status])
                response.raise_for_status()

            return response

        return make_request_fn

    async def request(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        method: str = "post",
        headers: Optional[Dict[str, Any]] = None,
        session: Optional[aiohttp.ClientSession] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        session = session or await self.session()
        self._logger.debug(f"Making request to {url} with content {json}")

        request_start = time.time()
        try:
            response = await self._requester(
                session,
                method,
                url,
                headers=headers,
                json=json,
                params=params,
                **kwargs,
            )
        except (
            aiohttp.ClientConnectionError
        ) as e:  # ensure the SDK user does not have to deal with knowing aiohttp
            self._logger.debug(
                f"Fatal connection error after {time.time()-request_start:.1f}s: {e}"
            )
            raise MistralConnectionException(str(e)) from e
        except (
            aiohttp.ClientResponseError
        ) as e:  # status 500 or something remains after retries
            self._logger.debug(
                f"Fatal ClientResponseError error after {time.time()-request_start:.1f}s: {e}"
            )
            raise MistralConnectionException(str(e)) from e
        except asyncio.TimeoutError as e:
            self._logger.debug(
                f"Fatal timeout error after {time.time()-request_start:.1f}s: {e}"
            )
            raise MistralConnectionException("The request timed out") from e
        except Exception as e:  # Anything caught here should be added above
            self._logger.debug(
                f"Unexpected fatal error after {time.time()-request_start:.1f}s: {e}"
            )
            raise MistralException(
                f"Unexpected exception ({e.__class__.__name__}): {e}"
            ) from e

        self._logger.debug(
            f"Received response with status {response.status} after {time.time()-request_start:.1f}s"
        )
        return response

    async def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(self._timeout),
                connector=aiohttp.TCPConnector(limit=0),
            )
            self._semaphore = asyncio.Semaphore(self._max_concurrent_requests)
            self._requester = self.build_aio_requester()
        return self._session

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    def __del__(self) -> None:
        # https://stackoverflow.com/questions/54770360/how-can-i-wait-for-an-objects-del-to-finish-before-the-async-loop-closes
        if self._session:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
                else:
                    loop.run_until_complete(self.close())
            except Exception:
                pass


class MistralAsyncClient(ClientBase):
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = ENDPOINT,
        max_retries: int = 5,
        timeout: int = 120,
        max_concurrent_requests: int = 64,
    ):
        super().__init__(endpoint, api_key, max_retries, timeout)

        self._backend = AIOHTTPBackend(
            max_concurrent_requests=max_concurrent_requests,
            max_retries=max_retries,
            timeout=timeout,
        )

    async def _request(
        self,
        method: str,
        json: Dict[str, Any],
        path: str,
        stream: bool = False,
        params: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], aiohttp.ClientResponse]:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        url = posixpath.join(self._endpoint, path)

        response = await self._backend.request(
            url, json, method, headers, params=params
        )
        if stream:
            return response

        try:
            json_response: Dict[str, Any] = await response.json()
        except JSONDecodeError:
            raise MistralAPIException.from_aio_response(
                response, message=f"Failed to decode json body: {await response.text()}"
            )
        except aiohttp.ClientPayloadError as e:
            raise MistralAPIException.from_aio_response(
                response,
                message=f"An unexpected error occurred while receiving the response: {e}",
            )

        self._logger.debug(f"JSON response: {json_response}")
        self._check_response(json_response, dict(response.headers), response.status)
        return json_response

    async def chat(
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

        response = await self._request("post", request, "v1/chat/completions")
        assert isinstance(response, dict), "Bad response from _request"
        return ChatCompletionResponse(**response)

    async def chat_stream(
        self,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        safe_mode: bool = True,
    ) -> AsyncGenerator[ChatCompletionStreamResponse, None]:
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
        async_response = await self._request(
            "post", request, "v1/chat/completions", stream=True
        )

        assert isinstance(
            async_response, aiohttp.ClientResponse
        ), "Bad response from _request"

        async with async_response as response:
            async for line in response.content:
                self._logger.debug(f"Received line: {line.decode()}")
                if line == b"\n":
                    continue

                if line.startswith(b"data: "):
                    line = line[6:].strip()
                    if line != b"[DONE]":
                        json_response = orjson.loads(line)
                        yield ChatCompletionStreamResponse(**json_response)

    async def embeddings(
        self, model: str, input: Union[str, List[str]]
    ) -> EmbeddingResponse:
        request = {"model": model, "input": input}
        response = await self._request("post", request, "v1/embeddings")
        assert isinstance(response, dict), "Bad response from _request"
        return EmbeddingResponse(**response)

    async def list_models(self) -> ModelList:
        response = await self._request("get", {}, "v1/models")
        assert isinstance(response, dict), "Bad response from _request"
        return ModelList(**response)
