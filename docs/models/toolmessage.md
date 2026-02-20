# ToolMessage


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `role`                                                                 | *Optional[Literal["tool"]]*                                            | :heavy_minus_sign:                                                     | N/A                                                                    |
| `content`                                                              | [Nullable[models.ToolMessageContent]](../models/toolmessagecontent.md) | :heavy_check_mark:                                                     | N/A                                                                    |
| `tool_call_id`                                                         | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | N/A                                                                    |
| `name`                                                                 | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | N/A                                                                    |