# BaseTaskStatus

## Example Usage

```python
from mistralai.client.models import BaseTaskStatus

value = BaseTaskStatus.RUNNING

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name               | Value              |
| ------------------ | ------------------ |
| `RUNNING`          | RUNNING            |
| `COMPLETED`        | COMPLETED          |
| `FAILED`           | FAILED             |
| `CANCELED`         | CANCELED           |
| `TERMINATED`       | TERMINATED         |
| `CONTINUED_AS_NEW` | CONTINUED_AS_NEW   |
| `TIMED_OUT`        | TIMED_OUT          |
| `UNKNOWN`          | UNKNOWN            |