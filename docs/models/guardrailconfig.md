# GuardrailConfig


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `block_on_error`                                                               | *Optional[bool]*                                                               | :heavy_minus_sign:                                                             | If true, return HTTP 403 and block request in the event of a server-side error |
| `moderation_llm_v1`                                                            | [Nullable[models.ModerationLlmv1Config]](../models/moderationllmv1config.md)   | :heavy_check_mark:                                                             | N/A                                                                            |