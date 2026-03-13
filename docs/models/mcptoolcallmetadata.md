# MCPToolCallMetadata

Metadata wrapper for MCP tool call responses.

Nests MCP-specific fields under `mcp_meta` to avoid collisions with other
metadata keys (e.g. `tool_call_result`) in Harmattan's streaming deltas.


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `mcp_meta`                                                                   | [OptionalNullable[models.MCPResultMetadata]](../models/mcpresultmetadata.md) | :heavy_minus_sign:                                                           | N/A                                                                          |
| `__pydantic_extra__`                                                         | Dict[str, *Any*]                                                             | :heavy_minus_sign:                                                           | N/A                                                                          |