# ToolAnnotations

Additional properties describing a Tool to clients.

NOTE: all properties in ToolAnnotations are **hints**.
They are not guaranteed to provide a faithful description of
tool behavior (including descriptive properties like `title`).

Clients should never make tool use decisions based on ToolAnnotations
received from untrusted servers.


## Fields

| Field                    | Type                     | Required                 | Description              |
| ------------------------ | ------------------------ | ------------------------ | ------------------------ |
| `title`                  | *OptionalNullable[str]*  | :heavy_minus_sign:       | N/A                      |
| `read_only_hint`         | *OptionalNullable[bool]* | :heavy_minus_sign:       | N/A                      |
| `destructive_hint`       | *OptionalNullable[bool]* | :heavy_minus_sign:       | N/A                      |
| `idempotent_hint`        | *OptionalNullable[bool]* | :heavy_minus_sign:       | N/A                      |
| `open_world_hint`        | *OptionalNullable[bool]* | :heavy_minus_sign:       | N/A                      |
| `__pydantic_extra__`     | Dict[str, *Any*]         | :heavy_minus_sign:       | N/A                      |