# BuiltInConnectors

## Example Usage

```python
from mistralai.client.models import BuiltInConnectors

# Open enum: unrecognized values are captured as UnrecognizedStr
value: BuiltInConnectors = "web_search"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"web_search"`
- `"web_search_premium"`
- `"code_interpreter"`
- `"image_generation"`
- `"document_library"`
