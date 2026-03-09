# ExecutionConfig

Not typed since mcp config can changed / not stable
we allow all extra fields and this is a dict
TODO: once mcp is stable, we need to type this


## Fields

| Field                | Type                 | Required             | Description          |
| -------------------- | -------------------- | -------------------- | -------------------- |
| `type`               | *str*                | :heavy_check_mark:   | N/A                  |
| `__pydantic_extra__` | Dict[str, *Any*]     | :heavy_minus_sign:   | N/A                  |