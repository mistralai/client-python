# VoiceAgentSessionUpdatedEvent

Sent to every participant once a session update is committed.

`instructions` and `tools` reach the agent at its next turn boundary.


## Fields

| Field                                                                                              | Type                                                                                               | Required                                                                                           | Description                                                                                        |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `type`                                                                                             | *Optional[Literal["session.updated"]]*                                                             | :heavy_minus_sign:                                                                                 | N/A                                                                                                |
| `session`                                                                                          | [models.AudioAgentConfigurationResponseConfig](../models/audioagentconfigurationresponseconfig.md) | :heavy_check_mark:                                                                                 | N/A                                                                                                |
| `ts`                                                                                               | *float*                                                                                            | :heavy_check_mark:                                                                                 | N/A                                                                                                |