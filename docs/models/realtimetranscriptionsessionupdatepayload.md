# RealtimeTranscriptionSessionUpdatePayload


## Fields

| Field                                                                              | Type                                                                               | Required                                                                           | Description                                                                        |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `audio_format`                                                                     | [OptionalNullable[models.AudioFormat]](../models/audioformat.md)                   | :heavy_minus_sign:                                                                 | Set before sending audio. Audio format updates are rejected after audio starts.    |
| `target_streaming_delay_ms`                                                        | *OptionalNullable[int]*                                                            | :heavy_minus_sign:                                                                 | Set before sending audio. Streaming delay updates are rejected after audio starts. |