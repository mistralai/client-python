"""Typed descriptors for connector dependencies and extensions."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from pydantic import BaseModel


class ConnectorSlot(BaseModel):
    """A declared connector dependency for a workflow execution.

    Mirrors the server-side ``ConnectorSlot`` from the workflow SDK plugin,
    providing a typed interface for specifying connector bindings instead of
    raw ``Dict[str, Any]`` extension dicts.

    Example::

        from mistralai.extra.workflows import ConnectorSlot

        gmail = ConnectorSlot(connector_name="gmail")
        notion = ConnectorSlot(connector_name="notion", credentials_name="work-account")
    """

    connector_name: str
    credentials_name: Optional[str] = None


class ConnectorBindings(BaseModel):
    """Container for a list of connector bindings."""

    bindings: List[ConnectorSlot]


class ConnectorExtension(BaseModel):
    """Mistral-specific extension carrying connector configuration."""

    connectors: ConnectorBindings


class WorkflowExtensions(BaseModel):
    """Top-level extensions dict passed to the workflow execution API.

    Serialises to the shape expected by the API::

        {"mistralai": {"connectors": {"bindings": [...]}}}
    """

    mistralai: ConnectorExtension

    @classmethod
    def from_connectors(cls, connectors: Sequence[ConnectorSlot]) -> WorkflowExtensions:
        """Build extensions from a sequence of connector slots."""
        return cls(
            mistralai=ConnectorExtension(
                connectors=ConnectorBindings(bindings=list(connectors))
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to the ``Dict[str, Any]`` the API expects."""
        return self.model_dump(mode="json", exclude_none=True)
