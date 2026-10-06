# ListOptimizationsV1ObservabilityOptimizationsGetRequest


## Fields

| Field                      | Type                       | Required                   | Description                |
| -------------------------- | -------------------------- | -------------------------- | -------------------------- |
| `project`                  | *OptionalNullable[str]*    | :heavy_minus_sign:         | Filter by project slug     |
| `evaluation`               | *OptionalNullable[str]*    | :heavy_minus_sign:         | Filter by evaluation slug  |
| `status`                   | *OptionalNullable[str]*    | :heavy_minus_sign:         | Filter by lifecycle status |
| `algorithm`                | *OptionalNullable[str]*    | :heavy_minus_sign:         | Filter by algorithm        |
| `tags`                     | List[*str*]                | :heavy_minus_sign:         | Filter by tags             |
| `page_size`                | *Optional[int]*            | :heavy_minus_sign:         | N/A                        |
| `page`                     | *Optional[int]*            | :heavy_minus_sign:         | N/A                        |