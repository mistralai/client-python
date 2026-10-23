# KeywordRetriever

Retrieve document chunks with similar keywords to the given query.

Uses the default settings for the index on the field.


## Fields

| Field                                                                                  | Type                                                                                   | Required                                                                               | Description                                                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `top_k`                                                                                | *Optional[int]*                                                                        | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `type`                                                                                 | *Literal["keyword"]*                                                                   | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `query`                                                                                | *str*                                                                                  | :heavy_check_mark:                                                                     | N/A                                                                                    |
| `operator`                                                                             | [Optional[models.Operator]](../models/operator.md)                                     | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `filter_`                                                                              | [OptionalNullable[models.KeywordRetrieverFilter]](../models/keywordretrieverfilter.md) | :heavy_minus_sign:                                                                     | N/A                                                                                    |
| `field`                                                                                | *OptionalNullable[str]*                                                                | :heavy_minus_sign:                                                                     | N/A                                                                                    |