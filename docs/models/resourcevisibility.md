# ResourceVisibility

## Example Usage

```python
from mistralai.client.models import ResourceVisibility

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ResourceVisibility = "shared_global"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"shared_global"`
- `"shared_org"`
- `"shared_workspace"`
- `"private"`
