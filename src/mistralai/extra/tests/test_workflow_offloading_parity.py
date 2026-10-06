"""Guards the offloading and compression fixtures replayed by the TS client's test suite."""

import pytest

from mistralai.extra.tests.fixtures.workflow_offloading_parity import (
    FIXTURE_PATH,
    render_fixtures,
)


@pytest.mark.skipif(
    not FIXTURE_PATH.parent.exists(),
    reason="The TS client is only next to this client in the dashboard monorepo",
)
def test_workflow_offloading_parity_fixtures_are_up_to_date():
    assert FIXTURE_PATH.exists() and render_fixtures() == FIXTURE_PATH.read_text(
        encoding="utf-8"
    ), (
        "The Python client no longer produces the committed offloading fixtures. "
        "Regenerate them with `uv run python -m "
        "mistralai.extra.tests.fixtures.workflow_offloading_parity`, then make "
        "sure the TS client tests still pass."
    )
