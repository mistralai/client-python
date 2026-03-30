# CompletionResponseStreamChoiceFinishReason

## Example Usage

```python
from mistralai.client.models import CompletionResponseStreamChoiceFinishReason

value = CompletionResponseStreamChoiceFinishReason.STOP

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name         | Value        |
| ------------ | ------------ |
| `STOP`       | stop         |
| `LENGTH`     | length       |
| `ERROR`      | error        |
| `TOOL_CALLS` | tool_calls   |