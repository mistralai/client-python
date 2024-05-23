from unittest import mock

import pytest
from mistralai.async_client import MistralAsyncClient
from mistralai.client import MistralClient


@pytest.fixture()
def client():
    client = MistralClient(api_key="test_api_key")
    client._client = mock.MagicMock()
    return client


@pytest.fixture()
def async_client():
    client = MistralAsyncClient(api_key="test_api_key")
    client._client = mock.AsyncMock()
    return client
