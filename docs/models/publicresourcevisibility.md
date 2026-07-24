# PublicResourceVisibility

Visibility options available to public API callers.

Excludes ``shared_global`` which is reserved for system-owned connectors.

## Example Usage

```python
from mistralai.client.models import PublicResourceVisibility
value: PublicResourceVisibility = "shared_org"
```


## Values

- `"shared_org"`
- `"shared_workspace"`
- `"private"`
