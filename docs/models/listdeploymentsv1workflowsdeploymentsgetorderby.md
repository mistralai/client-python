# ListDeploymentsV1WorkflowsDeploymentsGetOrderBy

Field to sort by. When omitted, active and managed deployments are grouped first, then sorted by created_at. When set, results are sorted purely by the specified field with no grouping.

## Example Usage

```python
from mistralai.client.models import ListDeploymentsV1WorkflowsDeploymentsGetOrderBy
value: ListDeploymentsV1WorkflowsDeploymentsGetOrderBy = "updated_at"
```


## Values

- `"updated_at"`
- `"created_at"`
