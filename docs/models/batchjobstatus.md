# BatchJobStatus

## Example Usage

```python
from mistralai.client.models import BatchJobStatus

value = BatchJobStatus.QUEUED

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name                     | Value                    |
| ------------------------ | ------------------------ |
| `QUEUED`                 | QUEUED                   |
| `RUNNING`                | RUNNING                  |
| `SUCCESS`                | SUCCESS                  |
| `FAILED`                 | FAILED                   |
| `TIMEOUT_EXCEEDED`       | TIMEOUT_EXCEEDED         |
| `CANCELLATION_REQUESTED` | CANCELLATION_REQUESTED   |
| `CANCELLED`              | CANCELLED                |