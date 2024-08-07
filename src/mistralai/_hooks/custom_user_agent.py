# MAKE SURE YOU UPDATE THE COPIES OF THIS FILES IN THE PROVIDERS'S PACKAGES WHEN YOU MAKE CHANGES HERE
from typing import Union

import httpx

from .types import BeforeRequestContext, BeforeRequestHook


class CustomUserAgentHook(BeforeRequestHook):
    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        request.headers["user-agent"] = (
            "mistral-client-python/" + request.headers["user-agent"].split(" ")[1]
        )
        return request
