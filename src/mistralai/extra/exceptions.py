class MistralClientException(Exception):
    """Base exception for all the client errors."""


class RunException(MistralClientException):
    """Exception raised for errors during a conversation run."""


class MCPException(MistralClientException):
    """Exception raised for errors related to MCP operations."""


class MCPAuthException(MCPException):
    """Exception raised for authentication errors with an MCP server."""
