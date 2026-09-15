# TranscriptionStreamEventTypes

## Example Usage

```python
from mistralai.client.models import TranscriptionStreamEventTypes

# Open enum: unrecognized values are captured as UnrecognizedStr
value: TranscriptionStreamEventTypes = "transcription.language"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"transcription.language"`
- `"transcription.segment"`
- `"transcription.text.delta"`
- `"transcription.done"`
