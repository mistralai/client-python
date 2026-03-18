# MistralPromptMode

Available options to the prompt_mode argument on the chat completion endpoint.
Values represent high-level intent. Assignment to actual SPs is handled internally.
System prompt may include knowledge cutoff date, model capabilities, tone to use, safety guidelines, etc.

## Example Usage

```python
from mistralai.azure.client.models import MistralPromptMode

# Open enum: unrecognized values are captured as UnrecognizedStr
value: MistralPromptMode = "reasoning"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"reasoning"`
