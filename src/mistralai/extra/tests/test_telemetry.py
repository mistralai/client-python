import os
import unittest
from typing import TYPE_CHECKING, cast
from unittest.mock import MagicMock, patch

from opentelemetry.sdk.trace import TracerProvider

from mistralai.client._hooks import SDKHooks
from mistralai.client._hooks.tracing import TracingHook
from mistralai.client.models import Security
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils.logger import get_default_logger
from mistralai.extra.observability import configure_telemetry, set_tracer_provider
from mistralai.extra.observability.telemetry import (
    MISTRAL_TELEMETRY_ENDPOINT,
    MISTRAL_SDK_TELEMETRY_ENV,
    OTEL_EXPORTER_OTLP_ENDPOINT_ENV,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV,
    TelemetryConfigurationError,
    _create_telemetry_tracer_provider,
    configure_telemetry_for_hook,
    resolve_telemetry_enabled,
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
    tracing_hooks = [h for h in hooks.before_request_hooks if isinstance(h, TracingHook)]
    assert len(tracing_hooks) == 1
    return tracing_hooks[0]


class FakeProvider:
    def __init__(self):
        self.shutdown_called = False

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

    def test_resolve_telemetry_enabled_defaults_to_false(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(resolve_telemetry_enabled())

    def test_resolve_telemetry_enabled_parses_env_values(self):
        for value in ("1", "true", "yes", "on"):
            with self.subTest(value=value):
                with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: value}):
                    self.assertTrue(resolve_telemetry_enabled())

        for value in ("0", "false", "no", "off"):
            with self.subTest(value=value):
                with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: value}):
                    self.assertFalse(resolve_telemetry_enabled())

    def test_otel_traces_endpoint_env_does_not_enable_telemetry(self):
        with patch.dict(
            os.environ,
            {OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV: "http://collector:4318/v1/traces"},
            clear=True,
        ):
            self.assertFalse(resolve_telemetry_enabled())

    def test_otel_endpoint_env_does_not_enable_telemetry(self):
        with patch.dict(
            os.environ,
            {OTEL_EXPORTER_OTLP_ENDPOINT_ENV: "http://collector:4318"},
            clear=True,
        ):
            self.assertFalse(resolve_telemetry_enabled())

    def test_mistral_env_false_disables_otel_endpoint_env_autoconfiguration(self):
        env = {
            MISTRAL_SDK_TELEMETRY_ENV: "false",
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV: "http://collector:4318/v1/traces",
        }

        with patch.dict(os.environ, env, clear=True):
            self.assertFalse(resolve_telemetry_enabled())

    def test_configure_telemetry_attaches_per_client_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = configure_telemetry(client, telemetry=True)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="test-key",
            use_otel_env_exporter=False,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_explicit_false_overrides_env_true(self):
        with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "true"}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                client = _make_client(api_key="test-key")
                configured = configure_telemetry(client, telemetry=False)

        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(_get_tracing_hook(client).tracer_provider)

    def test_explicit_false_disables_auto_telemetry_provider(self):
        provider = FakeProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client, telemetry=True)
                configured = configure_telemetry(client, telemetry=False)

        self.assertFalse(configured)
        self.assertTrue(provider.shutdown_called)
        self.assertIsNone(_get_tracing_hook(client).tracer_provider)

    def test_env_true_uses_mistral_api_key_fallback(self):
        provider = FakeProvider()
        env = {
            MISTRAL_SDK_TELEMETRY_ENV: "true",
            "MISTRAL_API_KEY": "env-key",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ) as create_provider:
                client = _make_client(api_key=None)
                configured = configure_telemetry(client)

        self.assertTrue(configured)
        create_provider.assert_called_once_with(
            api_key="env-key",
            use_otel_env_exporter=False,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_otel_endpoint_env_configures_without_mistral_api_key(self):
        provider = FakeProvider()
        env = {
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV: "http://collector:4318/v1/traces",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._resolve_api_key_from_security"
            ) as resolve_api_key:
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                    return_value=provider,
                ) as create_provider:
                    client = _make_client(api_key=None)
                    configured = configure_telemetry(client, telemetry=True)

        self.assertTrue(configured)
        resolve_api_key.assert_not_called()
        create_provider.assert_called_once_with(
            api_key=None,
            use_otel_env_exporter=True,
        )
        self.assertIs(_get_tracing_hook(client).tracer_provider, provider)

    def test_env_true_prefers_otel_endpoint_env_over_mistral_endpoint(self):
        provider = FakeProvider()
        env = {
            MISTRAL_SDK_TELEMETRY_ENV: "true",
            OTEL_EXPORTER_OTLP_ENDPOINT_ENV: "http://collector:4318",
        }

        with patch.dict(os.environ, env, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._resolve_api_key_from_security"
            ) as resolve_api_key:
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                    return_value=provider,
                ) as create_provider:
                    client = _make_client(api_key=None)
                    configured = configure_telemetry(client)

        self.assertTrue(configured)
        resolve_api_key.assert_not_called()
        create_provider.assert_called_once_with(
            api_key=None,
            use_otel_env_exporter=True,
        )

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
                    configure_telemetry(client, telemetry=True)

    def test_manual_provider_replaces_auto_telemetry_provider(self):
        provider = FakeProvider()
        manual_provider = TracerProvider()

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider",
                return_value=provider,
            ):
                client = _make_client(api_key="test-key")
                configure_telemetry(client, telemetry=True)

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
                configured = configure_telemetry_for_hook(hook, client.sdk_configuration)

        self.assertTrue(configured)
        self.assertIs(hook.tracer_provider, provider)

    def test_auto_configuration_skips_existing_manual_provider(self):
        hook = TracingHook()
        manual_provider = MagicMock()
        hook.tracer_provider = manual_provider
        client = _make_client(api_key="test-key")

        with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "true"}, clear=True):
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

        with patch.dict(os.environ, {MISTRAL_SDK_TELEMETRY_ENV: "true"}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._has_real_global_tracer_provider",
                return_value=True,
            ):
                with patch(
                    "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
                ) as create_provider:
                    configured = configure_telemetry_for_hook(
                        hook,
                        client.sdk_configuration,
                        respect_global_provider=True,
                    )

        self.assertFalse(configured)
        create_provider.assert_not_called()
        self.assertIsNone(hook.tracer_provider)

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
                use_otel_env_exporter=False,
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

    def test_otel_env_exporter_uses_exporter_environment_defaults(self):
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
                api_key=None,
                use_otel_env_exporter=True,
            )

        self.assertIsInstance(provider, FakeTracerProvider)
        self.assertEqual(len(FakeExporter.instances), 1)
        self.assertEqual(FakeExporter.instances[0].args, ())
        self.assertEqual(FakeExporter.instances[0].kwargs, {})


if __name__ == "__main__":
    unittest.main()
