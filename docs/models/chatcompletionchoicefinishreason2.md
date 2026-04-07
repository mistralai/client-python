# ChatCompletionChoiceFinishReason2

## Example Usage

```python
from mistralai.client.models import ChatCompletionChoiceFinishReason2

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ChatCompletionChoiceFinishReason2 = "stop"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"stop"`
- `"length"`
- `"model_length"`
- `"error"`
- `"tool_calls"`
