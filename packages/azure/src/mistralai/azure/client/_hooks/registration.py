from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

from mistralai.azure.client.httpclient import HttpClient

from .types import Hooks, SDKInitHook


# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


def _normalize_azure_base_url(base_url: str) -> str:
    """
    Users frequently copy operation-scoped "Target URI" values from Azure AI Foundry,
    e.g. endpoints ending in `/ocr` or `/chat/completions`.

    The generated SDK operations append their own paths (OCR uses path="/ocr", chat uses
    path="/chat/completions"), so if the base_url already ends with those suffixes the
    resulting URL becomes duplicated (e.g. .../ocr/ocr) and fails.
    """

    parts = urlsplit(base_url)
    path = parts.path.rstrip("/")

    known_suffixes = ("/ocr", "/chat/completions")
    for suffix in known_suffixes:
        if path.endswith(suffix):
            path = path[: -len(suffix)].rstrip("/")
            break

    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


class _NormalizeBaseUrlHook(SDKInitHook):
    def sdk_init(self, base_url: str, client: HttpClient):
        return _normalize_azure_base_url(base_url), client


def init_hooks(_hooks: Hooks) -> None:
    """Add hooks by calling hooks.register{sdk_init/before_request/after_success/after_error}Hook
    with an instance of a hook that implements that specific Hook interface
    Hooks are registered per SDK instance, and are valid for the lifetime of the SDK instance"""

    _hooks.register_sdk_init_hook(_NormalizeBaseUrlHook())
