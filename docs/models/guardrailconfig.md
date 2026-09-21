# GuardrailConfig


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `block_on_error`                                                                     | *Optional[bool]*                                                                     | :heavy_minus_sign:                                                                   | If true, return HTTP 403 and block request in the event of a server-side error       |
| `moderation_llm_v1`                                                                  | [OptionalNullable[models.ModerationLlmv1Config]](../models/moderationllmv1config.md) | :heavy_minus_sign:                                                                   | N/A                                                                                  |
| `moderation_llm_v2`                                                                  | [OptionalNullable[models.ModerationLlmv2Config]](../models/moderationllmv2config.md) | :heavy_minus_sign:                                                                   | N/A                                                                                  |