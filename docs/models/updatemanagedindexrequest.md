# UpdateManagedIndexRequest

The schema an index should have. Sent whole, not as a patch.

No ``config``: the embedding configuration is fixed at creation, so there is
nothing for a caller to send back.


## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `schema_`                                                    | [models.ManagedIndexFields](../models/managedindexfields.md) | :heavy_check_mark:                                           | N/A                                                          |