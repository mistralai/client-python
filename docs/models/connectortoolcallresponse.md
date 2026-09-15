# ConnectorToolCallResponse

Response from calling an MCP tool.

We override mcp_types.CallToolResult because:
- Models only support `content`, not `structuredContent` at top level
- Downstream consumers (le-chat, etc.) need structuredContent/isError/_meta via metadata

SYNC: Keep in sync with Harmattan (orchestrator) for harmonized tool result processing.


## Fields

| Field                                                                                          | Type                                                                                           | Required                                                                                       | Description                                                                                    |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `content`                                                                                      | List[[models.ConnectorToolCallResponseContent](../models/connectortoolcallresponsecontent.md)] | :heavy_check_mark:                                                                             | N/A                                                                                            |
| `metadata`                                                                                     | [OptionalNullable[models.ConnectorToolCallMetadata]](../models/connectortoolcallmetadata.md)   | :heavy_minus_sign:                                                                             | N/A                                                                                            |
| `__pydantic_extra__`                                                                           | Dict[str, *Any*]                                                                               | :heavy_minus_sign:                                                                             | N/A                                                                                            |