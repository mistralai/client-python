from .types import BeforeRequestHook, BeforeRequestContext, Hooks
import httpx


# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


class GCPCustomMethodPathHook(BeforeRequestHook):
    """Rewrite Vertex AI custom method paths from /rawPredict to :rawPredict.

    Google Cloud APIs use colon-prefixed custom methods (e.g., :rawPredict)
    but OpenAPI 3.x requires paths to start with /. This hook fixes the URL
    at request time.
    """

    REWRITES = {
        "/rawPredict": ":rawPredict",
        "/streamRawPredict": ":streamRawPredict",
    }

    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> httpx.Request:
        path = request.url.path  # excludes query params and fragments
        for old, new in self.REWRITES.items():
            if path.endswith(old):
                url_str = str(request.url)
                idx = url_str.rfind(old)
                if idx != -1:
                    url_str = url_str[:idx] + new + url_str[idx + len(old):]
                    return httpx.Request(
                        method=request.method,
                        url=url_str,
                        headers=request.headers,
                        content=request.content,
                    )
        return request


def init_hooks(hooks: Hooks):
    hooks.register_before_request_hook(GCPCustomMethodPathHook())
