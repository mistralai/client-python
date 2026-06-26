# SchemaFieldDataType

## Example Usage

```python
from mistralai.client.models import SchemaFieldDataType

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SchemaFieldDataType = "int"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"int"`
- `"bool"`
- `"string"`
- `"embedding"`
- `"long"`
- `"float"`
