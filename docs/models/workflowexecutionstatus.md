# WorkflowExecutionStatus

## Example Usage

```python
from mistralai.client.models import WorkflowExecutionStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: WorkflowExecutionStatus = "RUNNING"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"RUNNING"`
- `"COMPLETED"`
- `"FAILED"`
- `"CANCELED"`
- `"TERMINATED"`
- `"CONTINUED_AS_NEW"`
- `"TIMED_OUT"`
- `"RETRYING_AFTER_ERROR"`
