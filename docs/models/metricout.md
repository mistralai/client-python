# MetricOut

Metrics at the step number during the fine-tuning job. Use these metrics to assess if the training is going smoothly (loss should decrease, token accuracy should increase).


## Fields

| Field                       | Type                        | Required                    | Description                 |
| --------------------------- | --------------------------- | --------------------------- | --------------------------- |
| `train_loss`                | *OptionalNullable[float]*   | :heavy_minus_sign:          | N/A                         |
| `valid_loss`                | *OptionalNullable[float]*   | :heavy_minus_sign:          | N/A                         |
| `valid_mean_token_accuracy` | *OptionalNullable[float]*   | :heavy_minus_sign:          | N/A                         |