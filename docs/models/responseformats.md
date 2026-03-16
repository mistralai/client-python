# ResponseFormats

## Example Usage

```python
from mistralai.client.models import ResponseFormats

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ResponseFormats = "text"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"text"`
- `"json_object"`
- `"json_schema"`
