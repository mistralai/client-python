# BaseFieldDefinitionType

## Example Usage

```python
from mistralai.client.models import BaseFieldDefinitionType

# Open enum: unrecognized values are captured as UnrecognizedStr
value: BaseFieldDefinitionType = "ENUM"
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
- `"MAP"`
