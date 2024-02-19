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

        # This should be automatically updated by the deploy script
        self._version = "0.0.1"

    def _make_chat_request(
        self,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        random_seed: Optional[int] = None,
        stream: Optional[bool] = None,
        safe_prompt: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Constructs a request payload for making a chat request to the Mistral AI API.

        Parameters
        ----------
        model : str
            The model to be used for generating chat responses.

        messages : List[ChatMessage]
            A list of chat messages exchanged between users.

        temperature : float, optional
            The randomness of the generated responses. Higher values produce more random outputs. Default is None.

        max_tokens : int, optional
            The maximum number of tokens (words) to generate in the response. Default is None.

        top_p : float, optional
            Nucleus sampling parameter for controlling diversity in the generated responses. Default is None.

        random_seed : int, optional
            A seed value for controlling randomization in response generation. Default is None.

        stream : bool, optional
            Flag indicating whether to stream the response or not. Default is None.

        safe_prompt : bool, optional
            Flag indicating whether the prompt should be handled safely. Default is False.

        Returns
        -------
        request_data : Dict[str, Any]
            The constructed request payload to be sent to the Mistral AI API.
        """
        request_data: Dict[str, Any] = {
            "model": model,
            "messages": [msg.model_dump() for msg in messages],
            "safe_prompt": safe_prompt,
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
        """
        Checks the status codes of the HTTP response and raises exceptions if necessary.

        Parameters
        ----------
        response : Response
            The HTTP response object.

        Raises
        ------
        MistralAPIStatusException
            If the status code indicates a retryable error.

        MistralAPIException
            If the status code indicates a client error.

        MistralException
            If the status code indicates a server error.
        """
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
        """
        Checks the status codes of the HTTP streaming response and raises exceptions if necessary.

        Parameters
        ----------
        response : Response
            The HTTP response object.

        Raises
        ------
        MistralAPIStatusException
            If the status code indicates a retryable error.

        MistralAPIException
            If the status code indicates a client error.

        MistralException
            If the status code indicates a server error.
        """
        self._check_response_status_codes(response)

    def _check_response(self, response: Response) -> Dict[str, Any]:
        """
        Checks the status codes of the HTTP response, processes the JSON response, and raises exceptions if necessary.

        Parameters
        ----------
        response : Response
            The HTTP response object.

        Returns
        -------
        json_response : Dict[str, Any]
            The JSON response from the server.

        Raises
        ------
        MistralAPIStatusException
            If the status code indicates a retryable error.

        MistralAPIException
            If the status code indicates a client error.

        MistralException
            If the status code indicates a server error.

        MistralException
            If the response does not contain the expected JSON structure.
        """
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
        """
        Processes a line of text from a streamed response.

        Parameters
        ----------
        line : str
            A line of text from the streamed response.

        Returns
        -------
        json_streamed_response : Optional[Dict[str, Any]]
            The JSON response parsed from the input line, or None if the line does not contain valid JSON data.
        """
        if line.startswith("data: "):
            line = line[6:].strip()
            if line != "[DONE]":
                json_streamed_response: Dict[str, Any] = orjson.loads(line)
                return json_streamed_response
        return None
