#!/usr/bin/env python
"""Choosing a redaction policy in dedicated telemetry mode.

The `redaction` argument accepts:
  - True (default): the regex (content-oriented) policy
  - False: redaction disabled
  - a RedactionPolicy instance (e.g. AttributeRedactionPolicy)
  - a (key, value) -> value | None callback

Requires the telemetry extra: pip install "mistralai[telemetry]"
"""

import os

from mistralai.client import Mistral
from mistralai.extra.observability import AttributeRedactionPolicy, configure_telemetry


def main() -> None:
    api_key = os.environ["MISTRAL_API_KEY"]

    with Mistral(api_key=api_key) as client:
        configure_telemetry(client, redaction=AttributeRedactionPolicy())

        # Alternatives:
        # configure_telemetry(client, redaction=False)  # disable entirely
        # configure_telemetry(                          # custom callback
        #     client,
        #     redaction=lambda key, value: None if "email" in key else value,
        # )

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Say hello."}],
        )
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
