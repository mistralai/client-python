#!/usr/bin/env python
"""Dedicated telemetry mode.

The SDK creates and owns an OTLP exporter that ships spans to the Mistral
telemetry endpoint. Spans are redacted before export.

Requires the telemetry extra: pip install "mistralai[telemetry]"
"""

import os

from mistralai.client import Mistral
from mistralai.extra.observability import configure_telemetry


def main() -> None:
    api_key = os.environ["MISTRAL_API_KEY"]

    with Mistral(api_key=api_key) as client:
        # Dedicated mode is the default; redaction is on by default.
        configure_telemetry(client)

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "What is the best French cheese?"}],
        )
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
