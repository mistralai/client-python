# SchemaFieldStorage

## Example Usage

```python
from mistralai.client.models import SchemaFieldStorage

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SchemaFieldStorage = "in_memory"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"in_memory"`
- `"on_disk"`
