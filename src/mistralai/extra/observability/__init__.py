from contextlib import contextmanager
from typing import TYPE_CHECKING

from opentelemetry import trace as otel_trace

from .otel import MISTRAL_SDK_OTEL_TRACER_NAME
from .telemetry import (
    TelemetryConfigurationError,
    configure_telemetry,
)

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


@contextmanager
def trace(name: str, **kwargs):
    tracer = otel_trace.get_tracer(MISTRAL_SDK_OTEL_TRACER_NAME)
    with tracer.start_as_current_span(name, **kwargs) as span:
        yield span


def set_tracer_provider(
    client: "Mistral",
    provider: otel_trace.TracerProvider,
) -> None:
    """Attach a per-instance OpenTelemetry TracerProvider to a Mistral client.

    When set, all SDK spans produced by *client* will be emitted through
    *provider* instead of the global TracerProvider.

    This helper is kept for compatibility. New code can call
    configure_telemetry(client, provider=provider) directly.

    Usage::

        from opentelemetry.sdk.trace import TracerProvider
        from mistralai.client import Mistral
        from mistralai.extra.observability import set_tracer_provider

        client = Mistral(api_key="...")
        set_tracer_provider(client, TracerProvider())
    """
    configure_telemetry(client, provider=provider)


__all__ = [
    "TelemetryConfigurationError",
    "configure_telemetry",
    "set_tracer_provider",
    "trace",
]
