from __future__ import annotations

from typing import Any, Dict, Optional

from httpx import Response


class MistralException(Exception):
    """Base Exception class, returned when nothing more specific applies"""

    def __init__(self, message: Optional[str] = None) -> None:
        """
        Initializes a MistralException instance.

        Parameters
        ----------
        message : Optional[str], optional
            The error message, by default None.
        """
        super(MistralException, self).__init__(message)

        self.message = message

    def __str__(self) -> str:
        """
        Returns a string representation of the exception.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The error message.
        """
        msg = self.message or "<empty message>"
        return msg

    def __repr__(self) -> str:
        """
        Returns a string representation of the exception.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string containing the class name and error message.
        """
        return f"{self.__class__.__name__}(message={str(self)})"


class MistralAPIException(MistralException):
    """Returned when the API responds with an error message"""

    def __init__(
        self,
        message: Optional[str] = None,
        http_status: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initializes a MistralAPIException instance.

        Parameters
        ----------
        message : Optional[str], optional
            The error message, by default None.

        http_status : Optional[int], optional
            The HTTP status code, by default None.

        headers : Optional[Dict[str, Any]], optional
            The response headers, by default None.
        """
        super().__init__(message)
        self.http_status = http_status
        self.headers = headers or {}

    @classmethod
    def from_response(
        cls, response: Response, message: Optional[str] = None
    ) -> MistralAPIException:
        """
        Create a MistralAPIException from an HTTP response.

        Parameters
        ----------
        response : Response
            The HTTP response object.

        message : Optional[str], optional
            The error message, by default None.

        Returns
        -------
        MistralAPIException
            A MistralAPIException instance.
        """
        return cls(
            message=message or response.text,
            http_status=response.status_code,
            headers=dict(response.headers),
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the exception.

        Parameters
        ----------
        None

        Returns
        -------
        str
            A string containing the class name, error message, and HTTP status code.
        """
        return f"{self.__class__.__name__}(message={str(self)}, http_status={self.http_status})"

class MistralAPIStatusException(MistralAPIException):
    """Returned when we receive a non-200 response from the API that we should retry"""

class MistralConnectionException(MistralException):
    """Returned when the SDK can not reach the API server for any reason"""
