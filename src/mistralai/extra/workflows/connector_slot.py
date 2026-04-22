"""Typed descriptor for a connector dependency."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ConnectorSlot(BaseModel):
    """A declared connector dependency for a workflow execution.

    Mirrors the server-side ``ConnectorSlot`` from the workflow SDK plugin,
    providing a typed interface for specifying connector bindings instead of
    raw ``Dict[str, Any]`` extension dicts.

    Example::

        from mistralai.extra.workflows import ConnectorSlot, run_workflow_with_connectors

        gmail = ConnectorSlot(connector_name="gmail")
        notion = ConnectorSlot(connector_name="notion", credentials_name="work-account")

        await run_workflow_with_connectors(
            "my-workflow",
            input_data=payload,
            connectors=[gmail, notion],
            api_key="...",
            server_url="...",
        )
    """

    connector_name: str
    credentials_name: Optional[str] = None
