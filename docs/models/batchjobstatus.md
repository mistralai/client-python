# BatchJobStatus

## Example Usage

```python
from mistralai.client.models import BatchJobStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: BatchJobStatus = "QUEUED"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"QUEUED"`
- `"RUNNING"`
- `"SUCCESS"`
- `"FAILED"`
- `"TIMEOUT_EXCEEDED"`
- `"CANCELLATION_REQUESTED"`
- `"CANCELLED"`
