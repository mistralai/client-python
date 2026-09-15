# QueryInvocationBody


## Fields

| Field                                                                                      | Type                                                                                       | Required                                                                                   | Description                                                                                |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `name`                                                                                     | *str*                                                                                      | :heavy_check_mark:                                                                         | The name of the query to request                                                           |
| `input`                                                                                    | [OptionalNullable[models.QueryInvocationBodyInput]](../models/queryinvocationbodyinput.md) | :heavy_minus_sign:                                                                         | Input data for the query, matching its schema                                              |