# JobsAPIRoutesFineTuningGetFineTuningJobsStatus

The current job state to filter on. When set, the other results are not displayed.

## Example Usage

```python
from mistralai.client.models import JobsAPIRoutesFineTuningGetFineTuningJobsStatus
value: JobsAPIRoutesFineTuningGetFineTuningJobsStatus = "QUEUED"
```


## Values

- `"QUEUED"`
- `"STARTED"`
- `"VALIDATING"`
- `"VALIDATED"`
- `"RUNNING"`
- `"FAILED_VALIDATION"`
- `"FAILED"`
- `"SUCCESS"`
- `"CANCELLED"`
- `"CANCELLATION_REQUESTED"`
