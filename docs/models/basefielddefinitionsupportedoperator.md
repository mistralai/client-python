# BaseFieldDefinitionSupportedOperator

## Example Usage

```python
from mistralai.client.models import BaseFieldDefinitionSupportedOperator

# Open enum: unrecognized values are captured as UnrecognizedStr
value: BaseFieldDefinitionSupportedOperator = "lt"
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
