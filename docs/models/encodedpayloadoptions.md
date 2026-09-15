# EncodedPayloadOptions

## Example Usage

```python
from mistralai.client.models import EncodedPayloadOptions

# Open enum: unrecognized values are captured as UnrecognizedStr
value: EncodedPayloadOptions = "offloaded"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"offloaded"`
- `"encrypted"`
- `"encrypted-partial"`
- `"compressed"`
