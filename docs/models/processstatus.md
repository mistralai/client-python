# ProcessStatus

## Example Usage

```python
from mistralai.client.models import ProcessStatus

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ProcessStatus = "self_managed"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"self_managed"`
- `"missing_content"`
- `"noop"`
- `"done"`
- `"todo"`
- `"in_progress"`
- `"error"`
- `"waiting_for_capacity"`
