# AudioURLChunk

Audio URL chunk.

Attributes:
    type: The type of the chunk, which is always `ChunkTypes.audio_url`.
    audio_url: The URL of the audio file.


## Fields

| Field                                              | Type                                               | Required                                           | Description                                        |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `type`                                             | *Literal["audio_url"]*                             | :heavy_check_mark:                                 | N/A                                                |
| `audio_url`                                        | [models.AudioURLUnion](../models/audiourlunion.md) | :heavy_check_mark:                                 | N/A                                                |