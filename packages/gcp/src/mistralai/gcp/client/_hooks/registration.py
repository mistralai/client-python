import json
import logging
from .types import BeforeRequestHook, BeforeRequestContext, Hooks
import httpx

logger = logging.getLogger(__name__)


# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


class GCPVertexAIPathHook(BeforeRequestHook):
    """Build full Vertex AI URL path from project_id, region, and model.

    Extracts model from request body and builds the Vertex AI URL dynamically.
    """

    def __init__(self, project_id: str, region: str):
        self.project_id = project_id
        self.region = region

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> httpx.Request:
        if not request.content:
            return request

        try:
            body = json.loads(request.content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            # Non-JSON body (e.g. multipart upload) — pass through unmodified
            return request

        model = body.get("model")
        if not model:
            logger.warning(
                "GCPVertexAIPathHook: request body has no 'model' field; "
                "Vertex AI path will not be constructed. "
                "Operation: %s",
                hook_ctx.operation_id,
            )
            return request

        is_streaming = "stream" in hook_ctx.operation_id.lower()
        specifier = "streamRawPredict" if is_streaming else "rawPredict"

        path = (
            f"/v1/projects/{self.project_id}/locations/{self.region}/"
            f"publishers/mistralai/models/{model}:{specifier}"
        )

        return httpx.Request(
            method=request.method,
            url=request.url.copy_with(path=path),
            headers=request.headers,
            content=request.content,
        )


def init_hooks(_hooks: Hooks) -> None:
    """Initialize hooks. Called by SDKHooks.__init__.

    Note: GCPVertexAIPathHook requires project_id and region, so it is
    registered separately in MistralGCP.__init__ after those values are known.
    """
