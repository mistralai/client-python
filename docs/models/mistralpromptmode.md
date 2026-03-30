# MistralPromptMode

Available options to the prompt_mode argument on the chat completion endpoint.
Values represent high-level intent. Assignment to actual SPs is handled internally.
System prompt may include knowledge cutoff date, model capabilities, tone to use, safety guidelines, etc.

## Example Usage

```python
from mistralai.client.models import MistralPromptMode

value = MistralPromptMode.REASONING

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name        | Value       |
| ----------- | ----------- |
| `REASONING` | reasoning   |