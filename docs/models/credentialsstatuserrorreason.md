# CredentialsStatusErrorReason

## Example Usage

```python
from mistralai.client.models import CredentialsStatusErrorReason

# Open enum: unrecognized values are captured as UnrecognizedStr
value: CredentialsStatusErrorReason = "oauth expired"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"oauth expired"`
- `"oauth near expiry"`
- `"empty credentials"`
- `"unparsable credentials"`
- `"you need to reconnect"`
- `"oauth refresh error"`
