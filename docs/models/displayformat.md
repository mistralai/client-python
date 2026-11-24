# DisplayFormat

How an evaluator's numeric values render: ``percent``, ``integer`` or ``number``.

## Example Usage

```python
from mistralai.client.models import DisplayFormat

# Open enum: unrecognized values are captured as UnrecognizedStr
value: DisplayFormat = "number"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"number"`
- `"percent"`
- `"integer"`
