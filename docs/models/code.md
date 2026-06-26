# Code

Machine-readable error code.

## Example Usage

```python
from mistralai.client.models import Code

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Code = "canceled"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"canceled"`
- `"unknown"`
- `"invalid_argument"`
- `"deadline_exceeded"`
- `"not_found"`
- `"already_exists"`
- `"permission_denied"`
- `"resource_exhausted"`
- `"failed_precondition"`
- `"aborted"`
- `"out_of_range"`
- `"unimplemented"`
- `"internal"`
- `"unavailable"`
- `"data_loss"`
- `"unauthenticated"`
