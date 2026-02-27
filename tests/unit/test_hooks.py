"""Tests for SDKHooks registration and execution."""

from typing import Optional, Tuple, Union
from unittest.mock import MagicMock

import httpx
import pytest

from mistralai.client._hooks.sdkhooks import SDKHooks
from mistralai.client._hooks.types import (
    AfterErrorContext,
    AfterErrorHook,
    AfterSuccessContext,
    AfterSuccessHook,
    BeforeRequestContext,
    BeforeRequestHook,
    HookContext,
    SDKInitHook,
)
from mistralai.client.httpclient import HttpClient
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils.logger import get_default_logger


# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------


def _make_hook_ctx(
    base_url: str = "https://test.api",
    operation_id: str = "test_op",
) -> HookContext:
    config = SDKConfiguration(
        client=None,
        client_supplied=False,
        async_client=None,
        async_client_supplied=False,
        debug_logger=get_default_logger(),
    )
    return HookContext(
        config=config,
        base_url=base_url,
        operation_id=operation_id,
        oauth2_scopes=None,
        security_source=None,
    )


def _make_before_ctx(**kwargs) -> BeforeRequestContext:
    return BeforeRequestContext(_make_hook_ctx(**kwargs))


def _make_after_success_ctx(**kwargs) -> AfterSuccessContext:
    return AfterSuccessContext(_make_hook_ctx(**kwargs))


def _make_after_error_ctx(**kwargs) -> AfterErrorContext:
    return AfterErrorContext(_make_hook_ctx(**kwargs))


def _make_request(
    url: str = "https://test.api/v1/chat/completions",
    method: str = "POST",
) -> httpx.Request:
    return httpx.Request(
        method,
        url,
        headers={"user-agent": "python-httpx/0.27.0 speakeasy-sdk/1.0"},
    )


def _make_response(status_code: int = 200) -> httpx.Response:
    return httpx.Response(status_code, request=_make_request())


# -------------------------------------------------------------------------
# 1. Before request hooks execute in order
# -------------------------------------------------------------------------


class TestBeforeRequestHooksExecuteInOrder:
    def test_before_request_hooks_execute_in_order(self):
        call_order = []

        class HookA(BeforeRequestHook):
            def before_request(
                self, hook_ctx: BeforeRequestContext, request: httpx.Request
            ) -> Union[httpx.Request, Exception]:
                call_order.append("A")
                return request

        class HookB(BeforeRequestHook):
            def before_request(
                self, hook_ctx: BeforeRequestContext, request: httpx.Request
            ) -> Union[httpx.Request, Exception]:
                call_order.append("B")
                return request

        hooks = SDKHooks()
        hooks.register_before_request_hook(HookA())
        hooks.register_before_request_hook(HookB())

        ctx = _make_before_ctx()
        request = _make_request()
        hooks.before_request(ctx, request)

        # Default hooks (CustomUserAgentHook, TracingHook) run first,
        # then our custom hooks A and B
        assert call_order == ["A", "B"]


# -------------------------------------------------------------------------
# 2. Before request hook modifies request
# -------------------------------------------------------------------------


class TestBeforeRequestHookModifiesRequest:
    def test_before_request_hook_modifies_request(self):
        class AddHeaderHook(BeforeRequestHook):
            def before_request(
                self, hook_ctx: BeforeRequestContext, request: httpx.Request
            ) -> Union[httpx.Request, Exception]:
                # Create a new request with an extra header
                headers = dict(request.headers)
                headers["X-Custom"] = "test-value"
                return httpx.Request(
                    request.method,
                    request.url,
                    headers=headers,
                )

        hooks = SDKHooks()
        hooks.register_before_request_hook(AddHeaderHook())

        ctx = _make_before_ctx()
        request = _make_request()
        result = hooks.before_request(ctx, request)

        assert result.headers.get("X-Custom") == "test-value"


# -------------------------------------------------------------------------
# 3. Before request hook raises on exception
# -------------------------------------------------------------------------


class TestBeforeRequestHookRaisesOnException:
    def test_before_request_hook_raises_on_exception(self):
        class FailHook(BeforeRequestHook):
            def before_request(
                self, hook_ctx: BeforeRequestContext, request: httpx.Request
            ) -> Union[httpx.Request, Exception]:
                return ValueError("hook failed")

        hooks = SDKHooks()
        hooks.register_before_request_hook(FailHook())

        ctx = _make_before_ctx()
        request = _make_request()
        with pytest.raises(ValueError, match="hook failed"):
            hooks.before_request(ctx, request)


# -------------------------------------------------------------------------
# 4. After success hook modifies response
# -------------------------------------------------------------------------


class TestAfterSuccessHookModifiesResponse:
    def test_after_success_hook_modifies_response(self):
        class ModifyResponseHook(AfterSuccessHook):
            def after_success(
                self, hook_ctx: AfterSuccessContext, response: httpx.Response
            ) -> Union[httpx.Response, Exception]:
                # Return a new response with a different status code
                new_response = httpx.Response(
                    201,
                    request=response.request,
                    content=b"modified",
                )
                return new_response

        hooks = SDKHooks()
        hooks.register_after_success_hook(ModifyResponseHook())

        ctx = _make_after_success_ctx()
        response = _make_response(200)
        result = hooks.after_success(ctx, response)

        assert result.status_code == 201


# -------------------------------------------------------------------------
# 5. After success hook raises on exception
# -------------------------------------------------------------------------


class TestAfterSuccessHookRaisesOnException:
    def test_after_success_hook_raises_on_exception(self):
        class FailSuccessHook(AfterSuccessHook):
            def after_success(
                self, hook_ctx: AfterSuccessContext, response: httpx.Response
            ) -> Union[httpx.Response, Exception]:
                return RuntimeError("success hook failed")

        hooks = SDKHooks()
        hooks.register_after_success_hook(FailSuccessHook())

        ctx = _make_after_success_ctx()
        response = _make_response(200)
        with pytest.raises(RuntimeError, match="success hook failed"):
            hooks.after_success(ctx, response)


# -------------------------------------------------------------------------
# 6. After error hook receives error
# -------------------------------------------------------------------------


class TestAfterErrorHookReceivesError:
    def test_after_error_hook_receives_error(self):
        received_response = None
        received_error = None

        class CaptureErrorHook(AfterErrorHook):
            def after_error(
                self,
                hook_ctx: AfterErrorContext,
                response: Optional[httpx.Response],
                error: Optional[Exception],
            ) -> Union[
                Tuple[Optional[httpx.Response], Optional[Exception]], Exception
            ]:
                nonlocal received_response, received_error
                received_response = response
                received_error = error
                return response, error

        hooks = SDKHooks()
        hooks.register_after_error_hook(CaptureErrorHook())

        ctx = _make_after_error_ctx()
        err_response = _make_response(500)
        err = ConnectionError("network failure")
        hooks.after_error(ctx, err_response, err)

        assert received_response is not None
        assert received_response.status_code == 500
        assert received_error is not None
        assert str(received_error) == "network failure"


# -------------------------------------------------------------------------
# 7. After error hook raises on exception
# -------------------------------------------------------------------------


class TestAfterErrorHookRaisesOnException:
    def test_after_error_hook_raises_on_exception(self):
        class FailErrorHook(AfterErrorHook):
            def after_error(
                self,
                hook_ctx: AfterErrorContext,
                response: Optional[httpx.Response],
                error: Optional[Exception],
            ) -> Union[
                Tuple[Optional[httpx.Response], Optional[Exception]], Exception
            ]:
                return TypeError("error hook failed")

        hooks = SDKHooks()
        hooks.register_after_error_hook(FailErrorHook())

        ctx = _make_after_error_ctx()
        with pytest.raises(TypeError, match="error hook failed"):
            hooks.after_error(ctx, None, ConnectionError("original"))


# -------------------------------------------------------------------------
# 8. SDK init hook modifies URL
# -------------------------------------------------------------------------


class TestSdkInitHookModifiesUrl:
    def test_sdk_init_hook_modifies_url(self):
        class ChangeUrlHook(SDKInitHook):
            def sdk_init(
                self, base_url: str, client: HttpClient
            ) -> Tuple[str, HttpClient]:
                return "https://custom.api", client

        hooks = SDKHooks()
        hooks.register_sdk_init_hook(ChangeUrlHook())

        mock_client = MagicMock(spec=HttpClient)
        new_url, new_client = hooks.sdk_init(
            "https://original.api", mock_client
        )

        assert new_url == "https://custom.api"
        assert new_client is mock_client
