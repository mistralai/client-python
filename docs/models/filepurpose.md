# FilePurpose

## Example Usage

```python
from mistralai.client.models import FilePurpose

# Open enum: unrecognized values are captured as UnrecognizedStr
value: FilePurpose = "fine-tune"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"fine-tune"`
- `"batch"`
- `"ocr"`
