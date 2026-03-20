# ChatCompletionChoiceFinishReason1

## Example Usage

```python
from mistralai.client.models import ChatCompletionChoiceFinishReason1

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ChatCompletionChoiceFinishReason1 = "stop"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"stop"`
- `"length"`
- `"model_length"`
- `"error"`
- `"tool_calls"`
