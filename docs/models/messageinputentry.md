# MessageInputEntry

Representation of an input message inside the conversation.


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `role`                                                                       | [models.MessageInputEntryRole](../models/messageinputentryrole.md)           | :heavy_check_mark:                                                           | N/A                                                                          |
| `content`                                                                    | [models.MessageInputEntryContent](../models/messageinputentrycontent.md)     | :heavy_check_mark:                                                           | N/A                                                                          |
| `object`                                                                     | [Optional[models.Object]](../models/object.md)                               | :heavy_minus_sign:                                                           | N/A                                                                          |
| `type`                                                                       | [Optional[models.MessageInputEntryType]](../models/messageinputentrytype.md) | :heavy_minus_sign:                                                           | N/A                                                                          |
| `created_at`                                                                 | [date](https://docs.python.org/3/library/datetime.html#date-objects)         | :heavy_minus_sign:                                                           | N/A                                                                          |
| `completed_at`                                                               | [date](https://docs.python.org/3/library/datetime.html#date-objects)         | :heavy_minus_sign:                                                           | N/A                                                                          |
| `id`                                                                         | *Optional[str]*                                                              | :heavy_minus_sign:                                                           | N/A                                                                          |