import contextlib
import os
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock, patch

import httpx2 as httpx
import pytest
import requests
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SpanExportResult

from mistralai.client._hooks import SDKHooks
from mistralai.client._hooks.service_account_auth import ServiceAccountTokenError
from mistralai.client._hooks.tracing import TracingHook
from mistralai.client.models import Security
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils.logger import get_default_logger
from mistralai.extra.observability import (
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    RedactingSpanExporter,
    RegexRedactionPolicy,
    configure_telemetry,
    get_telemetry_tracer,
    set_tracer_provider,
)
from mistralai.extra.observability.otel import MISTRAL_SDK_OTEL_TRACER_NAME
from mistralai.extra.observability.telemetry import (
    MISTRAL_OTLP_TRACES_ENDPOINT_ENV,
    MISTRAL_SDK_TELEMETRY_ENV,
    MISTRAL_TELEMETRY_ENDPOINT,
    TelemetryConfigurationError,
    _create_telemetry_tracer_provider,
    _service_account_session,
    configure_telemetry_for_hook,
)

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


class FakeClient:
    def __init__(self, sdk_configuration: SDKConfiguration):
        self.sdk_configuration = sdk_configuration


def _make_client(api_key: str | None = "test-key") -> "Mistral":
    sdk_configuration = SDKConfiguration(
        client=None,
        client_supplied=True,
        async_client=None,
        async_client_supplied=True,
        debug_logger=get_default_logger(),
        security=Security(api_key=api_key),
    )
    sdk_configuration.__dict__["_hooks"] = SDKHooks()
    return cast("Mistral", FakeClient(sdk_configuration))


def _get_tracing_hook(client: "Mistral") -> TracingHook:
    hooks = client.sdk_configuration.__dict__["_hooks"]
    tracing_hooks = [
        h for h in hooks.before_request_hooks if isinstance(h, TracingHook)
    ]
    assert len(tracing_hooks) == 1
    return tracing_hooks[0]


def _configure_for_hook(
    client: "Mistral",
    telemetry: bool | str | None = None,
) -> bool:
    """Helper to call configure_telemetry_for_hook via a client."""
    return configure_telemetry_for_hook(
        _get_tracing_hook(client),
        client.sdk_configuration,
        telemetry=telemetry,
    )


class FakeProvider:
    def __init__(self):
        self.shutdown_called = False
        self.get_tracer_calls: list[str] = []
        self.tracers: dict[str, MagicMock] = {}

    def get_tracer(self, name: str):
        self.get_tracer_calls.append(name)
        if name not in self.tracers:
            self.tracers[name] = MagicMock(name=f"tracer:{name}")
        return self.tracers[name]

    def shutdown(self):
        self.shutdown_called = True


class FakeExporter:
    instances: list["FakeExporter"] = []

    def __init__(self, *args: object, **kwargs: object):
        self.args = args
        self.kwargs = kwargs
        FakeExporter.instances.append(self)


class FakeResource:
    @classmethod
    def create(cls, attributes: dict[str, str]) -> dict[str, dict[str, str]]:
        return {"resource": attributes}


class FakeSpanProcessor:
    def __init__(self, exporter: FakeExporter):
        self.exporter = exporter


class FakeTracerProvider:
    def __init__(self, *, resource: object):
        self.resource = resource
        self.span_processors: list[FakeSpanProcessor] = []

    def add_span_processor(self, span_processor: FakeSpanProcessor):
        self.span_processors.append(span_processor)


class TestTelemetryConfiguration(unittest.TestCase):
    def setUp(self):
        FakeExporter.instances.clear()

    def test_env_defaults_to_disabled(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client)

        hook = _get_tracing_hook(client)
        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)
        self.assertTrue(hook._telemetry_auto_disabled)

    def test_env_dedicated_values_attach_provider(self):
        provider = FakeProvider()
        with patch.dict(
            os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "dedicated"}, clear=True
        ):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="test-key",
            server_url="",
            redaction=True,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_env_false_values_disable_telemetry(self):
        with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "false"}):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client)

        hook = _get_tracing_hook(client)
        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)
        self.assertTrue(hook._telemetry_auto_disabled)

    def test_standard_otel_endpoint_env_does_not_enable_telemetry(self):
        endpoint_env_values = {
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "http://collector:4318/v1/traces",
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318",
        }

        for env_name, env_value in endpoint_env_values.items():
            with self.subTest(env_name=env_name):
                with patch.dict(os.environ, {env_name: env_value}, clear=True):
                    with patch(
                        "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
                    ) as create_provider:
                        client = _make_client(api_key="test-key")
                        configured = _configure_for_hook(client)

                self.assertFalse(configured)
                create_provider.assert_not_called()
                self.assertIsNone(_get_tracing_hook(client).tracer_provider)

    def test_invalid_mistral_env_value_raises_configuration_error(self):
        for value in ("1", "true", "yes", "on", "0", "no", "off", "maybe"):
            with self.subTest(value=value):
                with patch.dict(
                    os.environ, {MISTRAL_SDK_TELEMETRY_ENV: value}, clear=True
                ):
                    with self.assertRaisesRegex(
                        TelemetryConfigurationError,
                        r"dedicated.*global",
                    ):
                        client = _make_client(api_key="test-key")
                        _configure_for_hook(client)

    def test_configure_telemetry_attaches_per_client_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = configure_telemetry(client)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="test-key",
            server_url="",
            redaction=True,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_configure_telemetry_accepts_explicit_dedicated_provider_mode(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = configure_telemetry(client, provider="dedicated")

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="test-key",
            server_url="",
            redaction=True,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_configure_telemetry_global_provider_mode_clears_auto_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client)

            configured = configure_telemetry(client, provider="global")

        hook = _get_tracing_hook(client)
        self.assertTrue(configured)
        self.assertTrue(provider.shutdown_called)
        self.assertIsNone(hook.tracer_provider)
        self.assertIsNone(hook._auto_telemetry_provider)
        self.assertTrue(hook._telemetry_auto_disabled)

    def test_configure_telemetry_custom_provider_replaces_auto_without_shutdown(self):
        auto_provider = FakeProvider()
        custom_provider = TracerProvider()

        with patch.object(custom_provider, "shutdown") as custom_shutdown:
            with patch.dict(os.environ, {}, clear=True):
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                    return_value=auto_provider,
                ):
                    client = _make_client(api_key="test-key")
                    configure_telemetry(client)

                configured = configure_telemetry(client, provider=custom_provider)

        hook = _get_tracing_hook(client)
        self.assertTrue(configured)
        self.assertTrue(auto_provider.shutdown_called)
        custom_shutdown.assert_not_called()
        self.assertIs(hook.tracer_provider, custom_provider)
        self.assertIsNone(hook._auto_telemetry_provider)

    def test_configure_telemetry_dedicated_replaces_custom_without_shutdown(self):
        custom_provider = TracerProvider()
        dedicated_provider = FakeProvider()
        client = _make_client(api_key="test-key")

        with patch.object(custom_provider, "shutdown") as custom_shutdown:
            configure_telemetry(client, provider=custom_provider)

            with patch.dict(os.environ, {}, clear=True):
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                    return_value=dedicated_provider,
                ):
                    configured = configure_telemetry(client, provider="dedicated")

        hook = _get_tracing_hook(client)
        self.assertTrue(configured)
        custom_shutdown.assert_not_called()
        self.assertIs(hook.tracer_provider, dedicated_provider)
        self.assertIs(hook._auto_telemetry_provider, dedicated_provider)

    def test_configure_telemetry_dedicated_reconfigure_applies_new_redaction(self):
        first_provider = FakeProvider()
        second_provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                side_effect=[first_provider, second_provider],
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configure_telemetry(client)
                configured = configure_telemetry(client, redaction=False)

        hook = _get_tracing_hook(client)
        self.assertTrue(configured)
        self.assertEqual(create_provider.call_count, 2)
        create_provider.assert_any_call(
            api_key="test-key", server_url="", redaction=False
        )
        self.assertTrue(first_provider.shutdown_called)
        self.assertIs(hook.tracer_provider, second_provider)
        self.assertIs(hook._auto_telemetry_provider, second_provider)

    def test_get_telemetry_tracer_dedicated_uses_auto_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client)
                tracer = get_telemetry_tracer(client)

        self.assertIs(tracer, provider.tracers[MISTRAL_SDK_OTEL_TRACER_NAME])
        self.assertEqual(provider.get_tracer_calls, [MISTRAL_SDK_OTEL_TRACER_NAME])

    def test_get_telemetry_tracer_custom_provider_uses_custom_name(self):
        provider = FakeProvider()
        client = _make_client(api_key="test-key")

        configure_telemetry(client, provider=cast(TracerProvider, provider))
        tracer = get_telemetry_tracer(client, "my-agent")

        self.assertIs(tracer, provider.tracers["my-agent"])
        self.assertEqual(provider.get_tracer_calls, ["my-agent"])

    def test_get_telemetry_tracer_global_uses_global_provider(self):
        client = _make_client(api_key="test-key")
        configure_telemetry(client, provider="global")
        tracer = MagicMock()

        with patch(
            "mistralai.extra.observability.telemetry.otel_trace.get_tracer",
            return_value=tracer,
        ) as get_tracer:
            result = get_telemetry_tracer(client, "my-agent")

        self.assertIs(result, tracer)
        get_tracer.assert_called_once_with("my-agent")

    def test_get_telemetry_tracer_disabled_raises_configuration_error(self):
        env_cases = ({}, {MISTRAL_SDK_TELEMETRY_ENV: "false"})

        for env in env_cases:
            with self.subTest(env=env):
                with patch.dict(os.environ, env, clear=True):
                    with patch(
                        "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
                    ) as create_provider:
                        client = _make_client(api_key="test-key")
                        with self.assertRaisesRegex(
                            TelemetryConfigurationError,
                            "Telemetry is not configured",
                        ):
                            get_telemetry_tracer(client)

                create_provider.assert_not_called()

    def test_internal_explicit_false_overrides_env_dedicated(self):
        with patch.dict(
            os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "dedicated"}, clear=True
        ):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client, telemetry=False)

        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(_get_tracing_hook(client).tracer_provider)

    def test_internal_explicit_false_disables_auto_telemetry_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client)
                configured = _configure_for_hook(client, telemetry=False)

        self.assertFalse(configured)
        self.assertTrue(provider.shutdown_called)
        self.assertIsNone(_get_tracing_hook(client).tracer_provider)

    def test_env_global_uses_global_provider_mode(self):
        with patch.dict(
            os.environ,
            {MISTRAL_SDK_TELEMETRY_ENV: "global"},
            clear=True,
        ):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client)

        hook = _get_tracing_hook(client)
        self.assertTrue(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)
        self.assertTrue(hook._telemetry_auto_disabled)

    def test_env_global_does_not_replace_manual_provider(self):
        manual_provider = TracerProvider()
        client = _make_client(api_key="test-key")

        with patch.object(manual_provider, "shutdown") as manual_shutdown:
            configure_telemetry(client, provider=manual_provider)

            with patch.dict(
                os.environ,
                {MISTRAL_SDK_TELEMETRY_ENV: "global"},
                clear=True,
            ):
                configured = _configure_for_hook(client)

        self.assertFalse(configured)
        self.assertIs(_get_tracing_hook(client).tracer_provider, manual_provider)
        manual_shutdown.assert_not_called()

    def test_env_dedicated_uses_mistral_api_key_fallback(self):
        provider = FakeProvider()
        env = {
            MISTRAL_SDK_TELEMETRY_ENV: "dedicated",
            "MISTRAL_API_KEY": "env-key",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key=None)
                configured = _configure_for_hook(client)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="env-key",
            server_url="",
            redaction=True,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_standard_otel_endpoint_env_does_not_avoid_mistral_api_key(self):
        env = {
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "http://collector:4318/v1/traces",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key=None)
                with self.assertRaisesRegex(
                    TelemetryConfigurationError,
                    "Mistral telemetry requires an API key",
                ):
                    configure_telemetry(client)

        create_provider.assert_not_called()

    def test_env_dedicated_ignores_standard_otel_endpoint_env(self):
        provider = FakeProvider()
        env = {
            MISTRAL_SDK_TELEMETRY_ENV: "dedicated",
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector:4318",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = _configure_for_hook(client)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="test-key",
            server_url="",
            redaction=True,
        )

    def test_sdk_config_global_uses_global_provider_mode(self):
        client = _make_client(api_key="test-key")
        client.sdk_configuration.__dict__["telemetry"] = "global"
        hook = _get_tracing_hook(client)

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                configured = configure_telemetry_for_hook(
                    hook, client.sdk_configuration
                )

        self.assertTrue(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)
        self.assertTrue(hook._telemetry_auto_disabled)

    def test_missing_optional_dependencies_raise_install_hint(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._load_otel_sdk",
                side_effect=TelemetryConfigurationError(
                    "Install them with `pip install 'mistralai[telemetry]'`."
                ),
            ):
                client = _make_client(api_key="test-key")
                with self.assertRaisesRegex(
                    TelemetryConfigurationError,
                    r"mistralai\[telemetry\]",
                ):
                    configure_telemetry(client)

    def test_manual_provider_replaces_auto_telemetry_provider(self):
        provider = FakeProvider()
        manual_provider = TracerProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client)

        set_tracer_provider(client, manual_provider)

        self.assertTrue(provider.shutdown_called)
        self.assertIs(_get_tracing_hook(client).tracer_provider, manual_provider)

    def test_configure_telemetry_for_hook_reads_sdk_config_telemetry_flag(self):
        provider = FakeProvider()
        client = _make_client(api_key="test-key")
        client.sdk_configuration.__dict__["telemetry"] = True
        hook = _get_tracing_hook(client)

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                configured = configure_telemetry_for_hook(
                    hook, client.sdk_configuration
                )

        self.assertTrue(configured)
        self.assertIs(hook.tracer_provider, provider)

    def test_auto_configuration_skips_existing_manual_provider(self):
        hook = TracingHook()
        manual_provider = MagicMock()
        hook.tracer_provider = manual_provider
        client = _make_client(api_key="test-key")

        with patch.dict(
            os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "dedicated"}, clear=True
        ):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                configured = configure_telemetry_for_hook(
                    hook,
                    client.sdk_configuration,
                )

        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIs(hook.tracer_provider, manual_provider)

    def test_env_auto_configuration_respects_existing_global_provider(self):
        client = _make_client(api_key="test-key")
        hook = _get_tracing_hook(client)

        with patch.dict(
            os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "dedicated"}, clear=True
        ):
            with patch(
                "mistralai.extra.observability.telemetry._has_real_global_tracer_provider",
                return_value=True,
            ):
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
                ) as create_provider:
                    with self.assertLogs(
                        "mistralai.extra.observability.telemetry",
                        level="DEBUG",
                    ) as logs:
                        configured = configure_telemetry_for_hook(
                            hook,
                            client.sdk_configuration,
                            respect_global_provider=True,
                        )

        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)
        self.assertTrue(hook._telemetry_auto_disabled)
        self.assertIn("global OpenTelemetry provider", logs.output[0])

    def test_mistral_exporter_uses_mistral_endpoint_and_auth(self):
        with patch(
            "mistralai.extra.observability.telemetry._load_otel_sdk",
            return_value=(
                FakeSpanProcessor,
                FakeExporter,
                FakeResource,
                FakeTracerProvider,
            ),
        ):
            provider = _create_telemetry_tracer_provider(
                api_key="test-key",
            )

        self.assertIsInstance(provider, FakeTracerProvider)
        self.assertEqual(len(FakeExporter.instances), 1)
        self.assertEqual(FakeExporter.instances[0].args, ())
        self.assertEqual(
            FakeExporter.instances[0].kwargs,
            {
                "endpoint": MISTRAL_TELEMETRY_ENDPOINT,
                "headers": {"Authorization": "Bearer test-key"},
            },
        )

    def test_mistral_endpoint_env_overrides_default_endpoint(self):
        custom_endpoint = "http://collector:4318/v1/traces"
        with patch(
            "mistralai.extra.observability.telemetry._load_otel_sdk",
            return_value=(
                FakeSpanProcessor,
                FakeExporter,
                FakeResource,
                FakeTracerProvider,
            ),
        ):
            with patch.dict(
                os.environ,
                {MISTRAL_OTLP_TRACES_ENDPOINT_ENV: custom_endpoint},
                clear=True,
            ):
                provider = _create_telemetry_tracer_provider(api_key="test-key")

        self.assertIsInstance(provider, FakeTracerProvider)
        self.assertEqual(len(FakeExporter.instances), 1)
        self.assertEqual(FakeExporter.instances[0].args, ())
        self.assertEqual(
            FakeExporter.instances[0].kwargs,
            {
                "endpoint": custom_endpoint,
                "headers": {"Authorization": "Bearer test-key"},
            },
        )


class TestTelemetryEndpoint(unittest.TestCase):
    @staticmethod
    def _export_for_client(
        client_options: dict[str, str],
        auto_enable: bool,
        endpoint_override: str | None = None,
    ) -> tuple[dict, str]:
        from mistralai.client.sdk import Mistral

        env = {MISTRAL_SDK_TELEMETRY_ENV: "dedicated"} if auto_enable else {}
        if endpoint_override is not None:
            env[MISTRAL_OTLP_TRACES_ENDPOINT_ENV] = endpoint_override
        request_urls: list[str] = []

        def handle_request(request: httpx.Request) -> httpx.Response:
            request_urls.append(str(request.url))
            return httpx.Response(200, json={"object": "list", "data": []})

        with (
            patch.dict(os.environ, env, clear=True),
            patch(
                "mistralai.extra.observability.telemetry._has_real_global_tracer_provider",
                return_value=False,
            ),
            patch(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter"
            ) as exporter_class,
            httpx.Client(transport=httpx.MockTransport(handle_request)) as http_client,
            Mistral(
                api_key="test-key",
                client=http_client,
                server=client_options.get("server"),
                server_url=client_options.get("server_url"),
            ) as client,
        ):
            exporter_class.return_value.export.return_value = SpanExportResult.SUCCESS
            if not auto_enable:
                configure_telemetry(client)
            try:
                client.models.list()
                provider = _get_tracing_hook(client)._auto_telemetry_provider
                assert provider is not None
                assert provider.force_flush()
                exporter_class.return_value.export.assert_called_once()
            finally:
                configure_telemetry(client, provider="global", redaction=False)

        exporter_class.assert_called_once()
        assert len(request_urls) == 1
        return dict(exporter_class.call_args.kwargs), request_urls[0]

    def test_telemetry_follows_explicit_server_url(self):
        """Each case is (client options, API base URL, telemetry base URL).

        Only an explicit server_url moves the telemetry endpoint: the named
        regional servers do not serve the telemetry route.
        """
        cases: list[tuple[dict[str, str], str, str]] = [
            ({}, "https://api.mistral.ai", "https://api.mistral.ai"),
            ({"server": "global"}, "https://api.mistral.ai", "https://api.mistral.ai"),
            ({"server": "eu"}, "https://api.eu.mistral.ai", "https://api.mistral.ai"),
            ({"server": "us"}, "https://api.us.mistral.ai", "https://api.mistral.ai"),
            (
                {"server_url": "https://mistral.example.com"},
                "https://mistral.example.com",
                "https://mistral.example.com",
            ),
            (
                {"server_url": "https://llm.acme-corp.io/"},
                "https://llm.acme-corp.io",
                "https://llm.acme-corp.io",
            ),
            (
                {"server_url": "https://gateway.internal.net/mistral/"},
                "https://gateway.internal.net/mistral",
                "https://gateway.internal.net/mistral",
            ),
            (
                {"server_url": "http://localhost:8080"},
                "http://localhost:8080",
                "http://localhost:8080",
            ),
            (
                {"server": "eu", "server_url": "https://mistral.contoso.dev"},
                "https://mistral.contoso.dev",
                "https://mistral.contoso.dev",
            ),
        ]
        for client_options, api_base_url, telemetry_base_url in cases:
            for auto_enable in (False, True):
                with self.subTest(
                    client_options=client_options, auto_enable=auto_enable
                ):
                    exporter_options, request_url = self._export_for_client(
                        client_options, auto_enable
                    )
                    self.assertEqual(request_url, f"{api_base_url}/v1/models")
                    self.assertEqual(
                        exporter_options,
                        {
                            "endpoint": f"{telemetry_base_url}/telemetry/v1/traces",
                            "headers": {"Authorization": "Bearer test-key"},
                        },
                    )

    def test_blank_endpoint_override_uses_api_server(self):
        for endpoint_override in (None, "", "  "):
            for auto_enable in (False, True):
                with self.subTest(
                    endpoint_override=endpoint_override, auto_enable=auto_enable
                ):
                    exporter_options, _ = self._export_for_client(
                        {"server_url": "https://inference.foobar.ai"},
                        auto_enable,
                        endpoint_override,
                    )
                    self.assertEqual(
                        exporter_options["endpoint"],
                        "https://inference.foobar.ai/telemetry/v1/traces",
                    )

    def test_endpoint_override_takes_precedence(self):
        for auto_enable in (False, True):
            with self.subTest(auto_enable=auto_enable):
                exporter_options, request_url = self._export_for_client(
                    {"server_url": "https://proxy.widgets.org"},
                    auto_enable,
                    "  https://collector.example.com/v1/traces  ",
                )
                self.assertEqual(request_url, "https://proxy.widgets.org/v1/models")
                self.assertEqual(
                    exporter_options,
                    {
                        "endpoint": "https://collector.example.com/v1/traces",
                        "headers": {"Authorization": "Bearer test-key"},
                    },
                )


_TELEMETRY_LOGGER = "mistralai.extra.observability.telemetry"


@pytest.fixture
def clear_exporters():
    FakeExporter.instances.clear()


class TestTelemetryRedaction:
    @staticmethod
    def _make_provider(**kwargs):
        with patch(
            "mistralai.extra.observability.telemetry._load_otel_sdk",
            return_value=(
                FakeSpanProcessor,
                FakeExporter,
                FakeResource,
                FakeTracerProvider,
            ),
        ):
            return _create_telemetry_tracer_provider(api_key="test-key", **kwargs)

    @staticmethod
    def _exporter_of(provider):
        assert len(provider.span_processors) == 1
        return provider.span_processors[0].exporter

    def test_dedicated_wraps_exporter_by_default(self, clear_exporters):
        provider = self._make_provider()
        exporter = self._exporter_of(provider)
        assert isinstance(exporter, RedactingSpanExporter)
        assert exporter._exporter is FakeExporter.instances[0]
        assert isinstance(exporter._policy, RegexRedactionPolicy)

    def test_redaction_true_wraps_with_default_policy(self, clear_exporters):
        provider = self._make_provider(redaction=True)
        exporter = self._exporter_of(provider)
        assert isinstance(exporter, RedactingSpanExporter)
        assert isinstance(exporter._policy, RegexRedactionPolicy)

    def test_redaction_false_leaves_exporter_unwrapped(self, clear_exporters):
        provider = self._make_provider(redaction=False)
        exporter = self._exporter_of(provider)
        assert not isinstance(exporter, RedactingSpanExporter)
        assert exporter is FakeExporter.instances[0]

    def test_custom_policy_instance_is_used(self, clear_exporters):
        policy = AttributeRedactionPolicy()
        provider = self._make_provider(redaction=policy)
        exporter = self._exporter_of(provider)
        assert isinstance(exporter, RedactingSpanExporter)
        assert exporter._policy is policy

    def test_callback_is_wrapped_in_callback_policy(self, clear_exporters):
        def mask(key, value):
            return value

        provider = self._make_provider(redaction=mask)
        exporter = self._exporter_of(provider)
        assert isinstance(exporter, RedactingSpanExporter)
        assert isinstance(exporter._policy, CallbackRedactionPolicy)

    def test_dedicated_mode_forwards_custom_redaction_to_provider(self):
        # Wiring test
        with patch(
            "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
        ) as create_provider:
            create_provider.return_value = FakeProvider()
            client = _make_client(api_key="test-key")
            policy = RegexRedactionPolicy()
            configure_telemetry(client, provider="dedicated", redaction=policy)

        create_provider.assert_called_once_with(
            api_key="test-key", server_url="", redaction=policy
        )

    def test_dedicated_mode_forwards_default_redaction_to_provider(self):
        # Wiring test
        with patch(
            "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
        ) as create_provider:
            create_provider.return_value = FakeProvider()
            client = _make_client(api_key="test-key")
            configure_telemetry(client, provider="dedicated")

        create_provider.assert_called_once_with(
            api_key="test-key", server_url="", redaction=True
        )

    def test_global_mode_warns_by_default(self, caplog):
        client = _make_client(api_key="test-key")
        with caplog.at_level("WARNING", logger=_TELEMETRY_LOGGER):
            configure_telemetry(client, provider="global")
        assert "Telemetry redaction is only applied in 'dedicated'" in caplog.text

    def test_global_mode_does_not_warn_when_redaction_disabled(self, caplog):
        client = _make_client(api_key="test-key")
        with caplog.at_level("WARNING", logger=_TELEMETRY_LOGGER):
            configure_telemetry(client, provider="global", redaction=False)
        assert not [r for r in caplog.records if r.name == _TELEMETRY_LOGGER]

    def test_custom_provider_warns_by_default(self, caplog):
        client = _make_client(api_key="test-key")
        with caplog.at_level("WARNING", logger=_TELEMETRY_LOGGER):
            configure_telemetry(client, provider=TracerProvider())
        assert "Telemetry redaction is only applied in 'dedicated'" in caplog.text

    def test_custom_provider_does_not_warn_when_redaction_disabled(self, caplog):
        client = _make_client(api_key="test-key")
        with caplog.at_level("WARNING", logger=_TELEMETRY_LOGGER):
            configure_telemetry(client, provider=TracerProvider(), redaction=False)
        assert not [r for r in caplog.records if r.name == _TELEMETRY_LOGGER]


@pytest.fixture
def clean_telemetry_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "MISTRAL_API_KEY",
        "MISTRAL_SA_TOKEN_PATH",
        MISTRAL_SDK_TELEMETRY_ENV,
        MISTRAL_OTLP_TRACES_ENDPOINT_ENV,
    ):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def sa_token(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    token_file = tmp_path / "token"
    token_file.write_text("sa-token-v1\n")
    monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(token_file))
    return token_file


@pytest.mark.usefixtures("clean_telemetry_env")
class TestServiceAccountTelemetry:
    @pytest.mark.parametrize(
        ("client_key", "env_key", "use_sa_token", "expected"),
        [
            ("explicit-key", "env-key", True, "explicit-key"),
            (None, "env-key", True, None),
            (None, "env-key", False, "env-key"),
        ],
    )
    def test_credential_follows_api_call_precedence(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        client_key: str | None,
        env_key: str,
        use_sa_token: bool,
        expected: str | None,
    ):
        """None means the exporter authenticates with the service-account token."""
        monkeypatch.setenv("MISTRAL_API_KEY", env_key)
        if use_sa_token:
            token_file = tmp_path / "token"
            token_file.write_text("sa-token")
            monkeypatch.setenv("MISTRAL_SA_TOKEN_PATH", str(token_file))
        monkeypatch.setenv(MISTRAL_SDK_TELEMETRY_ENV, "dedicated")

        with patch(
            "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
            return_value=FakeProvider(),
        ) as create_provider:
            client = _make_client(api_key=client_key)
            assert _configure_for_hook(client)

        assert create_provider.call_args.kwargs["api_key"] == expected

    def test_exporter_authenticates_with_a_session_instead_of_static_headers(
        self, sa_token: Path
    ):
        with patch(
            "mistralai.extra.observability.telemetry._load_otel_sdk",
            return_value=(
                FakeSpanProcessor,
                FakeExporter,
                FakeResource,
                FakeTracerProvider,
            ),
        ):
            FakeExporter.instances.clear()
            _create_telemetry_tracer_provider(api_key=None)

        kwargs = FakeExporter.instances[0].kwargs
        assert "headers" not in kwargs
        assert _sent_authorization(kwargs["session"]) == "Bearer sa-token-v1"

    def test_each_export_reads_the_rotated_token(self, sa_token: Path):
        session = _service_account_session()
        assert _sent_authorization(session) == "Bearer sa-token-v1"

        sa_token.write_text("sa-token-v2\n")

        assert _sent_authorization(session) == "Bearer sa-token-v2"

    def test_unreadable_token_fails_the_export(self, sa_token: Path):
        session = _service_account_session()
        sa_token.unlink()

        with pytest.raises(ServiceAccountTokenError):
            _sent_authorization(session)


def _sent_authorization(session: object) -> str | bytes | None:
    """Return the Authorization header a POST through session would send."""
    assert isinstance(session, requests.Session)
    request = session.prepare_request(
        requests.Request("POST", "https://telemetry.test/v1/traces")
    )
    return request.headers.get("Authorization")


@pytest.mark.usefixtures("clean_telemetry_env")
class TestTelemetrySetupNeverFailsApiCalls:
    @staticmethod
    def _list_models_twice() -> list[str | None]:
        from mistralai.client.sdk import Mistral

        sent: list[str | None] = []

        def handle(request: httpx.Request) -> httpx.Response:
            sent.append(request.headers.get("Authorization"))
            return httpx.Response(200, json={"object": "list", "data": []})

        with (
            patch(
                "mistralai.extra.observability.telemetry._has_real_global_tracer_provider",
                return_value=False,
            ),
            httpx.Client(transport=httpx.MockTransport(handle)) as http_client,
            Mistral(server_url="https://api.mistral.ai", client=http_client) as client,
        ):
            client.models.list()
            client.models.list()
        return sent

    @pytest.mark.parametrize(
        ("env", "load_otel_sdk_error"),
        [
            ({MISTRAL_SDK_TELEMETRY_ENV: "dedicated"}, None),
            (
                {MISTRAL_SDK_TELEMETRY_ENV: "dedicated", "MISTRAL_API_KEY": "env-key"},
                TelemetryConfigurationError("pip install 'mistralai[telemetry]'"),
            ),
            ({MISTRAL_SDK_TELEMETRY_ENV: "maybe", "MISTRAL_API_KEY": "env-key"}, None),
        ],
        ids=["no-credential", "missing-telemetry-extra", "invalid-setting"],
    )
    def test_warns_once_and_keeps_calling_the_api(
        self,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
        env: dict[str, str],
        load_otel_sdk_error: Exception | None,
    ):
        for name, value in env.items():
            monkeypatch.setenv(name, value)

        with (
            patch(
                "mistralai.extra.observability.telemetry._load_otel_sdk",
                side_effect=load_otel_sdk_error,
            )
            if load_otel_sdk_error
            else contextlib.nullcontext(),
            caplog.at_level("WARNING", logger="mistralai.client._hooks.tracing"),
        ):
            sent = self._list_models_twice()

        assert len(sent) == 2
        warnings = [
            r for r in caplog.records if r.name == "mistralai.client._hooks.tracing"
        ]
        assert len(warnings) == 1
        assert "telemetry is disabled" in warnings[0].getMessage()

    def test_service_account_client_exports_with_dedicated_telemetry(
        self, monkeypatch: pytest.MonkeyPatch, sa_token: Path
    ):
        from mistralai.client.sdk import Mistral

        monkeypatch.setenv(MISTRAL_SDK_TELEMETRY_ENV, "dedicated")

        def handle(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"object": "list", "data": []})

        with (
            patch(
                "mistralai.extra.observability.telemetry._has_real_global_tracer_provider",
                return_value=False,
            ),
            patch(
                "opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter"
            ) as exporter_class,
            httpx.Client(transport=httpx.MockTransport(handle)) as http_client,
            Mistral(server_url="https://api.mistral.ai", client=http_client) as client,
        ):
            exporter_class.return_value.export.return_value = SpanExportResult.SUCCESS
            client.models.list()
            provider = _get_tracing_hook(client)._auto_telemetry_provider
            assert provider is not None
            assert provider.force_flush()

        exported = [
            span
            for call in exporter_class.return_value.export.call_args_list
            for span in call.args[0]
        ]
        assert [span.name for span in exported] == ["list_models_v1_models_get"]
        exporter_class.assert_called_once()
        assert _sent_authorization(exporter_class.call_args.kwargs["session"]) == (
            "Bearer sa-token-v1"
        )


if __name__ == "__main__":
    unittest.main()
