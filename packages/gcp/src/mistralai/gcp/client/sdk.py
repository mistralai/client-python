from .basesdk import BaseSDK
from .httpclient import AsyncHttpClient, ClientOwner, HttpClient, close_clients
from .sdkconfiguration import SDKConfiguration
from .utils.logger import Logger, get_default_logger
from .utils.retries import RetryConfig
import google.auth
import google.auth.credentials
import google.auth.transport.requests
import httpx
import importlib
from mistralai.gcp.client import models, utils
from mistralai.gcp.client._hooks import SDKHooks
from mistralai.gcp.client._hooks.registration import GCPVertexAIPathHook
from mistralai.gcp.client.types import OptionalNullable, UNSET
import sys
from typing import Callable, Dict, Optional, TYPE_CHECKING, cast
import weakref

if TYPE_CHECKING:
    from mistralai.gcp.client.chat import Chat
    from mistralai.gcp.client.fim import Fim


class MistralGCP(BaseSDK):
    r"""Mistral AI API: Dora OpenAPI schema

    Our Chat Completion and Embeddings APIs specification. Create your account on [La Plateforme](https://console.mistral.ai) to get access and read the [docs](https://docs.mistral.ai) to learn how to use it.
    """

    chat: "Chat"
    r"""Chat Completion API."""
    fim: "Fim"
    r"""Fill-in-the-middle API."""
    _sub_sdk_map = {
        "chat": ("mistralai.gcp.client.chat", "Chat"),
        "fim": ("mistralai.gcp.client.fim", "Fim"),
    }

    def __init__(
        self,
        project_id: Optional[str] = None,
        region: str = "europe-west4",
        access_token: Optional[str] = None,
        server: Optional[str] = None,
        server_url: Optional[str] = None,
        url_params: Optional[Dict[str, str]] = None,
        client: Optional[HttpClient] = None,
        async_client: Optional[AsyncHttpClient] = None,
        retry_config: OptionalNullable[RetryConfig] = UNSET,
        timeout_ms: Optional[int] = None,
        debug_logger: Optional[Logger] = None,
    ) -> None:
        r"""Instantiates the SDK configuring it with the provided parameters.

        :param project_id: GCP project ID (auto-detected from credentials if not provided)
        :param region: GCP region for Vertex AI (default: europe-west4)
        :param access_token: Fixed access token for testing (skips google.auth)
        :param server: The server by name to use for all methods
        :param server_url: The server URL to use for all methods
        :param url_params: Parameters to optionally template the server URL with
        :param client: The HTTP client to use for all synchronous methods
        :param async_client: The Async HTTP client to use for all asynchronous methods
        :param retry_config: The retry configuration to use for all supported methods
        :param timeout_ms: Optional request timeout applied to each operation in milliseconds
        """
        credentials: Optional[google.auth.credentials.Credentials] = None
        if access_token is None:
            creds, detected_project_id = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            if creds is None:
                raise ValueError("Failed to obtain GCP credentials")
            # Cast to Credentials base class which has refresh() and token
            creds = cast(google.auth.credentials.Credentials, creds)
            creds.refresh(google.auth.transport.requests.Request())
            credentials = creds
            project_id = project_id or detected_project_id

        if project_id is None:
            raise ValueError(
                "project_id must be provided or available from default credentials"
            )

        self._credentials = credentials
        self._project_id = project_id
        self._region = region
        self._fixed_access_token = access_token

        def get_auth_token() -> str:
            if self._fixed_access_token:
                return self._fixed_access_token
            creds = self._credentials
            if creds is None:
                raise ValueError("No credentials available")
            # Only refresh when the token is expired or missing.
            # This avoids a blocking HTTP round-trip on every request and
            # minimises event-loop blocking when called from async paths
            # (the Speakeasy-generated basesdk always calls security
            # callables synchronously).
            if not creds.valid:
                creds.refresh(google.auth.transport.requests.Request())
            token = creds.token
            if token is None:
                raise ValueError("Failed to obtain access token")
            return token

        if server_url is None:
            server_url = f"https://{region}-aiplatform.googleapis.com"

        client_supplied = True
        if client is None:
            client = httpx.Client(follow_redirects=True)
            client_supplied = False

        assert issubclass(
            type(client), HttpClient
        ), "The provided client must implement the HttpClient protocol."

        async_client_supplied = True
        if async_client is None:
            async_client = httpx.AsyncClient(follow_redirects=True)
            async_client_supplied = False

        if debug_logger is None:
            debug_logger = get_default_logger()

        assert issubclass(
            type(async_client), AsyncHttpClient
        ), "The provided async_client must implement the AsyncHttpClient protocol."

        def get_security() -> models.Security:
            return models.Security(api_key=get_auth_token())

        security: Callable[[], models.Security] = get_security

        if url_params is not None:
            server_url = utils.template_url(server_url, url_params)

        BaseSDK.__init__(
            self,
            SDKConfiguration(
                client=client,
                client_supplied=client_supplied,
                async_client=async_client,
                async_client_supplied=async_client_supplied,
                security=security,
                server_url=server_url,
                server=server,
                retry_config=retry_config,
                timeout_ms=timeout_ms,
                debug_logger=debug_logger,
            ),
            parent_ref=self,
        )

        hooks = SDKHooks()
        self.sdk_configuration.__dict__["_hooks"] = hooks

        # Register hook that builds Vertex AI URL path
        hooks.register_before_request_hook(GCPVertexAIPathHook(project_id, region))

        current_server_url, *_ = self.sdk_configuration.get_server_details()
        server_url, self.sdk_configuration.client = hooks.sdk_init(
            current_server_url, client
        )
        if current_server_url != server_url:
            self.sdk_configuration.server_url = server_url

        weakref.finalize(
            self,
            close_clients,
            cast(ClientOwner, self.sdk_configuration),
            self.sdk_configuration.client,
            self.sdk_configuration.client_supplied,
            self.sdk_configuration.async_client,
            self.sdk_configuration.async_client_supplied,
        )

    def dynamic_import(self, modname, retries=3):
        last_exc: Optional[Exception] = None
        for attempt in range(retries):
            try:
                return importlib.import_module(modname)
            except (KeyError, ImportError, ModuleNotFoundError) as e:
                last_exc = e
                # Clear any half-initialized module and retry
                sys.modules.pop(modname, None)
                if attempt == retries - 1:
                    break
        raise ImportError(
            f"Failed to import module '{modname}' after {retries} attempts"
        ) from last_exc

    def __getattr__(self, name: str):
        if name in self._sub_sdk_map:
            module_path, class_name = self._sub_sdk_map[name]
            try:
                module = self.dynamic_import(module_path)
                klass = getattr(module, class_name)
                instance = klass(self.sdk_configuration, parent_ref=self)
                setattr(self, name, instance)
                return instance
            except ImportError as e:
                raise AttributeError(
                    f"Failed to import module {module_path} for attribute {name}: {e}"
                ) from e
            except AttributeError as e:
                raise AttributeError(
                    f"Failed to find class {class_name} in module {module_path} for attribute {name}: {e}"
                ) from e

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __dir__(self):
        default_attrs = list(super().__dir__())
        lazy_attrs = list(self._sub_sdk_map.keys())
        return sorted(list(set(default_attrs + lazy_attrs)))

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        if (
            self.sdk_configuration.client is not None
            and not self.sdk_configuration.client_supplied
        ):
            self.sdk_configuration.client.close()
        self.sdk_configuration.client = None

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        if (
            self.sdk_configuration.async_client is not None
            and not self.sdk_configuration.async_client_supplied
        ):
            await self.sdk_configuration.async_client.aclose()
        self.sdk_configuration.async_client = None
