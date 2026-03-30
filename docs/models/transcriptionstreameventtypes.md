# TranscriptionStreamEventTypes

## Example Usage

```python
from mistralai.client.models import TranscriptionStreamEventTypes

value = TranscriptionStreamEventTypes.TRANSCRIPTION_LANGUAGE

# Open enum: unrecognized values are captured as UnrecognizedStr
```


## Values

| Name                       | Value                      |
| -------------------------- | -------------------------- |
| `TRANSCRIPTION_LANGUAGE`   | transcription.language     |
| `TRANSCRIPTION_SEGMENT`    | transcription.segment      |
| `TRANSCRIPTION_TEXT_DELTA` | transcription.text.delta   |
| `TRANSCRIPTION_DONE`       | transcription.done         |