import logging
import os
from abc import ABC
from typing import Any, Dict, List, Optional

import orjson
from httpx import Response

from mistralai.constants import RETRY_STATUS_CODES
from mistralai.exceptions import (
    MistralAPIException,
    MistralAPIStatusException,
    MistralException,
)
from mistralai.models.chat_completion import ChatMessage, Function

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

        # This should be automatically updated by the deploy script
        self._version = "0.0.1"

    def _parse_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_tools: List[Dict[str, Any]] = []
        for tool in tools:
            if tool["type"] == "function":
                parsed_function = {}
                parsed_function["type"] = tool["type"]
                if isinstance(tool["function"], Function):
                    parsed_function["function"] = tool["function"].model_dump(exclude_none=True)
                else:
                    parsed_function["function"] = tool["function"]

                parsed_tools.append(parsed_function)

        return parsed_tools

    def _parse_messages(self, messages: List[Any]) -> List[Dict[str, Any]]:
        parsed_messages: List[Dict[str, Any]] = []
        for message in messages:
            if isinstance(message, ChatMessage):
                parsed_messages.append(message.model_dump(exclude_none=True))
            else:
                parsed_messages.append(message)

        return parsed_messages

    def _make_chat_request(
        self,
        model: str,
        messages: List[Any],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        stream: Optional[bool] = None,
        safe_prompt: Optional[bool] = False,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "model": model,
            "messages": self._parse_messages(messages),
            "safe_prompt": safe_prompt,
        }
        if tools is not None:
            request_data["tools"] = self._parse_tools(tools)
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
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif 400 <= response.status_code < 500:
            raise MistralAPIException.from_response(
                response,
                message=f"Status: {response.status_code}. Message: {response.text}",
            )
        elif response.status_code >= 500:
            raise MistralException(
                message=f"Status: {response.status_code}. Message: {response.text}",
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
