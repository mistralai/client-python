# MAKE SURE YOU UPDATE THE COPIES OF THIS FILES IN THE PROVIDERS'S PACKAGES WHEN YOU MAKE CHANGES HERE
from typing import Union

import httpx

from .types import BeforeRequestContext, BeforeRequestHook

prefix = "mistral-client-python/"

class CustomUserAgentHook(BeforeRequestHook):
    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> Union[httpx.Request, Exception]:
        current = request.headers["user-agent"]
        if current.startswith(prefix):
            return request
        
        request.headers["user-agent"] = (
            prefix + current.split(" ")[1]
        )

        return request
