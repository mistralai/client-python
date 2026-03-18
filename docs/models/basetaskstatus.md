# BaseTaskStatus

## Example Usage

```python
from mistralai.client.models import BaseTaskStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: BaseTaskStatus = "RUNNING"
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
- `"UNKNOWN"`
