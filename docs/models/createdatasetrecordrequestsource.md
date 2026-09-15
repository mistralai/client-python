# CreateDatasetRecordRequestSource

Caller-declared channel that initiated record creation. This value does not certify that the payload is an unmodified copy of its source.

## Example Usage

```python
from mistralai.client.models import CreateDatasetRecordRequestSource
value: CreateDatasetRecordRequestSource = "DIRECT_INPUT"
```


## Values

- `"DIRECT_INPUT"`
- `"TELEMETRY_SPAN"`
