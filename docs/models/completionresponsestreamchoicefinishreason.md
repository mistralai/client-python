# CompletionResponseStreamChoiceFinishReason

## Example Usage

```python
from mistralai.client.models import CompletionResponseStreamChoiceFinishReason

# Open enum: unrecognized values are captured as UnrecognizedStr
value: CompletionResponseStreamChoiceFinishReason = "stop"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"stop"`
- `"length"`
- `"error"`
- `"tool_calls"`
