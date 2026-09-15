# ManagedIndexStatus

Lifecycle of an index. Derived, not stored -- see ``managed_index_from_row``.

## Example Usage

```python
from mistralai.client.models import ManagedIndexStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ManagedIndexStatus = "provisioning"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"provisioning"`
- `"ready"`
- `"failed"`
- `"deleting"`
