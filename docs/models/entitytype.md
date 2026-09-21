# EntityType

The type of entity, used to share a library.

## Example Usage

```python
from mistralai.client.models import EntityType

# Open enum: unrecognized values are captured as UnrecognizedStr
value: EntityType = "User"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"User"`
- `"Workspace"`
- `"Org"`
