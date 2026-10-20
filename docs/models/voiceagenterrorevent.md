# VoiceAgentErrorEvent

Shared error envelope for worker and SDK failures.


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `type`                                                                       | *Optional[Literal["error"]]*                                                 | :heavy_minus_sign:                                                           | N/A                                                                          |
| `source`                                                                     | [models.VoiceAgentErrorEventSource](../models/voiceagenterroreventsource.md) | :heavy_check_mark:                                                           | N/A                                                                          |
| `code`                                                                       | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          |
| `message`                                                                    | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          |
| `fatal`                                                                      | *bool*                                                                       | :heavy_check_mark:                                                           | N/A                                                                          |
| `payload`                                                                    | Dict[str, *Any*]                                                             | :heavy_minus_sign:                                                           | N/A                                                                          |