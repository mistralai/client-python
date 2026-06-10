# PromptsGetRequest


## Fields

| Field                                   | Type                                    | Required                                | Description                             |
| --------------------------------------- | --------------------------------------- | --------------------------------------- | --------------------------------------- |
| `prompt_id`                             | *str*                                   | :heavy_check_mark:                      | N/A                                     |
| `version`                               | *Optional[int]*                         | :heavy_minus_sign:                      | Fetch specific version number.          |
| `alias`                                 | *Optional[str]*                         | :heavy_minus_sign:                      | Fetch version pointed to by alias name. |
| `fields`                                | List[*str*]                             | :heavy_minus_sign:                      | The set of field mask paths.            |