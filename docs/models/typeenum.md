# TypeEnum

## Example Usage

```python
from mistralai.client.models import TypeEnum

# Open enum: unrecognized values are captured as UnrecognizedStr
value: TypeEnum = "ENUM"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"ENUM"`
- `"TEXT"`
- `"INT"`
- `"FLOAT"`
- `"BOOL"`
- `"TIMESTAMP"`
- `"ARRAY"`
