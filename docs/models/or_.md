# Or

Disjunction: rows must match at least one sub-filter.


## Fields

| Field                                        | Type                                         | Required                                     | Description                                  |
| -------------------------------------------- | -------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| `type`                                       | *Literal["or"]*                              | :heavy_check_mark:                           | N/A                                          |
| `matches`                                    | List[[models.OrMatch](../models/ormatch.md)] | :heavy_check_mark:                           | N/A                                          |