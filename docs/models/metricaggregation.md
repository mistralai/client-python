# MetricAggregation

## Example Usage

```python
from mistralai.client.models import MetricAggregation

# Open enum: unrecognized values are captured as UnrecognizedStr
value: MetricAggregation = "count"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"count"`
- `"count_distinct"`
- `"sum"`
- `"avg"`
- `"min"`
- `"max"`
- `"p50"`
- `"p90"`
- `"p95"`
- `"p99"`
