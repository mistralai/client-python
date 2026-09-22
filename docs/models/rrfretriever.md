# RRFRetriever

Fuse child retriever rankings via reciprocal rank fusion.


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `top_k`                                                                        | *Optional[int]*                                                                | :heavy_minus_sign:                                                             | N/A                                                                            |
| `type`                                                                         | *Literal["rrf"]*                                                               | :heavy_check_mark:                                                             | N/A                                                                            |
| `retrievers`                                                                   | List[[models.RRFRetrieverRetriever](../models/rrfretrieverretriever.md)]       | :heavy_check_mark:                                                             | N/A                                                                            |
| `weights`                                                                      | List[*float*]                                                                  | :heavy_minus_sign:                                                             | N/A                                                                            |
| `rank_constant`                                                                | *Optional[int]*                                                                | :heavy_minus_sign:                                                             | N/A                                                                            |
| `filter_`                                                                      | [OptionalNullable[models.RRFRetrieverFilter]](../models/rrfretrieverfilter.md) | :heavy_minus_sign:                                                             | N/A                                                                            |