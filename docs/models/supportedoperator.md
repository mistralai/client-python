# SupportedOperator

## Example Usage

```python
from mistralai.client.models import SupportedOperator

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SupportedOperator = "eq"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"eq"`
- `"neq"`
- `"lt"`
- `"lte"`
- `"gt"`
- `"gte"`
- `"like"`
- `"ilike"`
- `"not_like"`
- `"not_ilike"`
- `"between"`
- `"not_between"`
- `"in"`
- `"not_in"`
- `"exists"`
- `"not_exists"`
- `"regexp"`
- `"not_regexp"`
- `"contains"`
- `"not_contains"`
- `"has"`
- `"hasAny"`
- `"hasAll"`
- `"hasToken"`
