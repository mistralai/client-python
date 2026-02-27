"""Tests for the GCPVertexAIPathHook (request URL rewriting for Vertex AI)."""

import json

import httpx
import pytest

from mistralai.gcp.client._hooks.registration import GCPVertexAIPathHook
from mistralai.client._hooks.types import BeforeRequestContext, HookContext
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils.logger import get_default_logger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_hook(project_id: str = "my-project", region: str = "us-central1"):
    return GCPVertexAIPathHook(project_id=project_id, region=region)


def _make_config():
    return SDKConfiguration(
        client=None,
        client_supplied=False,
        async_client=None,
        async_client_supplied=False,
        debug_logger=get_default_logger(),
    )


def _make_ctx(operation_id: str = "chat_completion"):
    config = _make_config()
    hook_ctx = HookContext(
        config=config,
        base_url="https://test.api",
        operation_id=operation_id,
        oauth2_scopes=None,
        security_source=None,
    )
    return BeforeRequestContext(hook_ctx)


def _make_request(body: dict | None = None, url: str = "https://us-central1-aiplatform.googleapis.com/v1/chat/completions"):
    content = json.dumps(body).encode() if body else b""
    return httpx.Request("POST", url, content=content)


# -------------------------------------------------------------------------
# 1. Non-streaming uses rawPredict
# -------------------------------------------------------------------------


class TestNonStreamingUsesRawPredict:
    def test_non_streaming_uses_raw_predict(self):
        hook = _make_hook()
        ctx = _make_ctx(operation_id="chat_completion")
        body = {"model": "mistral-large-latest", "messages": [{"role": "user", "content": "Hi"}]}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        assert ":rawPredict" in str(result.url.path)
        assert ":streamRawPredict" not in str(result.url.path)


# -------------------------------------------------------------------------
# 2. Streaming uses streamRawPredict
# -------------------------------------------------------------------------


class TestStreamingUsesStreamRawPredict:
    def test_streaming_uses_stream_raw_predict(self):
        hook = _make_hook()
        ctx = _make_ctx(operation_id="chat_completion_stream")
        body = {"model": "mistral-large-latest", "messages": [{"role": "user", "content": "Hi"}]}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        assert ":streamRawPredict" in str(result.url.path)


# -------------------------------------------------------------------------
# 3. No model in body -- request unchanged
# -------------------------------------------------------------------------


class TestNoModelInBodyUnchanged:
    def test_no_model_in_body_unchanged(self):
        hook = _make_hook()
        ctx = _make_ctx()
        body = {"messages": [{"role": "user", "content": "Hi"}]}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        # Should return the original request unchanged
        assert result is request


# -------------------------------------------------------------------------
# 4. Non-JSON body -- request unchanged
# -------------------------------------------------------------------------


class TestNonJsonBodyUnchanged:
    def test_non_json_body_unchanged(self):
        hook = _make_hook()
        ctx = _make_ctx()
        request = httpx.Request("POST", "https://test.api/v1/chat", content=b"\x00\x01\x02binary")

        result = hook.before_request(ctx, request)

        assert result is request


# -------------------------------------------------------------------------
# 5. Empty content -- request unchanged
# -------------------------------------------------------------------------


class TestEmptyContentUnchanged:
    def test_empty_content_unchanged(self):
        hook = _make_hook()
        ctx = _make_ctx()
        request = httpx.Request("POST", "https://test.api/v1/chat", content=b"")

        result = hook.before_request(ctx, request)

        assert result is request


# -------------------------------------------------------------------------
# 6. Region in path
# -------------------------------------------------------------------------


class TestRegionInPath:
    def test_region_in_path(self):
        hook = _make_hook(region="europe-west4")
        ctx = _make_ctx()
        body = {"model": "mistral-large-latest", "messages": []}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        assert "europe-west4" in result.url.path


# -------------------------------------------------------------------------
# 7. Project ID in path
# -------------------------------------------------------------------------


class TestProjectIdInPath:
    def test_project_id_in_path(self):
        hook = _make_hook(project_id="my-custom-project")
        ctx = _make_ctx()
        body = {"model": "mistral-large-latest", "messages": []}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        assert "my-custom-project" in result.url.path


# -------------------------------------------------------------------------
# 8. Model in path
# -------------------------------------------------------------------------


class TestModelInPath:
    def test_model_in_path(self):
        hook = _make_hook()
        ctx = _make_ctx()
        body = {"model": "mistral-large-latest", "messages": []}
        request = _make_request(body)

        result = hook.before_request(ctx, request)

        assert "mistral-large-latest" in result.url.path
        # Verify the full expected path structure
        expected_path = "/v1/projects/my-project/locations/us-central1/publishers/mistralai/models/mistral-large-latest:rawPredict"
        assert result.url.path == expected_path
