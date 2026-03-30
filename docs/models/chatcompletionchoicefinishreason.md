# ChatCompletionChoiceFinishReason

## Example Usage

```python
from mistralai.client.models import ChatCompletionChoiceFinishReason

value = ChatCompletionChoiceFinishReason.STOP

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name           | Value          |
| -------------- | -------------- |
| `STOP`         | stop           |
| `LENGTH`       | length         |
| `MODEL_LENGTH` | model_length   |
| `ERROR`        | error          |
| `TOOL_CALLS`   | tool_calls     |