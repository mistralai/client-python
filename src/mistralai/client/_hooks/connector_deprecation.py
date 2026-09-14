import warnings
from typing import Union

import httpx

from .types import BeforeRequestContext, BeforeRequestHook


class ConnectorToolDeprecationHook(BeforeRequestHook):
    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        if hook_ctx.operation_id == "connector_call_tool_v1":
            warnings.warn(
                "call_tool and call_tool_async are deprecated; use "
                "call_mcp_tool_async to call the connectors gateway directly.",
                DeprecationWarning,
                stacklevel=5,
            )
        return request
