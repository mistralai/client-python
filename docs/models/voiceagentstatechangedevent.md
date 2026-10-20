# VoiceAgentStateChangedEvent


## Fields

| Field                                      | Type                                       | Required                                   | Description                                |
| ------------------------------------------ | ------------------------------------------ | ------------------------------------------ | ------------------------------------------ |
| `type`                                     | *Optional[Literal["agent.state.changed"]]* | :heavy_minus_sign:                         | N/A                                        |
| `old_state`                                | [models.OldState](../models/oldstate.md)   | :heavy_check_mark:                         | N/A                                        |
| `state`                                    | [models.State](../models/state.md)         | :heavy_check_mark:                         | N/A                                        |
| `ts`                                       | *float*                                    | :heavy_check_mark:                         | N/A                                        |