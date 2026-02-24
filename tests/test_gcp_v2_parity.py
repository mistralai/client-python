"""
Parity tests for the GCP v2 SDK.

Verifies that the regenerated mistralai.gcp package exposes
the same public API surface as the v1 mistralai_gcp package.
Uses introspection only — no API calls or credentials required.
"""
import inspect

import pytest

from mistralai.gcp.client import MistralGCP
from mistralai.gcp.client.chat import Chat
from mistralai.gcp.client.fim import Fim
from mistralai.gcp.client.types import UNSET

GCP_METHODS: dict[str, set[str]] = {
    "chat": {"complete", "stream"},
    "fim": {"complete", "stream"},
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
    ("project_id", None),
    ("region", "europe-west4"),
    ("access_token", None),
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
    ("model", _EMPTY),
    ("messages", _EMPTY),
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
    ("retries", UNSET),
    ("server_url", None),
    ("timeout_ms", None),
    ("http_headers", None),
]

CHAT_STREAM_PARAMS = [
    (name, True if name == "stream" else default)
    for name, default in CHAT_COMPLETE_PARAMS
]

FIM_COMPLETE_PARAMS = [
    ("model", _EMPTY),
    ("prompt", _EMPTY),
    ("temperature", UNSET),
    ("top_p", 1),
    ("max_tokens", UNSET),
    ("stream", False),
    ("stop", None),
    ("random_seed", UNSET),
    ("metadata", UNSET),
    ("suffix", UNSET),
    ("min_tokens", UNSET),
    ("retries", UNSET),
    ("server_url", None),
    ("timeout_ms", None),
    ("http_headers", None),
]

FIM_STREAM_PARAMS = [
    (name, True if name == "stream" else default)
    for name, default in FIM_COMPLETE_PARAMS
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestGCPSDKStructure:
    def test_sdk_has_chat(self):
        assert "chat" in MistralGCP.__annotations__

    def test_sdk_has_fim(self):
        assert "fim" in MistralGCP.__annotations__

    @pytest.mark.parametrize("param_name,expected_default", CONSTRUCTOR_PARAMS)
    def test_constructor_param(self, param_name, expected_default):
        sig = inspect.signature(MistralGCP.__init__)
        assert param_name in sig.parameters, f"Missing constructor param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Constructor param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    @pytest.mark.parametrize("method", ["__enter__", "__exit__", "__aenter__", "__aexit__"])
    def test_context_manager_support(self, method):
        assert hasattr(MistralGCP, method), f"MistralGCP missing {method}"


class TestGCPChat:
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
    def test_complete_model_required(self):
        sig = inspect.signature(Chat.complete)
        assert sig.parameters["model"].default is _EMPTY

    def test_stream_model_required(self):
        sig = inspect.signature(Chat.stream)
        assert sig.parameters["model"].default is _EMPTY

    def test_complete_stream_defaults_false(self):
        sig = inspect.signature(Chat.complete)
        assert sig.parameters["stream"].default is False

    def test_stream_stream_defaults_true(self):
        sig = inspect.signature(Chat.stream)
        assert sig.parameters["stream"].default is True


class TestGCPFim:
    def test_has_complete(self):
        assert hasattr(Fim, "complete")
        mark_tested("fim", "complete")

    def test_has_complete_async(self):
        assert hasattr(Fim, "complete_async")
        mark_tested("fim", "complete_async")

    def test_has_stream(self):
        assert hasattr(Fim, "stream")
        mark_tested("fim", "stream")

    def test_has_stream_async(self):
        assert hasattr(Fim, "stream_async")
        mark_tested("fim", "stream_async")

    # -- complete params --
    @pytest.mark.parametrize("param_name,expected_default", FIM_COMPLETE_PARAMS)
    def test_complete_has_param(self, param_name, expected_default):
        sig = inspect.signature(Fim.complete)
        assert param_name in sig.parameters, f"Fim.complete missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Fim.complete param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- stream params --
    @pytest.mark.parametrize("param_name,expected_default", FIM_STREAM_PARAMS)
    def test_stream_has_param(self, param_name, expected_default):
        sig = inspect.signature(Fim.stream)
        assert param_name in sig.parameters, f"Fim.stream missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Fim.stream param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- complete_async matches complete --
    @pytest.mark.parametrize("param_name,expected_default", FIM_COMPLETE_PARAMS)
    def test_complete_async_has_param(self, param_name, expected_default):
        sig = inspect.signature(Fim.complete_async)
        assert param_name in sig.parameters, f"Fim.complete_async missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Fim.complete_async param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- stream_async matches stream --
    @pytest.mark.parametrize("param_name,expected_default", FIM_STREAM_PARAMS)
    def test_stream_async_has_param(self, param_name, expected_default):
        sig = inspect.signature(Fim.stream_async)
        assert param_name in sig.parameters, f"Fim.stream_async missing param: {param_name}"
        actual = sig.parameters[param_name].default
        assert actual == expected_default, (
            f"Fim.stream_async param {param_name}: expected {expected_default!r}, got {actual!r}"
        )

    # -- sync/async parity --
    def test_complete_async_matches_complete(self):
        sync_params = set(inspect.signature(Fim.complete).parameters) - {"self"}
        async_params = set(inspect.signature(Fim.complete_async).parameters) - {"self"}
        assert sync_params == async_params

    def test_stream_async_matches_stream(self):
        sync_params = set(inspect.signature(Fim.stream).parameters) - {"self"}
        async_params = set(inspect.signature(Fim.stream_async).parameters) - {"self"}
        assert sync_params == async_params

    # -- key defaults --
    def test_complete_model_required(self):
        sig = inspect.signature(Fim.complete)
        assert sig.parameters["model"].default is _EMPTY

    def test_stream_model_required(self):
        sig = inspect.signature(Fim.stream)
        assert sig.parameters["model"].default is _EMPTY

    def test_complete_stream_defaults_false(self):
        sig = inspect.signature(Fim.complete)
        assert sig.parameters["stream"].default is False

    def test_stream_stream_defaults_true(self):
        sig = inspect.signature(Fim.stream)
        assert sig.parameters["stream"].default is True

    def test_complete_top_p_defaults_to_1(self):
        sig = inspect.signature(Fim.complete)
        assert sig.parameters["top_p"].default == 1

    def test_stream_top_p_defaults_to_1(self):
        sig = inspect.signature(Fim.stream)
        assert sig.parameters["top_p"].default == 1


class TestGCPCoverage:
    def test_all_methods_tested(self):
        expected = set()
        for resource, methods in GCP_METHODS.items():
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

    def test_no_unexpected_public_methods_on_fim(self):
        public = {m for m in dir(Fim) if not m.startswith("_") and callable(getattr(Fim, m, None))}
        known = {"complete", "complete_async", "stream", "stream_async", "do_request", "do_request_async"}
        unexpected = public - known
        assert not unexpected, f"Unexpected Fim methods: {unexpected}"
