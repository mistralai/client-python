# ConnectorErrorCode

## Example Usage

```python
from mistralai.client.models import ConnectorErrorCode

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ConnectorErrorCode = "connectors_count_limit_reached"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"connectors_count_limit_reached"`
- `"credentials_rejected"`
- `"server_unreachable"`
- `"custom_connectors_disabled"`
