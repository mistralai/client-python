# OAuthMetadataSource

How a connector's OAuth server metadata was obtained.

## Example Usage

```python
from mistralai.client.models import OAuthMetadataSource

# Open enum: unrecognized values are captured as UnrecognizedStr
value: OAuthMetadataSource = "autodiscovery"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"autodiscovery"`
- `"provided"`
