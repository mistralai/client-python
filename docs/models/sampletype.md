# SampleType

## Example Usage

```python
from mistralai.client.models import SampleType

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SampleType = "pretrain"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"pretrain"`
- `"instruct"`
- `"batch_request"`
- `"batch_result"`
- `"batch_error"`
