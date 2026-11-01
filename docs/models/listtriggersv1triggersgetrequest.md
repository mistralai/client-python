# ListTriggersV1TriggersGetRequest


## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `handler`                                                              | [OptionalNullable[models.TriggerHandler]](../models/triggerhandler.md) | :heavy_minus_sign:                                                     | Filter by handler type                                                 |
| `primitive_id`                                                         | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Filter by primitive ID (workflow, agent, or app)                       |
| `event_source_id`                                                      | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | Filter by event source ID (webhook id)                                 |