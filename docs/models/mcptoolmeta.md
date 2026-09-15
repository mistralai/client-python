# MCPToolMeta

Typed _meta for MCP tools.

Only the 'ui' field is typed. Other fields are allowed via extra="allow".


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `ui`                                                                     | [OptionalNullable[models.MCPUIToolMeta]](../models/mcpuitoolmeta.md)     | :heavy_minus_sign:                                                       | N/A                                                                      |
| `ai_mistral_turbine`                                                     | [OptionalNullable[models.TurbineToolMeta]](../models/turbinetoolmeta.md) | :heavy_minus_sign:                                                       | N/A                                                                      |
| `__pydantic_extra__`                                                     | Dict[str, *Any*]                                                         | :heavy_minus_sign:                                                       | N/A                                                                      |