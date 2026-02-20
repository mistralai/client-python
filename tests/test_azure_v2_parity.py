"""
Parity tests for the Azure v2 SDK.

Verifies that the regenerated mistralai.azure package exposes
the same public API surface as the v1 mistralai_azure package.
Uses introspection only — no API calls or credentials required.
"""
import inspect

import pytest

from mistralai.azure.client import MistralAzure
from mistralai.azure.client.chat import Chat
from mistralai.azure.client.ocr import Ocr
from mistralai.azure.client.types import UNSET

AZURE_METHODS: dict[str, set[str]] = {
    "chat": {"complete", "stream"},
    "ocr": {"process"},
}

TESTED_METHODS: set[str] = set()

_EMPTY = inspect.Parameter.empty


def mark_tested(resource: str, method: str) -> None:
    TESTED_METHODS.add(f"{resource}.{method}")


# ---------------------------------------------------------------------------
# Expected parameter specs: (name, expected_default)
# Use _EMPTY for required params, UNSET for OptionalNullable, None for Optional
# ---------------------------------------------------------------------------

CONSTRUCTOR_PARAMS = [
    ("api_key", _EMPTY),
    ("server", None),
    ("server_url", None),
    ("url_params", None),
    ("client", None),
    ("async_client", None),
    ("retry_config", UNSET),
    ("timeout_ms", None),
    ("debug_logger", None),
]

CHAT_COMPLETE_PARAMS = [
    ("messages", _EMPTY),
    ("model", "azureai"),
    ("temperature", UNSET),
    ("top_p", None),
    ("max_tokens", UNSET),
    ("stream", False),
    ("stop", None),
    ("random_seed", UNSET),
    ("metadata", UNSET),
    ("response_format", None),
    ("tools", UNSET),
    ("tool_choice", None),
    ("presence_penalty", None),
    ("frequency_penalty", None),
    ("n", UNSET),
    ("prediction", None),
    ("parallel_tool_calls", None),
    ("prompt_mode", UNSET),
    ("safe_prompt", None),
    ("retries", UNSET),
    ("server_url", None),
    ("timeout_ms", None),
    ("http_headers", None),
]

CHAT_STREAM_PARAMS = [
    (name, True if name == "stream" else default)
    for name, default in CHAT_COMPLETE_PARAMS
]

OCR_PROCESS_PARAMS = [
    ("model", _EMPTY),
    ("document", _EMPTY),
    ("id", None),
    ("pages", UNSET),
    ("include_image_base64", UNSET),
    ("image_limit", UNSET),
    ("image_min_size", UNSET),
    ("bbox_annotation_format", UNSET),
    ("document_annotation_format", UNSET),
    ("document_annotation_prompt", UNSET),
    ("table_format", UNSET),
    ("extract_header", None),
    ("extract_footer", None),
    ("retries", UNSET),
    ("server_url", None),
    ("timeout_ms", None),
    ("http_headers", None),
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAzureSDKStructure:
    def test_sdk_has_chat(self):
        assert "chat" in MistralAzure.__annotations__

    def test_sdk_has_ocr(self):
        assert "ocr" in MistralAzure.__annotations__

    @pytest.mark.parametrize("param_name,expected_default", CONSTRUCTOR_PARAMS)
    def test_constructor_param(self, param_name, expected_default):
        sig = inspect.signature(MistralAzure.__init__)
        assert param_name in sig.parameters, f"Missing constructor param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Constructor param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    @pytest.mark.parametrize("method", ["__enter__", "__exit__", "__aenter__", "__aexit__"])
    def test_context_manager_support(self, method):
        assert hasattr(MistralAzure, method), f"MistralAzure missing {method}"


class TestAzureChat:
    def test_has_complete(self):
        assert hasattr(Chat, "complete")
        mark_tested("chat", "complete")

    def test_has_complete_async(self):
        assert hasattr(Chat, "complete_async")
        mark_tested("chat", "complete_async")

    def test_has_stream(self):
        assert hasattr(Chat, "stream")
        mark_tested("chat", "stream")

    def test_has_stream_async(self):
        assert hasattr(Chat, "stream_async")
        mark_tested("chat", "stream_async")

    # -- complete params --
    @pytest.mark.parametrize("param_name,expected_default", CHAT_COMPLETE_PARAMS)
    def test_complete_has_param(self, param_name, expected_default):
        sig = inspect.signature(Chat.complete)
        assert param_name in sig.parameters, f"Chat.complete missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Chat.complete param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- stream params --
    @pytest.mark.parametrize("param_name,expected_default", CHAT_STREAM_PARAMS)
    def test_stream_has_param(self, param_name, expected_default):
        sig = inspect.signature(Chat.stream)
        assert param_name in sig.parameters, f"Chat.stream missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Chat.stream param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- complete_async matches complete --
    @pytest.mark.parametrize("param_name,expected_default", CHAT_COMPLETE_PARAMS)
    def test_complete_async_has_param(self, param_name, expected_default):
        sig = inspect.signature(Chat.complete_async)
        assert param_name in sig.parameters, f"Chat.complete_async missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Chat.complete_async param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- stream_async matches stream --
    @pytest.mark.parametrize("param_name,expected_default", CHAT_STREAM_PARAMS)
    def test_stream_async_has_param(self, param_name, expected_default):
        sig = inspect.signature(Chat.stream_async)
        assert param_name in sig.parameters, f"Chat.stream_async missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Chat.stream_async param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- sync/async parity --
    def test_complete_async_matches_complete(self):
        sync_params = set(inspect.signature(Chat.complete).parameters) - {"self"}
        async_params = set(inspect.signature(Chat.complete_async).parameters) - {"self"}
        assert sync_params == async_params

    def test_stream_async_matches_stream(self):
        sync_params = set(inspect.signature(Chat.stream).parameters) - {"self"}
        async_params = set(inspect.signature(Chat.stream_async).parameters) - {"self"}
        assert sync_params == async_params

    # -- key defaults --
    def test_complete_model_defaults_azureai(self):
        sig = inspect.signature(Chat.complete)
        assert sig.parameters["model"].default == "azureai"

    def test_stream_model_defaults_azureai(self):
        sig = inspect.signature(Chat.stream)
        assert sig.parameters["model"].default == "azureai"

    def test_complete_stream_defaults_false(self):
        sig = inspect.signature(Chat.complete)
        assert sig.parameters["stream"].default is False

    def test_stream_stream_defaults_true(self):
        sig = inspect.signature(Chat.stream)
        assert sig.parameters["stream"].default is True


class TestAzureOcr:
    def test_has_process(self):
        assert hasattr(Ocr, "process")
        mark_tested("ocr", "process")

    def test_has_process_async(self):
        assert hasattr(Ocr, "process_async")
        mark_tested("ocr", "process_async")

    # -- process params --
    @pytest.mark.parametrize("param_name,expected_default", OCR_PROCESS_PARAMS)
    def test_process_has_param(self, param_name, expected_default):
        sig = inspect.signature(Ocr.process)
        assert param_name in sig.parameters, f"Ocr.process missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Ocr.process param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- process_async matches process --
    @pytest.mark.parametrize("param_name,expected_default", OCR_PROCESS_PARAMS)
    def test_process_async_has_param(self, param_name, expected_default):
        sig = inspect.signature(Ocr.process_async)
        assert param_name in sig.parameters, f"Ocr.process_async missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Ocr.process_async param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- sync/async parity --
    def test_process_async_matches_process(self):
        sync_params = set(inspect.signature(Ocr.process).parameters) - {"self"}
        async_params = set(inspect.signature(Ocr.process_async).parameters) - {"self"}
        assert sync_params == async_params


class TestAzureCoverage:
    def test_all_methods_tested(self):
        expected = set()
        for resource, methods in AZURE_METHODS.items():
            for method in methods:
                expected.add(f"{resource}.{method}")
                expected.add(f"{resource}.{method}_async")
        untested = expected - TESTED_METHODS
        assert not untested, f"Untested methods: {untested}"

    def test_no_unexpected_public_methods_on_chat(self):
        public = {m for m in dir(Chat) if not m.startswith("_") and callable(getattr(Chat, m, None))}
        known = {"complete", "complete_async", "stream", "stream_async", "do_request", "do_request_async"}
        unexpected = public - known
        assert not unexpected, f"Unexpected Chat methods: {unexpected}"

    def test_no_unexpected_public_methods_on_ocr(self):
        public = {m for m in dir(Ocr) if not m.startswith("_") and callable(getattr(Ocr, m, None))}
        known = {"process", "process_async", "do_request", "do_request_async"}
        unexpected = public - known
        assert not unexpected, f"Unexpected Ocr methods: {unexpected}"
