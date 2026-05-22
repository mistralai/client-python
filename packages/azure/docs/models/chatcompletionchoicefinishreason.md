# ChatCompletionChoiceFinishReason

## Example Usage

```python
from mistralai.azure.client.models import ChatCompletionChoiceFinishReason

# Open enum: unrecognized values are captured as UnrecognizedStr
value: ChatCompletionChoiceFinishReason = "stop"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"stop"`
- `"length"`
- `"model_length"`
- `"error"`
- `"tool_calls"`
