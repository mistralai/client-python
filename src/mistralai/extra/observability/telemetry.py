"""Opt-in OpenTelemetry SDK configuration for Mistral telemetry."""

from __future__ import annotations

import os
import weakref
from typing import TYPE_CHECKING, Any

from opentelemetry import trace as otel_trace

from mistralai.client.utils import get_security_from_env

from .otel import OTEL_SERVICE_NAME

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider

    from mistralai.client.sdk import Mistral
    from mistralai.client.sdkconfiguration import SDKConfiguration
    from mistralai.client._hooks.tracing import TracingHook


MISTRAL_SDK_TELEMETRY_ENV = "MISTRAL_SDK_TELEMETRY"
MISTRAL_TELEMETRY_ENDPOINT = "https://api.mistral.ai/telemetry/v1/traces"
OTEL_EXPORTER_OTLP_ENDPOINT_ENV = "OTEL_EXPORTER_OTLP_ENDPOINT"
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV = "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


class TelemetryConfigurationError(RuntimeError):
    """Raised when opt-in telemetry cannot be configured."""


def resolve_telemetry_enabled(telemetry: bool | None = None) -> bool:
    """Resolve the telemetry opt-in flag from an explicit value or environment."""
    return _resolve_telemetry_configuration(telemetry)[0]


def _resolve_telemetry_configuration(
    telemetry: bool | None = None,
) -> tuple[bool, bool]:
    """Return whether telemetry is enabled and whether to use OTel env config."""
    use_otel_env_exporter = _has_otel_exporter_endpoint_env()
    if telemetry is not None:
        return telemetry, telemetry and use_otel_env_exporter

    env_telemetry = _resolve_mistral_telemetry_env()
    if env_telemetry is not None:
        return env_telemetry, env_telemetry and use_otel_env_exporter

    return False, False


def _resolve_mistral_telemetry_env() -> bool | None:
    env_value = os.getenv(MISTRAL_SDK_TELEMETRY_ENV)
    if env_value is None or env_value == "":
        return None

    normalized = env_value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False

    accepted_values = ", ".join(sorted(_TRUE_VALUES | _FALSE_VALUES))
    raise TelemetryConfigurationError(
        f"Invalid {MISTRAL_SDK_TELEMETRY_ENV}={env_value!r}. "
        f"Expected one of: {accepted_values}."
    )


def _has_otel_exporter_endpoint_env() -> bool:
    return any(
        bool(os.getenv(env_name, "").strip())
        for env_name in (
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_ENV,
            OTEL_EXPORTER_OTLP_ENDPOINT_ENV,
        )
    )


def configure_telemetry(client: "Mistral") -> bool:
    """Configure an isolated telemetry provider for a Mistral client.

    Calling configure_telemetry(client) explicitly enables SDK telemetry.
    Environment and SDKConfiguration-based auto-resolution are handled by the
    request hook.

    Returns True when telemetry is enabled and a provider is attached. Returns
    False when a non-telemetry provider is already set.
    """
    hooks = getattr(client.sdk_configuration, "_hooks", None)
    if hooks is None:
        raise ValueError("Cannot configure telemetry: SDK hooks not initialised.")

    return configure_telemetry_for_hook(
        _get_tracing_hook(hooks),
        client.sdk_configuration,
        telemetry=True,
        finalizer_owner=client,
    )


def configure_telemetry_for_hook(
    hook: "TracingHook",
    sdk_config: "SDKConfiguration",
    telemetry: bool | None = None,
    finalizer_owner: Any | None = None,
    respect_global_provider: bool = False,
) -> bool:
    """Configure telemetry for a tracing hook when the user has opted in."""
    # Fast path: already resolved and no explicit override requested.
    if hook._auto_telemetry_provider is not None and telemetry is not False:
        return True
    if telemetry is False and hook._auto_telemetry_provider is None:
        return False
    if telemetry is None and hook._telemetry_auto_disabled:
        return False

    telemetry_setting = telemetry
    if telemetry_setting is None:
        config_setting = getattr(sdk_config, "telemetry", None)
        telemetry_setting = config_setting if isinstance(config_setting, bool) else None
    using_env_setting = telemetry_setting is None

    telemetry_enabled, use_otel_env_exporter = _resolve_telemetry_configuration(
        telemetry_setting
    )
    if not telemetry_enabled:
        if telemetry_setting is False:
            _shutdown_telemetry_provider(hook)
            hook._telemetry_auto_disabled = False
        elif using_env_setting:
            hook._telemetry_auto_disabled = True
        return False

    if (
        respect_global_provider
        and using_env_setting
        and _has_real_global_tracer_provider()
    ):
        return False

    if hook._auto_telemetry_provider is not None:
        return True

    if hook.tracer_provider is not None:
        return False

    api_key = (
        None
        if use_otel_env_exporter
        else _resolve_api_key_from_security(getattr(sdk_config, "security", None))
    )
    provider = _create_telemetry_tracer_provider(
        api_key=api_key,
        use_otel_env_exporter=use_otel_env_exporter,
    )
    _attach_telemetry_provider(hook, provider, finalizer_owner or sdk_config)
    return True


def set_tracing_hook_provider(
    client: "Mistral",
    provider: otel_trace.TracerProvider,
) -> None:
    """Attach a provider to the client's tracing hook, replacing auto telemetry."""
    hooks = getattr(client.sdk_configuration, "_hooks", None)
    if hooks is None:
        raise ValueError(
            "Cannot set tracer_provider: SDK hooks not initialised on this client."
        )

    hook = _get_tracing_hook(hooks)
    _shutdown_telemetry_provider(hook)
    hook.tracer_provider = provider


def _get_tracing_hook(hooks: Any) -> "TracingHook":
    from mistralai.client._hooks.tracing import TracingHook

    for hook in hooks.before_request_hooks:
        if isinstance(hook, TracingHook):
            return hook

    raise ValueError(
        "Cannot configure telemetry: TracingHook not found in the client's hooks."
    )


def _resolve_api_key_from_security(security: Any) -> str:
    from mistralai.client.models import Security

    if callable(security):
        security = security()

    if getattr(security, "api_key", None) is None:
        security = None

    security = get_security_from_env(security, Security)
    api_key = getattr(security, "api_key", None) if security is not None else None
    if api_key is None:
        raise TelemetryConfigurationError(
            "Mistral telemetry requires an API key. Pass api_key=... to the "
            "client or set MISTRAL_API_KEY."
        )

    return str(api_key)


def _create_telemetry_tracer_provider(
    *,
    api_key: str | None,
    use_otel_env_exporter: bool,
) -> "SDKTracerProvider":
    (
        batch_span_processor_cls,
        otlp_span_exporter_cls,
        resource_cls,
        tracer_provider_cls,
    ) = _load_otel_sdk()

    if use_otel_env_exporter:
        exporter = otlp_span_exporter_cls()
    else:
        if api_key is None:
            raise TelemetryConfigurationError(
                "Mistral telemetry requires an API key. Pass api_key=... to the "
                "client or set MISTRAL_API_KEY."
            )
        exporter = otlp_span_exporter_cls(
            endpoint=MISTRAL_TELEMETRY_ENDPOINT,
            headers={"Authorization": _as_bearer_token(api_key)},
        )
    provider = tracer_provider_cls(
        resource=resource_cls.create({"service.name": OTEL_SERVICE_NAME})
    )
    provider.add_span_processor(batch_span_processor_cls(exporter))
    return provider


def _load_otel_sdk():
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError as exc:
        raise TelemetryConfigurationError(
            "Mistral telemetry requires optional OpenTelemetry SDK/exporter "
            "dependencies. Install them with `pip install 'mistralai[telemetry]'` "
            "or `uv add 'mistralai[telemetry]'`."
        ) from exc

    return BatchSpanProcessor, OTLPSpanExporter, Resource, TracerProvider


def _has_real_global_tracer_provider() -> bool:
    return not isinstance(
        otel_trace.get_tracer_provider(),
        otel_trace.ProxyTracerProvider,
    )


def _attach_telemetry_provider(
    hook: "TracingHook",
    provider: "SDKTracerProvider",
    finalizer_owner: Any,
) -> None:
    _shutdown_telemetry_provider(hook)
    hook.tracer_provider = provider
    hook._auto_telemetry_provider = provider
    hook._telemetry_auto_disabled = False
    hook._telemetry_finalizer = weakref.finalize(
        finalizer_owner, provider.shutdown
    )


def _shutdown_telemetry_provider(hook: "TracingHook") -> None:
    finalizer = hook._telemetry_finalizer
    if finalizer is not None:
        finalizer.detach()
        hook._telemetry_finalizer = None

    provider = hook._auto_telemetry_provider
    if provider is not None:
        provider.shutdown()
        if hook.tracer_provider is provider:
            hook.tracer_provider = None
        hook._auto_telemetry_provider = None


def _as_bearer_token(api_key: str) -> str:
    return api_key if api_key.lower().startswith("bearer ") else f"Bearer {api_key}"
