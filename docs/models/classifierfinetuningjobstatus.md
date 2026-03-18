# ClassifierFineTuningJobStatus

The current status of the fine-tuning job.

## Example Usage

```python
from mistralai.client.models import ClassifierFineTuningJobStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ClassifierFineTuningJobStatus = "QUEUED"
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
