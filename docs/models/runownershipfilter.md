# RunOwnershipFilter

OR-able group isolating the "runs I care about" default (created by me OR in my starred projects).

Kept separate from the plain generic filters so it can OR internally while still AND-ing with
everything else. The UI drives it via two sugar chips: "Created by me" writes `creator_ids`, and
"Starred projects" sets `starred_by_me`. Dropping a chip clears its term and the OR collapses to the
remaining one; dropping both leaves the group empty (no ownership scoping).

`starred_by_me` is resolved server-side against the caller's favorites, so the client never has to
page through projects to collect starred ids — and a caller with zero starred projects correctly
matches no runs (rather than falling through to the whole workspace). `project_ids` remains for
explicit, caller-supplied project scoping.


## Fields

| Field                                                              | Type                                                               | Required                                                           | Description                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `combinator`                                                       | [Optional[models.FilterCombinator]](../models/filtercombinator.md) | :heavy_minus_sign:                                                 | N/A                                                                |
| `creator_ids`                                                      | List[*str*]                                                        | :heavy_minus_sign:                                                 | N/A                                                                |
| `project_ids`                                                      | List[*str*]                                                        | :heavy_minus_sign:                                                 | N/A                                                                |
| `starred_by_me`                                                    | *Optional[bool]*                                                   | :heavy_minus_sign:                                                 | N/A                                                                |