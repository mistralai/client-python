# Roles

## Example Usage

```python
from mistralai.client.models import Roles

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Roles = "system"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"system"`
- `"user"`
- `"assistant"`
- `"tool"`
