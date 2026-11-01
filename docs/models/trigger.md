# Trigger


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `id`                                                       | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `creator_id`                                               | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `workspace_id`                                             | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `organization_id`                                          | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `customer_id`                                              | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `owner_type`                                               | [models.TriggersOwnerType](../models/triggersownertype.md) | :heavy_check_mark:                                         | N/A                                                        |
| `event_source`                                             | [models.Webhook](../models/webhook.md)                     | :heavy_check_mark:                                         | N/A                                                        |
| `handler`                                                  | [models.TriggerHandler](../models/triggerhandler.md)       | :heavy_check_mark:                                         | N/A                                                        |
| `action`                                                   | [models.TriggerAction](../models/triggeraction.md)         | :heavy_check_mark:                                         | N/A                                                        |
| `filters`                                                  | *Nullable[str]*                                            | :heavy_check_mark:                                         | N/A                                                        |
| `title`                                                    | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |