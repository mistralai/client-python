import os
from pathlib import Path
from typing import Optional

import httpx2 as httpx

from mistralai.extra.exceptions import MistralClientException

from .types import BeforeRequestContext, BeforeRequestHook

MISTRAL_SA_TOKEN_PATH_ENV = "MISTRAL_SA_TOKEN_PATH"


class ServiceAccountTokenError(MistralClientException):
    """Raised when the configured service-account token file cannot be read."""


def read_service_account_token() -> Optional[str]:
    """Read the token at ``MISTRAL_SA_TOKEN_PATH``, or None when it is unset.

    Uncached so kubelet rotation is picked up: the read is negligible next to the request, and
    caching would need the token's expiry, which would drag a JWT dependency into the client.
    """
    path = os.getenv(MISTRAL_SA_TOKEN_PATH_ENV)
    if not path:
        return None
    try:
        token = Path(path).read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ServiceAccountTokenError(
            f"Failed to read service-account token from {path}"
        ) from exc
    if not token:
        raise ServiceAccountTokenError(f"Service-account token file is empty: {path}")
    return token


def bearer_header(token: str) -> str:
    return token if token.lower().startswith("bearer ") else f"Bearer {token}"


def _env_authorization() -> Optional[str]:
    api_key = os.getenv("MISTRAL_API_KEY")
    return bearer_header(api_key) if api_key else None


class ServiceAccountAuthHook(BeforeRequestHook):
    """Authenticates from ``MISTRAL_SA_TOKEN_PATH`` when no api_key was passed.

    Yields the precedence per-request headers > explicit api_key > SA token > ``MISTRAL_API_KEY``.
    The generated security layer already covers the explicit key and ``MISTRAL_API_KEY``.
    """

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> httpx.Request:
        if hook_ctx.config.security is not None:
            return request
        # http_headers are applied at build time, before hooks run. Anything other than the env
        # key's header came from the caller and outranks the service-account token.
        existing = request.headers.get("Authorization")
        if existing is not None and existing != _env_authorization():
            return request
        token = read_service_account_token()
        if token is None:
            return request
        request.headers["Authorization"] = bearer_header(token)
        return request
