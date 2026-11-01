# TriggerStatusValue

## Example Usage

```python
from mistralai.client.models import TriggerStatusValue

# Open enum: unrecognized values are captured as UnrecognizedStr
value: TriggerStatusValue = "SUBMITTED"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"SUBMITTED"`
- `"SUBMISSION_FAILED"`
- `"TRIGGERED"`
- `"TRIGGER_FAILED"`
