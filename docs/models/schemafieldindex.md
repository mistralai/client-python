# SchemaFieldIndex

## Example Usage

```python
from mistralai.client.models import SchemaFieldIndex

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SchemaFieldIndex = "ann"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"ann"`
- `"bm25"`
- `"attribute"`
