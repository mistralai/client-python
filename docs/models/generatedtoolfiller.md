# GeneratedToolFiller

A filler the model writes for each call, in the user's language.

`instructions` guide what it says. `fallback` is spoken when it writes none;
without one, the call is silent.


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `type`                                                     | *Literal["generated"]*                                     | :heavy_check_mark:                                         | N/A                                                        |
| `instructions`                                             | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `fallback`                                                 | [OptionalNullable[models.Fallback]](../models/fallback.md) | :heavy_minus_sign:                                         | N/A                                                        |