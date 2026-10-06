"""Guards the encryption fixtures replayed by the TS client's test suite."""

import pytest

from mistralai.extra.tests.fixtures.workflow_encryption_parity import (
    FIXTURE_PATH,
    render_fixtures,
)


@pytest.mark.skipif(
    not FIXTURE_PATH.exists(),
    reason="The TS client is only next to this client in the dashboard monorepo",
)
def test_workflow_encryption_parity_fixtures_are_up_to_date():
    assert render_fixtures() == FIXTURE_PATH.read_text(encoding="utf-8"), (
        "The Python client no longer produces the committed encryption fixtures. "
        "Regenerate them with `uv run python -m "
        "mistralai.extra.tests.fixtures.workflow_encryption_parity`, then make "
        "sure the TS client tests still pass."
    )
