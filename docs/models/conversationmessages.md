# ConversationMessages

Similar to the conversation history but only keep the messages


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `object`                                                                               | [Optional[models.ConversationMessagesObject]](../models/conversationmessagesobject.md) | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `conversation_id`                                                                      | *str*                                                                                  | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `messages`                                                                             | List[[models.MessageEntries](../models/messageentries.md)]                             | :heavy_check_mark:                                                                     | N/A                                                                                    |