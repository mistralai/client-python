"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from .httpclient import AsyncHttpClient, HttpClient
from .sdkconfiguration import SDKConfiguration
from .utils.logger import Logger, NoOpLogger
from .utils.retries import RetryConfig
import httpx
from mistralai import models, utils
from mistralai._hooks import SDKHooks
from mistralai.agents import Agents
from mistralai.chat import Chat
from mistralai.embeddings import Embeddings
from mistralai.files import Files
from mistralai.fim import Fim
from mistralai.fine_tuning import FineTuning
from mistralai.models_ import Models
from mistralai.types import OptionalNullable, UNSET
from typing import Any, Callable, Dict, Optional, Union

class Mistral(BaseSDK):
    r"""Mistral AI API: Our Chat Completion and Embeddings APIs specification. Create your account on [La Plateforme](https://console.mistral.ai) to get access and read the [docs](https://docs.mistral.ai) to learn how to use it."""
    models: Models
    r"""Model Management API"""
    files: Files
    r"""Files API"""
    fine_tuning: FineTuning
    chat: Chat
    r"""Chat Completion API."""
    fim: Fim
    r"""Fill-in-the-middle API."""
    agents: Agents
    r"""Agents API."""
    embeddings: Embeddings
    r"""Embeddings API."""
    def __init__(
        self,
        api_key: Optional[Union[Optional[str], Callable[[], Optional[str]]]] = None,
        server: Optional[str] = None,
        server_url: Optional[str] = None,
        url_params: Optional[Dict[str, str]] = None,
        client: Optional[HttpClient] = None,
        async_client: Optional[AsyncHttpClient] = None,
        retry_config: OptionalNullable[RetryConfig] = UNSET,
        timeout_ms: Optional[int] = None,
        debug_logger: Optional[Logger] = None
    ) -> None:
        r"""Instantiates the SDK configuring it with the provided parameters.

        :param api_key: The api_key required for authentication
        :param server: The server by name to use for all methods
        :param server_url: The server URL to use for all methods
        :param url_params: Parameters to optionally template the server URL with
        :param client: The HTTP client to use for all synchronous methods
        :param async_client: The Async HTTP client to use for all asynchronous methods
        :param retry_config: The retry configuration to use for all supported methods
        :param timeout_ms: Optional request timeout applied to each operation in milliseconds
        """
        if client is None:
            client = httpx.Client()

        assert issubclass(
            type(client), HttpClient
        ), "The provided client must implement the HttpClient protocol."

        if async_client is None:
            async_client = httpx.AsyncClient()

        if debug_logger is None:
            debug_logger = NoOpLogger()

        assert issubclass(
            type(async_client), AsyncHttpClient
        ), "The provided async_client must implement the AsyncHttpClient protocol."
        
        security: Any = None
        if callable(api_key):
            security = lambda: models.Security(api_key = api_key()) # pylint: disable=unnecessary-lambda-assignment
        else:
            security = models.Security(api_key = api_key)

        if server_url is not None:
            if url_params is not None:
                server_url = utils.template_url(server_url, url_params)
    

        BaseSDK.__init__(self, SDKConfiguration(
            client=client,
            async_client=async_client,
            security=security,
            server_url=server_url,
            server=server,
            retry_config=retry_config,
            timeout_ms=timeout_ms,
            debug_logger=debug_logger
        ))

        hooks = SDKHooks()

        current_server_url, *_ = self.sdk_configuration.get_server_details()
        server_url, self.sdk_configuration.client = hooks.sdk_init(current_server_url, self.sdk_configuration.client)
        if current_server_url != server_url:
            self.sdk_configuration.server_url = server_url

        # pylint: disable=protected-access
        self.sdk_configuration.__dict__["_hooks"] = hooks

        self._init_sdks()


    def _init_sdks(self):
        self.models = Models(self.sdk_configuration)
        self.files = Files(self.sdk_configuration)
        self.fine_tuning = FineTuning(self.sdk_configuration)
        self.chat = Chat(self.sdk_configuration)
        self.fim = Fim(self.sdk_configuration)
        self.agents = Agents(self.sdk_configuration)
        self.embeddings = Embeddings(self.sdk_configuration)
    