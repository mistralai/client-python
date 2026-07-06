"""Opt-in OpenTelemetry SDK configuration for Mistral telemetry."""

from __future__ import annotations

import logging
import os
import weakref
from typing import TYPE_CHECKING, Any, Final, Literal

from opentelemetry import trace as otel_trace

from mistralai.client.utils import get_security_from_env

from .otel import MISTRAL_SDK_OTEL_TRACER_NAME, OTEL_SERVICE_NAME

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider

    from mistralai.client.sdk import Mistral
    from mistralai.client.sdkconfiguration import SDKConfiguration
    from mistralai.client._hooks.tracing import TracingHook


MISTRAL_SDK_TELEMETRY_ENV = "MISTRAL_SDK_TELEMETRY"
MISTRAL_TELEMETRY_ENDPOINT = "https://api.mistral.ai/telemetry/v1/traces"
MISTRAL_OTLP_TRACES_ENDPOINT_ENV = "MISTRAL_OTLP_TRACES_ENDPOINT"
TELEMETRY_PROVIDER_DEDICATED: Final[Literal["dedicated"]] = "dedicated"
TELEMETRY_PROVIDER_GLOBAL: Final[Literal["global"]] = "global"

_DISABLED_VALUE = "false"
_PROVIDER_VALUES = {TELEMETRY_PROVIDER_DEDICATED, TELEMETRY_PROVIDER_GLOBAL}

TelemetryProviderMode = Literal["dedicated", "global"]
TelemetrySetting = bool | str | None

logger = logging.getLogger(__name__)


class TelemetryConfigurationError(RuntimeError):
    """Raised when opt-in telemetry cannot be configured."""


def _resolve_telemetry_mode(value: bool | str) -> TelemetryProviderMode | None:
    if isinstance(value, bool):
        return TELEMETRY_PROVIDER_DEDICATED if value else None

    normalized = value.strip().lower()
    if normalized == TELEMETRY_PROVIDER_DEDICATED:
        return TELEMETRY_PROVIDER_DEDICATED
    if normalized == TELEMETRY_PROVIDER_GLOBAL:
        return TELEMETRY_PROVIDER_GLOBAL
    if normalized == _DISABLED_VALUE:
        return None

    accepted_values = ", ".join(sorted(_PROVIDER_VALUES | {_DISABLED_VALUE}))
    raise TelemetryConfigurationError(
        f"Invalid telemetry setting {value!r}. Expected one of: {accepted_values}."
    )


def _resolve_provider_mode(value: str) -> TelemetryProviderMode:
    normalized = value.strip().lower()
    if normalized == TELEMETRY_PROVIDER_DEDICATED:
        return TELEMETRY_PROVIDER_DEDICATED
    if normalized == TELEMETRY_PROVIDER_GLOBAL:
        return TELEMETRY_PROVIDER_GLOBAL

    accepted_values = ", ".join(sorted(_PROVIDER_VALUES))
    raise TelemetryConfigurationError(
        f"Invalid telemetry provider {value!r}. Expected one of: {accepted_values}."
    )


def _resolve_mistral_telemetry_env() -> TelemetryProviderMode | None:
    env_value = os.getenv(MISTRAL_SDK_TELEMETRY_ENV)
    if env_value is None or env_value == "":
        return None

    try:
        return _resolve_telemetry_mode(env_value)
    except TelemetryConfigurationError as exc:
        accepted_values = ", ".join(sorted(_PROVIDER_VALUES | {_DISABLED_VALUE}))
        raise TelemetryConfigurationError(
            f"Invalid {MISTRAL_SDK_TELEMETRY_ENV}={env_value!r}. "
            f"Expected one of: {accepted_values}."
        ) from exc


def configure_telemetry(
    client: "Mistral",
    provider: str | otel_trace.TracerProvider = TELEMETRY_PROVIDER_DEDICATED,
) -> bool:
    """Configure telemetry provider mode for a Mistral client.

    By default, this creates an SDK-owned telemetry provider/exporter. Passing
    provider="global" clears the per-client provider so SDK spans use the
    global OpenTelemetry provider. Passing a TracerProvider attaches it to this
    client without taking ownership of its lifecycle.
    """
    hooks = getattr(client.sdk_configuration, "_hooks", None)
    if hooks is None:
        raise ValueError("Cannot configure telemetry: SDK hooks not initialised.")

    hook = _get_tracing_hook(hooks)
    if isinstance(provider, str):
        provider_mode = _resolve_provider_mode(provider)
        if provider_mode == TELEMETRY_PROVIDER_GLOBAL:
            return _use_global_tracer_provider(hook, replace_existing=True)

        return configure_telemetry_for_hook(
            hook,
            client.sdk_configuration,
            telemetry=provider_mode,
            finalizer_owner=client,
            replace_existing=True,
        )

    if isinstance(provider, bool):
        raise TelemetryConfigurationError(
            "Invalid telemetry provider bool. Expected 'dedicated', 'global', "
            "or an OpenTelemetry TracerProvider."
        )

    _attach_custom_tracer_provider(hook, provider)
    return True


def get_telemetry_tracer(
    client: "Mistral",
    name: str | None = None,
) -> otel_trace.Tracer:
    """Return a tracer from the telemetry provider configured for a client.

    Custom and SDK-owned dedicated providers are used directly. Clients
    explicitly configured for global telemetry use the OpenTelemetry global
    provider. If telemetry is disabled or has not been configured for this
    client, a TelemetryConfigurationError is raised.
    """
    hooks = getattr(client.sdk_configuration, "_hooks", None)
    if hooks is None:
        raise ValueError("Cannot get telemetry tracer: SDK hooks not initialised.")

    hook = _get_tracing_hook(hooks)
    tracer_name = name or MISTRAL_SDK_OTEL_TRACER_NAME

    if hook.tracer_provider is None and not hook._telemetry_use_global_provider:
        configure_telemetry_for_hook(
            hook,
            client.sdk_configuration,
            finalizer_owner=client,
            respect_global_provider=True,
        )

    if hook.tracer_provider is not None:
        return hook.tracer_provider.get_tracer(tracer_name)
    if hook._telemetry_use_global_provider:
        return otel_trace.get_tracer(tracer_name)

    raise TelemetryConfigurationError(
        "Telemetry is not configured for this client. Call configure_telemetry(client) "
        "or configure_telemetry(client, provider='global') before requesting a "
        "telemetry tracer."
    )


def configure_telemetry_for_hook(
    hook: "TracingHook",
    sdk_config: "SDKConfiguration",
    telemetry: TelemetrySetting = None,
    finalizer_owner: Any | None = None,
    respect_global_provider: bool = False,
    replace_existing: bool = False,
) -> bool:
    """Configure telemetry for a tracing hook when the user has opted in."""
    # Fast path: already resolved and no explicit override requested.
    if telemetry is None and (
        hook._auto_telemetry_provider is not None or hook._telemetry_use_global_provider
    ):
        return True
    if telemetry is None and hook._telemetry_auto_disabled:
        return False

    telemetry_setting = telemetry
    if telemetry_setting is None:
        config_setting = getattr(sdk_config, "telemetry", None)
        telemetry_setting = (
            config_setting if isinstance(config_setting, (bool, str)) else None
        )
    using_env_setting = telemetry_setting is None

    provider_mode = (
        _resolve_telemetry_mode(telemetry_setting)
        if telemetry_setting is not None
        else _resolve_mistral_telemetry_env()
    )
    if provider_mode is None:
        _shutdown_telemetry_provider(hook)
        hook._telemetry_use_global_provider = False
        hook._telemetry_auto_disabled = True
        return False

    if provider_mode == TELEMETRY_PROVIDER_GLOBAL:
        return _use_global_tracer_provider(
            hook,
            replace_existing=replace_existing or not using_env_setting,
        )

    if (
        provider_mode == TELEMETRY_PROVIDER_DEDICATED
        and respect_global_provider
        and using_env_setting
        and _has_real_global_tracer_provider()
    ):
        logger.debug(
            "Skipping Mistral SDK telemetry auto-configuration because a global "
            "OpenTelemetry provider is already configured. Call "
            "configure_telemetry(client, provider='dedicated') to attach an "
            "SDK-owned provider for this client."
        )
        hook._telemetry_use_global_provider = False
        hook._telemetry_auto_disabled = True
        return False

    if hook._auto_telemetry_provider is not None:
        return True

    if hook.tracer_provider is not None:
        if not replace_existing:
            return False
        hook.tracer_provider = None

    api_key = _resolve_api_key_from_security(getattr(sdk_config, "security", None))
    provider = _create_telemetry_tracer_provider(
        api_key=api_key,
    )
    _attach_telemetry_provider(hook, provider, finalizer_owner or sdk_config)
    return True


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
) -> "SDKTracerProvider":
    (
        batch_span_processor_cls,
        otlp_span_exporter_cls,
        resource_cls,
        tracer_provider_cls,
    ) = _load_otel_sdk()

    if api_key is None:
        raise TelemetryConfigurationError(
            "Mistral telemetry requires an API key. Pass api_key=... to the "
            "client or set MISTRAL_API_KEY."
        )
    exporter = otlp_span_exporter_cls(
        endpoint=_resolve_mistral_telemetry_endpoint(),
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


def _resolve_mistral_telemetry_endpoint() -> str:
    return os.getenv(
        MISTRAL_OTLP_TRACES_ENDPOINT_ENV,
        MISTRAL_TELEMETRY_ENDPOINT,
    ).strip() or MISTRAL_TELEMETRY_ENDPOINT


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
    hook._telemetry_use_global_provider = False
    hook._telemetry_auto_disabled = False
    hook._telemetry_finalizer = weakref.finalize(
        finalizer_owner, provider.shutdown
    )


def _attach_custom_tracer_provider(
    hook: "TracingHook",
    provider: otel_trace.TracerProvider,
) -> None:
    _shutdown_telemetry_provider(hook)
    hook.tracer_provider = provider
    hook._telemetry_use_global_provider = False
    hook._telemetry_auto_disabled = False


def _use_global_tracer_provider(
    hook: "TracingHook",
    *,
    replace_existing: bool,
) -> bool:
    if (
        hook.tracer_provider is not None
        and hook._auto_telemetry_provider is None
        and not replace_existing
    ):
        return False

    _shutdown_telemetry_provider(hook)
    hook.tracer_provider = None
    hook._telemetry_use_global_provider = True
    hook._telemetry_auto_disabled = True
    return True


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
