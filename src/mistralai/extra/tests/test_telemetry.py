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
    MISTRAL_OTLP_TRACES_ENDPOINT_ENV,
    TelemetryConfigurationError,
    _create_telemetry_tracer_provider,
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
    tracing_hooks = [h for h in hooks.before_request_hooks if isinstance(h, TracingHook)]
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
        )

    def test_sdk_config_global_uses_global_provider_mode(self):
        client = _make_client(api_key="test-key")
        client.sdk_configuration.__dict__["telemetry"] = "global"
        hook = _get_tracing_hook(client)

        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "mistralai.extra.observability.telemetry._create_telemetry_tracer_provider"
            ) as create_provider:
                configured = configure_telemetry_for_hook(hook, client.sdk_configuration)

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
                configured = configure_telemetry_for_hook(hook, client.sdk_configuration)

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


if __name__ == "__main__":
    unittest.main()
