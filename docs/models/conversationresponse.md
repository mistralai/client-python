# ConversationResponse

The response after appending new entries to the conversation.


## Fields

| Field                                                                              | Type                                                                               | Required                                                                           | Description                                                                        |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `object`                                                                           | *Optional[Literal["conversation.response"]]*                                       | :heavy_minus_sign:                                                                 | N/A                                                                                |
| `conversation_id`                                                                  | *str*                                                                              | :heavy_check_mark:                                                                 | N/A                                                                                |
| `outputs`                                                                          | List[[models.ConversationResponseOutput](../models/conversationresponseoutput.md)] | :heavy_check_mark:                                                                 | N/A                                                                                |
| `usage`                                                                            | [models.ConversationUsageInfo](../models/conversationusageinfo.md)                 | :heavy_check_mark:                                                                 | N/A                                                                                |
| `guardrails`                                                                       | List[Dict[str, *Any*]]                                                             | :heavy_minus_sign:                                                                 | N/A                                                                                |