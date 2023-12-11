import logging
from abc import ABC
from typing import Any, Dict, List, Optional

from mistralai.exceptions import MistralAPIException, MistralException
from mistralai.models.chat_completion import ChatMessage


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

    @staticmethod
    def _make_chat_request(
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

        return request_data

    def _check_response(
        self, json_response: Dict[str, Any], headers: Dict[str, Any], status: int
    ) -> None:
        if "object" not in json_response:
            raise MistralException(message=f"Unexpected response: {json_response}")
        if "error" == json_response["object"]:  # has errors
            raise MistralAPIException(
                message=json_response["message"],
                http_status=status,
                headers=headers,
            )
        if 400 <= status < 500:
            raise MistralAPIException(
                message=f"Unexpected client error (status {status}): {json_response}",
                http_status=status,
                headers=headers,
            )
        if status >= 500:
            raise MistralException(
                message=f"Unexpected server error (status {status}): {json_response}"
            )
