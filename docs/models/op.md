# Op

## Example Usage

```python
from mistralai.client.models import Op

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Op = "lt"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"lt"`
- `"lte"`
- `"gt"`
- `"gte"`
- `"startswith"`
- `"istartswith"`
- `"endswith"`
- `"iendswith"`
- `"contains"`
- `"icontains"`
- `"matches"`
- `"notcontains"`
- `"inotcontains"`
- `"eq"`
- `"neq"`
- `"isnull"`
- `"includes"`
- `"excludes"`
- `"len_eq"`
