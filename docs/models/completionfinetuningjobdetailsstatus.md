# CompletionFineTuningJobDetailsStatus

## Example Usage

```python
from mistralai.client.models import CompletionFineTuningJobDetailsStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: CompletionFineTuningJobDetailsStatus = "QUEUED"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"QUEUED"`
- `"STARTED"`
- `"VALIDATING"`
- `"VALIDATED"`
- `"RUNNING"`
- `"FAILED_VALIDATION"`
- `"FAILED"`
- `"SUCCESS"`
- `"CANCELLED"`
- `"CANCELLATION_REQUESTED"`
