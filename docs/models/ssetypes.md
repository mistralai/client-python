# SSETypes

Server side events sent when streaming a conversation response.

## Example Usage

```python
from mistralai.client.models import SSETypes

# Open enum: unrecognized values are captured as UnrecognizedStr
value: SSETypes = "conversation.response.started"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"conversation.response.started"`
- `"conversation.response.done"`
- `"conversation.response.error"`
- `"message.output.delta"`
- `"tool.execution.started"`
- `"tool.execution.delta"`
- `"tool.execution.done"`
- `"agent.handoff.started"`
- `"agent.handoff.done"`
- `"function.call.delta"`
