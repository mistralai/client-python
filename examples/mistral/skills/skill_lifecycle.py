#!/usr/bin/env python
"""Create, version, and alias an agent Skill (with assets) — Mistral SDK (beta)."""
import os

from mistralai.client import Mistral


def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    # A skill = model-facing instructions (`description` + `body`) plus optional
    # companion `assets`, all versioned together. `description` is what tells the
    # agent when to use the skill, so it is part of the versioned definition.
    # `aliases` are movable labels; `main` marks the runnable version.
    skill = client.beta.skills.create(
        name="release-notes",
        definition={
            "description": "Use when turning merged PRs into release notes.",
            "body": "# Release notes\nGroup changes under Added / Fixed / Changed.",
            "assets": {
                "template.md": {"text_content": "## Added\n## Fixed\n## Changed", "is_executable": False},
            },
        },
        notes="initial",
        aliases=["main"],
    )
    print(f"created skill {skill.id} (v{skill.version}), assets: {list(skill.definition.assets)}")

    # Improve the instructions -> new immutable version, and move `main` to it in
    # one call (passing aliases on create_version re-points them to the new version).
    version = client.beta.skills.create_version(
        skill_id=skill.id,
        definition={
            "description": "Use when turning merged PRs into release notes, grouped by type.",
            "body": "# Release notes v2\nGroup changes under Added / Fixed / Changed / Security.",
        },
        notes="add Security section",
        aliases=["main"],
    )
    print(f"published v{version.version}, moved 'main' to it")

    runnable = client.beta.skills.get(skill_id=skill.id, alias="main")
    print(f"main -> v{runnable.version}: {runnable.definition.description}")

    client.beta.skills.delete(skill_id=skill.id)


if __name__ == "__main__":
    main()
