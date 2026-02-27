"""Tests for MistralGCP constructor with mocked google.auth."""

import pytest

from mistralai.gcp.client.sdk import MistralGCP


# -------------------------------------------------------------------------
# 1. Constructor with access_token bypasses google.auth
# -------------------------------------------------------------------------


class TestConstructorWithAccessToken:
    def test_constructor_with_access_token(self):
        client = MistralGCP(
            project_id="my-project",
            region="us-central1",
            access_token="test-token",
        )

        assert client._project_id == "my-project"
        assert client._region == "us-central1"
        assert client._fixed_access_token == "test-token"
        # Credentials should be None when access_token is used
        assert client._credentials is None


# -------------------------------------------------------------------------
# 2. Default server URL
# -------------------------------------------------------------------------


class TestDefaultServerUrl:
    def test_default_server_url(self):
        client = MistralGCP(
            project_id="my-project",
            region="europe-west4",
            access_token="test-token",
        )

        url, _ = client.sdk_configuration.get_server_details()
        assert url == "https://europe-west4-aiplatform.googleapis.com"


# -------------------------------------------------------------------------
# 3. Custom region changes server URL
# -------------------------------------------------------------------------


class TestCustomRegion:
    def test_custom_region(self):
        client = MistralGCP(
            project_id="my-project",
            region="us-east1",
            access_token="test-token",
        )

        url, _ = client.sdk_configuration.get_server_details()
        assert url == "https://us-east1-aiplatform.googleapis.com"


# -------------------------------------------------------------------------
# 4. ValueError if no project_id and no default creds
# -------------------------------------------------------------------------


class TestProjectIdRequired:
    def test_project_id_required(self):
        # Without project_id and without google.auth providing one,
        # we should get a ValueError. Since access_token bypasses google.auth,
        # not providing project_id should raise.
        with pytest.raises(ValueError, match="project_id must be provided"):
            MistralGCP(
                project_id=None,
                region="us-central1",
                access_token="test-token",
            )


# -------------------------------------------------------------------------
# 5. Context manager works
# -------------------------------------------------------------------------


class TestContextManager:
    def test_context_manager(self):
        with MistralGCP(
            project_id="my-project",
            region="us-central1",
            access_token="test-token",
        ) as m:
            assert isinstance(m, MistralGCP)
            assert m.sdk_configuration.client is not None


# -------------------------------------------------------------------------
# 6. dir() includes sub SDKs
# -------------------------------------------------------------------------


class TestDirIncludesSubSdks:
    def test_dir_includes_sub_sdks(self):
        client = MistralGCP(
            project_id="my-project",
            region="us-central1",
            access_token="test-token",
        )

        d = dir(client)
        assert "chat" in d
        assert "fim" in d


# -------------------------------------------------------------------------
# 7. Chat request via respx exercises path hook rewriting
# -------------------------------------------------------------------------


class TestChatRequestViaRespx:
    def test_chat_request_rewrites_path(self):
        """GCP path hook rewrites /v1/chat/completions to rawPredict."""
        import respx
        import httpx

        client = MistralGCP(
            project_id="my-project",
            region="us-central1",
            access_token="test-token",
        )

        chat_response = {
            "id": "test-001",
            "object": "chat.completion",
            "model": "mistral-small-latest",
            "created": 1700000000,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello."},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "total_tokens": 15,
            },
        }

        with respx.mock(
            base_url="https://us-central1-aiplatform.googleapis.com"
        ) as router:
            # The GCP hook rewrites to rawPredict path
            router.post(url__regex=r".*rawPredict.*").mock(
                return_value=httpx.Response(200, json=chat_response)
            )
            result = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": "Hi"}],
            )

        assert result is not None
        assert result.id == "test-001"
