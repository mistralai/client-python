# DeleteManagedIndexResponse

Wire representation returned when an index is deleted (id, name, status).


## Fields

| Field                                                                         | Type                                                                          | Required                                                                      | Description                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `id`                                                                          | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `name`                                                                        | *str*                                                                         | :heavy_check_mark:                                                            | N/A                                                                           |
| `status`                                                                      | [models.ManagedIndexStatus](../models/managedindexstatus.md)                  | :heavy_check_mark:                                                            | Lifecycle of an index. Derived, not stored -- see ``managed_index_from_row``. |