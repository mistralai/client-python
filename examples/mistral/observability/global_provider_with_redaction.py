#!/usr/bin/env python
"""Global provider mode with application-owned redaction.

In global (or custom TracerProvider) mode your application owns the OTEL export
pipeline, so `configure_telemetry`'s redaction argument is ignored. To redact
spans you wrap your own exporter with RedactingSpanExporter.

Requires the telemetry extra: pip install "mistralai[telemetry]"
"""

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from mistralai.client import Mistral
from mistralai.extra.observability import RedactingSpanExporter, configure_telemetry


def main() -> None:
    api_key = os.environ["MISTRAL_API_KEY"]

    # Build your own provider and wrap the exporter with redaction.
    provider = TracerProvider()
    provider.add_span_processor(
        BatchSpanProcessor(RedactingSpanExporter(OTLPSpanExporter()))
    )
    trace.set_tracer_provider(provider)

    with Mistral(api_key=api_key) as client:
        # SDK spans flow through the global provider configured above.
        configure_telemetry(client, provider="global")

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Say hello."}],
        )
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
