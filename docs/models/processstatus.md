# ProcessStatus

## Example Usage

```python
from mistralai.client.models import ProcessStatus

value = ProcessStatus.SELF_MANAGED

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name                   | Value                  |
| ---------------------- | ---------------------- |
| `SELF_MANAGED`         | self_managed           |
| `MISSING_CONTENT`      | missing_content        |
| `NOOP`                 | noop                   |
| `DONE`                 | done                   |
| `TODO`                 | todo                   |
| `IN_PROGRESS`          | in_progress            |
| `ERROR`                | error                  |
| `WAITING_FOR_CAPACITY` | waiting_for_capacity   |