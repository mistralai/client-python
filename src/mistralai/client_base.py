import logging
import os
from abc import ABC
from typing import Any, Callable, Dict, List, Optional, Union

import orjson
from httpx import Headers

from mistralai.constants import HEADER_MODEL_DEPRECATION_TIMESTAMP
from mistralai.exceptions import MistralException
from mistralai.models.chat_completion import (
    ChatMessage,
    Function,
    ResponseFormat,
    ToolChoice,
)

CLIENT_VERSION = "0.4.2"


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

    def _get_model(self, model: Optional[str] = None) -> str:
        if model is not None:
            return model
        else:
            if self._default_model is None:
                raise MistralException(message="model must be provided")
            return self._default_model

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

    def _check_model_deprecation_header_callback_factory(self, model: Optional[str] = None) -> Callable:
        model = self._get_model(model)

        def _check_model_deprecation_header_callback(
            headers: Headers,
        ) -> None:
            if HEADER_MODEL_DEPRECATION_TIMESTAMP in headers:
                self._logger.warning(
                    f"WARNING: The model {model} is deprecated "
                    f"and will be removed on {headers[HEADER_MODEL_DEPRECATION_TIMESTAMP]}. "
                    "Please refer to https://docs.mistral.ai/getting-started/models/#api-versioning "
                    "for more information."
                )

        return _check_model_deprecation_header_callback

    def _make_completion_request(
        self,
        prompt: str,
        model: Optional[str] = None,
        suffix: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        stop: Optional[List[str]] = None,
        stream: Optional[bool] = False,
    ) -> Dict[str, Any]:
        request_data: Dict[str, Any] = {
            "prompt": prompt,
            "suffix": suffix,
            "model": model,
            "stream": stream,
        }

        if stop is not None:
            request_data["stop"] = stop

        request_data["model"] = self._get_model(model)

        request_data.update(
            self._build_sampling_params(
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                random_seed=random_seed,
            )
        )

        self._logger.debug(f"Completion request: {request_data}")

        return request_data

    def _build_sampling_params(
        self,
        max_tokens: Optional[int],
        random_seed: Optional[int],
        temperature: Optional[float],
        top_p: Optional[float],
    ) -> Dict[str, Any]:
        params = {}
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if top_p is not None:
            params["top_p"] = top_p
        if random_seed is not None:
            params["random_seed"] = random_seed
        return params

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
        }

        request_data["model"] = self._get_model(model)

        request_data.update(
            self._build_sampling_params(
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                random_seed=random_seed,
            )
        )

        if safe_prompt:
            request_data["safe_prompt"] = safe_prompt
        if tools is not None:
            request_data["tools"] = self._parse_tools(tools)
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
