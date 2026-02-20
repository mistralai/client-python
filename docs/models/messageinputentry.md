# MessageInputEntry

Representation of an input message inside the conversation.


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `object`                                                                 | *Optional[Literal["entry"]]*                                             | :heavy_minus_sign:                                                       | N/A                                                                      |
| `type`                                                                   | *Optional[Literal["message.input"]]*                                     | :heavy_minus_sign:                                                       | N/A                                                                      |
| `created_at`                                                             | [date](https://docs.python.org/3/library/datetime.html#date-objects)     | :heavy_minus_sign:                                                       | N/A                                                                      |
| `completed_at`                                                           | [date](https://docs.python.org/3/library/datetime.html#date-objects)     | :heavy_minus_sign:                                                       | N/A                                                                      |
| `id`                                                                     | *Optional[str]*                                                          | :heavy_minus_sign:                                                       | N/A                                                                      |
| `role`                                                                   | [models.Role](../models/role.md)                                         | :heavy_check_mark:                                                       | N/A                                                                      |
| `content`                                                                | [models.MessageInputEntryContent](../models/messageinputentrycontent.md) | :heavy_check_mark:                                                       | N/A                                                                      |
| `prefix`                                                                 | *Optional[bool]*                                                         | :heavy_minus_sign:                                                       | N/A                                                                      |