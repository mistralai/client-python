# SharingDelete


## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `org_id`                                                             | *str*                                                                | :heavy_check_mark:                                                   | N/A                                                                  |
| `share_with_uuid`                                                    | *str*                                                                | :heavy_check_mark:                                                   | The id of the entity (user, workspace or organization) to share with |
| `share_with_type`                                                    | [models.EntityType](../models/entitytype.md)                         | :heavy_check_mark:                                                   | The type of entity, used to share a library.                         |