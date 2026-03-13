# MessageTokens

Information on a single message included in a tokenized prompt as part of an InstructRequest.


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `role`                                                     | [models.MessageTokensRole](../models/messagetokensrole.md) | :heavy_check_mark:                                         | N/A                                                        |
| `total_tokens`                                             | *Nullable[int]*                                            | :heavy_check_mark:                                         | N/A                                                        |
| `truncated`                                                | *Optional[bool]*                                           | :heavy_minus_sign:                                         | N/A                                                        |
| `usage_count`                                              | *Optional[int]*                                            | :heavy_minus_sign:                                         | N/A                                                        |