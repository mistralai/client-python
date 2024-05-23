import logging
import os
from abc import ABC
from typing import Any, Dict, List, Optional, Union

import orjson

from mistralai.exceptions import (
    MistralException,
)
from mistralai.models.chat_completion import ChatMessage, Function, ResponseFormat, ToolChoice

CLIENT_VERSION = "0.2.0"


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

        if api_key is None:
            api_key = os.environ.get("MISTRAL_API_KEY")
        if api_key is None:
            raise MistralException(message="API key not provided. Please set MISTRAL_API_KEY environment variable.")
        self._api_key = api_key
        self._endpoint = endpoint
        self._logger = logging.getLogger(__name__)

        # For azure endpoints, we default to the mistral model
        if "inference.azure.com" in self._endpoint:
            self._default_model = "mistral"

        self._version = CLIENT_VERSION

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

    def _parse_tool_choice(self, tool_choice: Union[str, ToolChoice]) -> str:
        if isinstance(tool_choice, ToolChoice):
            return tool_choice.value
        return tool_choice

    def _parse_response_format(self, response_format: Union[Dict[str, Any], ResponseFormat]) -> Dict[str, Any]:
        if isinstance(response_format, ResponseFormat):
            return response_format.model_dump(exclude_none=True)
        return response_format

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
        messages: List[Any],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        stream: Optional[bool] = None,
        safe_prompt: Optional[bool] = False,
        tool_choice: Optional[Union[str, ToolChoice]] = None,
        response_format: Optional[Union[Dict[str, str], ResponseFormat]] = None,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "messages": self._parse_messages(messages),
            "safe_prompt": safe_prompt,
        }

        if model is not None:
            request_data["model"] = model
        else:
            if self._default_model is None:
                raise MistralException(message="model must be provided")
            request_data["model"] = self._default_model

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

        if tool_choice is not None:
            request_data["tool_choice"] = self._parse_tool_choice(tool_choice)
        if response_format is not None:
            request_data["response_format"] = self._parse_response_format(response_format)

        self._logger.debug(f"Chat request: {request_data}")

        return request_data

    def _process_line(self, line: str) -> Optional[Dict[str, Any]]:
        if line.startswith("data: "):
            line = line[6:].strip()
            if line != "[DONE]":
                json_streamed_response: Dict[str, Any] = orjson.loads(line)
                return json_streamed_response
        return None
