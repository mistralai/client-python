#!/usr/bin/env python
"""Create, version, and alias a Prompt with the Mistral SDK (beta)."""
import os

from mistralai.client import Mistral


def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    # A prompt is a versioned template. `variables` declares the placeholder
    # names used in `content`; callers fill in the values themselves when they
    # use the prompt (the registry stores the template, it does not render it).
    prompt = client.beta.prompts.create(
        name="welcome-email",
        definition={
            "content": "Welcome to {{company}}! Great to have you in {{city}}.",
            "variables": [{"name": "city"}, {"name": "company"}],
        },
        title="Welcome email",
        notes="initial draft",
    )
    print(f"created prompt {prompt.id} (v{prompt.version})")

    # Iterate: a new definition creates a new immutable version. Passing
    # `aliases` here re-points "production" to the new version in one call.
    client.beta.prompts.create_version(
        prompt_id=prompt.id,
        definition={
            "content": "👋 Welcome to {{company}} — enjoy {{city}}!",
            "variables": [{"name": "city"}, {"name": "company"}],
        },
        notes="warmer tone",
        aliases=["production"],
    )

    # Read what "production" serves (latest by default; or pin ?version=/?alias=).
    live = client.beta.prompts.get(prompt_id=prompt.id, alias="production")
    print(f"production -> v{live.version}: {live.definition.content}")

    client.beta.prompts.delete(prompt_id=prompt.id)


if __name__ == "__main__":
    main()
