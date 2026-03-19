import logging

import httpx

from .types import BeforeRequestContext, BeforeRequestHook, Hooks

logger = logging.getLogger(__name__)


# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


class AzureServerlessPathHook(BeforeRequestHook):
    """Rewrite URL paths for legacy Azure serverless endpoints.

    After the spec update, operation paths match Foundry Resource format:
      - Chat: /models/chat/completions
      - OCR:  /providers/mistral/azure/ocr

    Legacy serverless endpoints (*.models.ai.azure.com) use different paths:
      - Chat: /chat/completions
      - OCR:  /ocr

    This hook rewrites Foundry paths back to serverless paths when
    is_foundry=False.
    """

    SERVERLESS_PATHS: dict[str, str] = {
        "chat": "/chat/completions",
        "ocr": "/ocr",
    }

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> httpx.Request:
        for key, path in self.SERVERLESS_PATHS.items():
            if key in hook_ctx.operation_id:
                query = b""
                if b"?" in request.url.raw_path:
                    query = b"?" + request.url.raw_path.split(b"?", 1)[1]
                return httpx.Request(
                    method=request.method,
                    url=request.url.copy_with(
                        raw_path=path.encode("ascii") + query,
                    ),
                    headers=request.headers,
                    content=request.content,
                )
        return request


def init_hooks(_hooks: Hooks) -> None:
    """Initialize hooks. Called by SDKHooks.__init__.

    Note: AzureServerlessPathHook requires is_foundry context, so it is
    registered separately in MistralAzure.__init__ when is_foundry=False.
    """
