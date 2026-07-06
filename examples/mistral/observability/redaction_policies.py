#!/usr/bin/env python
"""Choosing and extending a redaction policy in dedicated telemetry mode.

The `redaction` argument of `configure_telemetry` accepts:
  - True (default): the regex (content-oriented) policy
  - False: redaction disabled
  - a RedactionPolicy instance (e.g. AttributeRedactionPolicy)
  - a (key, value) -> value | None callback

Built-in policies expose their defaults as public constants so you can
extend them instead of replacing them wholesale:
  - AttributeRedactionPolicy: DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
    DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS, DEFAULT_SAFE_ATTRIBUTE_KEYS,
    DEFAULT_TOKEN_PATTERNS
  - RegexRedactionPolicy: DEFAULT_PII_SECRET_PATTERNS

CallbackRedactionPolicy is different in kind: instead of extending constants you
supply a `(key, value) -> value | None` function and decide per attribute. It is
the only policy that can return None to drop an attribute entirely; the built-in
policies replace values in place and never remove keys.

`demonstrate()` applies the policies directly to a sample attribute mapping and
prints the before/after; it needs no API key and no network. `main()` wires an
extended policy into `configure_telemetry` and issues a live request (requires
the telemetry extra: pip install "mistralai[telemetry]").
"""

import os
import re

from opentelemetry.util.types import AttributeValue

from mistralai.client import Mistral
from mistralai.extra.observability import (
    DEFAULT_PII_SECRET_PATTERNS,
    DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
    AttributeRedactionPolicy,
    CallbackRedactionPolicy,
    RegexRedactionPolicy,
    configure_telemetry,
)

# A custom attribute key your application sets and wants masked, on top of the
# built-in sensitive keys.
CUSTOMER_EMAIL_KEY = "app.customer.email"

# A custom secret shape (e.g. an internal token) the default patterns don't know.
ACME_TOKEN_PATTERN = re.compile(r"\bacme-[a-z0-9]{16}\b")


def build_attribute_policy() -> AttributeRedactionPolicy:
    """Key-oriented policy: defaults plus one extra sensitive key."""
    return AttributeRedactionPolicy(
        sensitive_keys=DEFAULT_SENSITIVE_ATTRIBUTE_KEYS | {CUSTOMER_EMAIL_KEY},
    )


def build_regex_policy() -> RegexRedactionPolicy:
    """Content-oriented policy: default patterns plus one extra secret shape."""
    return RegexRedactionPolicy(
        patterns=(*DEFAULT_PII_SECRET_PATTERNS, ACME_TOKEN_PATTERN),
    )


def custom_mask(key: str, value: AttributeValue) -> AttributeValue | None:
    """Callback: full control over each attribute.

    Return the value to keep it, a transformed value to mask it, or None to drop
    the attribute entirely (something the built-in policies cannot do).
    """
    # Drop your application's private namespace outright.
    if key.startswith("app."):
        return None
    # Leave model/usage metadata untouched.
    if key.startswith(("gen_ai.request", "gen_ai.usage")):
        return value
    # Mask anything else with your own marker.
    return "***"


def build_callback_policy() -> CallbackRedactionPolicy:
    """Callback-based policy wrapping the custom_mask function above."""
    return CallbackRedactionPolicy(custom_mask)


def demonstrate() -> None:
    """Show, without any network call, what each extended policy redacts."""
    attributes = {
        # Safe key, survives both policies.
        "gen_ai.request.model": "mistral-small-latest",
        # Built-in sensitive key: whole value dropped by the attribute policy.
        "gen_ai.input.messages": "user: my card is 4111 1111 1111 1111",
        # Custom key we added to the attribute policy's sensitive set.
        CUSTOMER_EMAIL_KEY: "jane@example.com",
        # Free-form value carrying secrets: caught by the regex policy's patterns.
        "http.request.body": "Authorization: Bearer sk-abcdefghijklmnopqrst; "
        "internal=acme-0123456789abcdef",
    }

    for label, policy in (
        ("AttributeRedactionPolicy (extended keys)", build_attribute_policy()),
        ("RegexRedactionPolicy (extended patterns)", build_regex_policy()),
        ("CallbackRedactionPolicy (custom function)", build_callback_policy()),
    ):
        print(f"\n{label}")
        redacted = policy.redact_attributes(attributes)
        for key in attributes:
            # A callback may drop a key entirely (returns None), so it can be
            # absent from the redacted mapping.
            after = redacted[key] if key in redacted else "<dropped>"
            print(f"  {key}")
            print(f"    before: {attributes[key]}")
            print(f"    after : {after}")


def main() -> None:
    demonstrate()

    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("\nSet MISTRAL_API_KEY to run the live configure_telemetry example.")
        return

    with Mistral(api_key=api_key) as client:
        # Wire the extended attribute policy into dedicated telemetry mode.
        configure_telemetry(client, redaction=build_attribute_policy())

        # Alternatives:
        # configure_telemetry(client, redaction=build_regex_policy())
        # configure_telemetry(client, redaction=custom_mask)          # bare callback
        # configure_telemetry(client, redaction=build_callback_policy())
        # configure_telemetry(client, redaction=False)               # disable entirely

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Say hello."}],
        )
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
