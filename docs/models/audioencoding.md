# AudioEncoding

## Example Usage

```python
from mistralai.client.models import AudioEncoding

# Open enum: unrecognized values are captured as UnrecognizedStr
value: AudioEncoding = "pcm_s16le"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"pcm_s16le"`
- `"pcm_s32le"`
- `"pcm_f16le"`
- `"pcm_f32le"`
- `"pcm_mulaw"`
- `"pcm_alaw"`
