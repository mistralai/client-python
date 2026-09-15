# ScheduleOverlapPolicy

Controls what happens when a workflow would be started by a schedule but
one is already running.

## Example Usage

```python
from mistralai.client.models import ScheduleOverlapPolicy

# Open enum: unrecognized values are captured as UnrecognizedInt
value: ScheduleOverlapPolicy = 1
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `1`
- `2`
- `3`
- `4`
- `5`
- `6`
