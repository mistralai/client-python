# ClassifierFineTuningJobDetailsStatus

## Example Usage

```python
from mistralai.client.models import ClassifierFineTuningJobDetailsStatus

value = ClassifierFineTuningJobDetailsStatus.QUEUED

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name                     | Value                    |
| ------------------------ | ------------------------ |
| `QUEUED`                 | QUEUED                   |
| `STARTED`                | STARTED                  |
| `VALIDATING`             | VALIDATING               |
| `VALIDATED`              | VALIDATED                |
| `RUNNING`                | RUNNING                  |
| `FAILED_VALIDATION`      | FAILED_VALIDATION        |
| `FAILED`                 | FAILED                   |
| `SUCCESS`                | SUCCESS                  |
| `CANCELLED`              | CANCELLED                |
| `CANCELLATION_REQUESTED` | CANCELLATION_REQUESTED   |