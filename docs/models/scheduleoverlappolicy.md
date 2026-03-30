# ScheduleOverlapPolicy

Controls what happens when a workflow would be started by a schedule but
one is already running.

## Example Usage

```python
from mistralai.client.models import ScheduleOverlapPolicy

value = ScheduleOverlapPolicy.ONE

# Open enum: unrecognized values are captured as UnrecognizedInt
```


## Values

| Name    | Value   |
| ------- | ------- |
| `ONE`   | 1       |
| `TWO`   | 2       |
| `THREE` | 3       |
| `FOUR`  | 4       |
| `FIVE`  | 5       |
| `SIX`   | 6       |