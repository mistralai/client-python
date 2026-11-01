# WebhookProvider

## Example Usage

```python
from mistralai.client.models import WebhookProvider

# Open enum: unrecognized values are captured as UnrecognizedStr
value: WebhookProvider = "slack"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"slack"`
- `"github"`
- `"notion"`
- `"lucca"`
- `"linear"`
- `"microsoft"`
- `"ashby"`
- `"custom"`
