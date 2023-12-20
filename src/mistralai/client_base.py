import logging
import os
import orjson
from httpx import Response
from abc import ABC
from typing import Any, Dict, List, Optional

from mistralai.constants import RETRY_STATUS_CODES
from mistralai.exceptions import (
    MistralAPIException,
    MistralException,
    MistralAPIStatusException,
)
from mistralai.models.chat_completion import ChatMessage

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=os.getenv("LOG_LEVEL", "ERROR"),
)


class ClientBase(ABC):
    def __init__(
        self,
        endpoint: str,
        api_key: Optional[str] = None,
        max_retries: int = 5,
        timeout: int = 120,
    ):
        self._max_retries = max_retries
        self._timeout = timeout

        self._endpoint = endpoint
        self._api_key = api_key
        self._logger = logging.getLogger(__name__)

    def _make_chat_request(
        self,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        stream: Optional[bool] = None,
        safe_mode: Optional[bool] = False,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "model": model,
            "messages": [msg.model_dump() for msg in messages],
            "safe_prompt": safe_mode,
        }
        if temperature is not None:
            request_data["temperature"] = temperature
        if max_tokens is not None:
            request_data["max_tokens"] = max_tokens
        if top_p is not None:
            request_data["top_p"] = top_p
        if random_seed is not None:
            request_data["random_seed"] = random_seed
        if stream is not None:
            request_data["stream"] = stream

        self._logger.debug(f"Chat request: {request_data}")

        return request_data

    def _check_response_status_codes(self, response: Response) -> None:
        if response.status_code in RETRY_STATUS_CODES:
            raise MistralAPIStatusException.from_response(
                response,
                message=f"Cannot stream response. Status: {response.status_code}",
            )
        elif 400 <= response.status_code < 500:
            raise MistralAPIException.from_response(
                response,
                message=f"Cannot stream response. Status: {response.status_code}",
            )
        elif response.status_code >= 500:
            raise MistralException(
                message=f"Unexpected server error (status {response.status_code})"
            )

    def _check_streaming_response(self, response: Response) -> None:
        self._check_response_status_codes(response)

    def _check_response(self, response: Response) -> Dict[str, Any]:
        self._check_response_status_codes(response)

        json_response: Dict[str, Any] = response.json()

        if "object" not in json_response:
            raise MistralException(message=f"Unexpected response: {json_response}")
        if "error" == json_response["object"]:  # has errors
            raise MistralAPIException.from_response(
                response,
                message=json_response["message"],
            )

        return json_response

    def _process_line(self, line: str) -> Optional[Dict[str, Any]]:
        if line.startswith("data: "):
            line = line[6:].strip()
            if line != "[DONE]":
                json_streamed_response: Dict[str, Any] = orjson.loads(line)
                return json_streamed_response
        return None
